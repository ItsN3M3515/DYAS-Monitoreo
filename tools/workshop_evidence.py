#!/usr/bin/env python3
"""Ejercicios reales sobre el stack de laboratorio ya iniciado, con fallas temporales.

No inicia Docker ni modifica el host. Configura y restablece /api/fallas; ejecuta k6.
El workflow manual usa un runner nuevo y conserva datos, capturas y timestamps UTC.
"""

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from playwright.sync_api import sync_playwright


QUERIES = {
    "3": 'sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*"}[1m]))',
    "5": 'sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*", status=~"5.."}[1m])) / sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*"}[1m]))',
    "6": 'histogram_quantile(0.95, sum by (application, le) (rate(http_server_requests_seconds_bucket{uri!~"/actuator.*"}[1m])))',
    "7": 'sum by (resultado) (increase(pedidos_total[5m]))',
}
PROM = "http://localhost:9090"
INVENTARIO = "http://localhost:8082"
PEDIDOS = "http://localhost:8081"
JAEGER = "http://localhost:16686"
GRAFANA = "http://localhost:3000"


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def request(url, method="GET", payload=None, headers=None):
    body = json.dumps(payload).encode() if payload is not None else None
    values = {"Content-Type": "application/json", **(headers or {})}
    try:
        with urlopen(Request(url, data=body, headers=values, method=method), timeout=20) as response:
            return response.status, response.read().decode()
    except HTTPError as error:
        return error.code, error.read().decode()


def get_json(url):
    status, body = request(url)
    if status != 200:
        raise RuntimeError(f"GET {url}: HTTP {status}: {body[:300]}")
    return json.loads(body)


class Workshop:
    def __init__(self, output, page):
        self.output = output
        self.page = page
        self.timeline = []
        self.browser_errors = []
        page.on("pageerror", lambda error: self.browser_errors.append(str(error)))
        page.on("requestfailed", lambda req: self.browser_errors.append(f"{req.url}: {req.failure}"))
        output.mkdir(parents=True, exist_ok=True)

    def save(self, name, value):
        (self.output / f"{name}.json").write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

    def event(self, phase, **values):
        item = {"utc": now(), "phase": phase, **values}
        print(json.dumps(item), flush=True)
        self.timeline.append(item)
        self.save("timeline", self.timeline)

    def screenshot(self, name, url, text=None):
        self.browser_errors.clear()
        try:
            response = self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            assert response and response.ok, f"HTTP {response.status if response else 'sin respuesta'}: {url}"
            self.page.wait_for_function("document.body && document.body.innerText.trim().length > 40", timeout=45000)
            if text:
                element = self.page.get_by_text(text, exact=False).first
                element.wait_for(timeout=45000)
                element.scroll_into_view_if_needed()
            self.page.wait_for_timeout(2500)
        except Exception:
            (self.output / f"{name}-failed.html").write_text(self.page.content())
            self.page.screenshot(path=str(self.output / f"{name}-failed.png"), full_page=True)
            raise
        finally:
            self.save(f"{name}-browser", {"utc": now(), "url": self.page.url, "title": self.page.title(), "body_excerpt": self.page.locator("body").inner_text()[:2500], "errors": self.browser_errors})
        self.page.screenshot(path=str(self.output / f"{name}.png"), full_page=True)
        self.event("screenshot", name=name, url=url)

    def dashboard(self, name):
        # Usar la ruta canónica de Grafana, incluidos UID y slug.
        metadata = get_json(GRAFANA + "/api/dashboards/uid/tienda-observabilidad")["meta"]
        self.screenshot(name, GRAFANA + metadata["url"] + "?from=now-10m&to=now&kiosk", "Inventario: peticiones por endpoint")

    def faults(self, query=""):
        method = "POST" if query else "DELETE"
        status, body = request(INVENTARIO + "/api/fallas" + ("?" + query if query else ""), method)
        if status != 200:
            raise RuntimeError(f"No se pudo configurar el simulador: {status} {body}")
        self.event("fault-configuration", configuration=json.loads(body))

    def metrics(self, phase, screenshots=False):
        for number, query in QUERIES.items():
            result = get_json(PROM + "/api/v1/query?" + urlencode({"query": query}))
            if result["status"] != "success":
                raise RuntimeError(result)
            self.save(f"query-{number}-{phase}", {"utc": now(), "query": query, "response": result})
            if screenshots:
                url = PROM + "/query?" + urlencode({"g0.expr": query, "g0.tab": "1"})
                self.screenshot(f"query-{number}-{phase}", url)

    def alert_state(self):
        result = get_json(PROM + "/api/v1/rules?type=alert")
        return {rule["name"]: rule for group in result["data"]["groups"] for rule in group["rules"]}

    def wait_alert(self, name, state, timeout=150):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            rules = self.alert_state()
            if rules.get(name, {}).get("state") == state:
                filename = f"alert-{name}-{state}"
                self.save(filename, {"utc": now(), "rules": rules})
                self.event("alert-state", name=name, state=state)
                self.screenshot(filename, PROM + "/alerts", name)
                return rules[name]
            time.sleep(2)
        raise RuntimeError(f"{name} no alcanzó {state}; último estado: {rules}")

    def probe(self, label, expected):
        for attempt in range(30):
            trace_id = secrets.token_hex(16)
            parent_id = secrets.token_hex(8)
            status, body = request(
                PEDIDOS + "/api/pedidos", "POST", {"producto": "teclado", "cantidad": 1},
                {"traceparent": f"00-{trace_id}-{parent_id}-01"},
            )
            if status == expected:
                self.save(f"request-{label}", {"utc": now(), "status": status, "body": json.loads(body), "trace_id": trace_id, "injected_parent_id": parent_id})
                return trace_id
            time.sleep(0.3)
        raise RuntimeError(f"No se obtuvo HTTP {expected} para {label}")

    @staticmethod
    def spans(body):
        # grpc-gateway puede transmitir varios objetos JSON, uno por bloque OTLP.
        decoder, resources, remaining = json.JSONDecoder(), [], body.strip()
        while remaining:
            value, end = decoder.raw_decode(remaining)
            resources.extend(value.get("result", value).get("resourceSpans", []))
            remaining = remaining[end:].lstrip()
        rows = []
        for resource in resources:
            attributes = {item["key"]: item["value"].get("stringValue") for item in resource["resource"].get("attributes", [])}
            for scope in resource.get("scopeSpans", []):
                for span in scope.get("spans", []):
                    trace_id = span["traceId"]
                    if not re.fullmatch(r"[0-9a-fA-F]{32}", trace_id):
                        trace_id = base64.b64decode(trace_id).hex()
                    rows.append({"service": attributes.get("service.name"), "trace_id": trace_id.lower(), "span_id": span["spanId"], "parent_span_id": span.get("parentSpanId"), "name": span["name"], "duration_ms": (int(span["endTimeUnixNano"]) - int(span["startTimeUnixNano"])) / 1_000_000, "status": span.get("status", {}), "attributes": span.get("attributes", [])})
        return rows

    def trace(self, label, trace_id):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            status, body = request(JAEGER + "/api/v3/traces/" + trace_id)
            if status == 200:
                rows = self.spans(body)
                if len(rows) >= 3 and {row["service"] for row in rows} == {"pedidos", "inventario"}:
                    assert all(row["trace_id"] == trace_id for row in rows)
                    (self.output / f"trace-{label}-otlp.json").write_text(body + "\n")
                    self.save(f"trace-{label}", {"utc": now(), "trace_id": trace_id, "spans": rows})
                    self.screenshot(f"trace-{label}", JAEGER + "/trace/" + trace_id, "inventario")
                    return rows
            time.sleep(2)
        raise RuntimeError(f"No se encontró una traza de ambos servicios: {trace_id}")

    def run(self):
        self.faults()
        dashboard = get_json(GRAFANA + "/api/dashboards/uid/tienda-observabilidad")
        self.save("dashboard-provisioned", dashboard)
        panel = next(p for p in dashboard["dashboard"]["panels"] if p["id"] == 12)
        assert panel["title"] == "Inventario: peticiones por endpoint"
        # Con allowUiUpdates=true, Grafana deja meta.provisioned en false:
        # ese indicador controla la edición. El ID externo identifica el archivo.
        assert dashboard["meta"].get("provisionedExternalId", "").endswith("tienda.json"), dashboard["meta"]
        source = json.loads(Path("grafana/dashboards/tienda.json").read_text())
        assert panel["targets"] == next(p for p in source["panels"] if p["id"] == 12)["targets"]
        self.event("fresh-stack-panel-verified", panel_id=12)
        self.event("baseline-start")
        for _ in range(13):
            time.sleep(5)
        targets = get_json(PROM + "/api/v1/targets")
        shop = [t for t in targets["data"]["activeTargets"] if t["labels"].get("job") == "tienda"]
        assert len(shop) == 2 and all(t["health"] == "up" for t in shop)
        self.save("targets", targets)
        self.screenshot("targets-up", PROM + "/targets", "tienda")
        self.metrics("baseline", screenshots=True)
        self.dashboard("dashboard-baseline")
        self.save("alerts-baseline", self.alert_state())
        assert all(rule["state"] == "inactive" for rule in self.alert_state().values())
        self.trace("normal", self.probe("normal", 201))

        self.faults("tasaError=0.3")
        self.wait_alert("TasaDeErroresAlta", "pending")
        self.wait_alert("TasaDeErroresAlta", "firing")
        self.metrics("errors", screenshots=True)
        self.dashboard("dashboard-errors-firing")
        error_id = self.probe("error", 503)
        self.trace("error", error_id)
        logs = {}
        for service in ("pedidos", "inventario"):
            output = subprocess.check_output(["docker", "compose", "logs", "--no-color", service], text=True)
            matching = [line for line in output.splitlines() if error_id in line and "ERROR" in line]
            assert matching, f"No se encontró el log ERROR de {service}: {error_id}"
            logs[service] = matching
        self.save("correlated-logs", {"utc": now(), "trace_id": error_id, "logs": logs})

        self.faults("latenciaMs=800")
        self.wait_alert("LatenciaP95Alta", "pending")
        self.wait_alert("LatenciaP95Alta", "firing")
        self.metrics("latency")
        self.dashboard("dashboard-latency-firing")
        slow = self.trace("slow", self.probe("slow", 201))
        assert any(row["service"] == "inventario" and row["duration_ms"] >= 750 for row in slow)

        self.faults()
        deadline = time.monotonic() + 150
        while time.monotonic() < deadline:
            rules = self.alert_state()
            if all(rule["state"] == "inactive" for rule in rules.values()):
                self.save("alerts-recovered", {"utc": now(), "rules": rules})
                break
            time.sleep(2)
        else:
            raise RuntimeError("Las alertas no regresaron a Inactive")
        assert get_json(INVENTARIO + "/api/fallas") == {"latenciaMs": 0, "tasaError": 0.0}
        self.screenshot("alerts-recovered", PROM + "/alerts")
        self.dashboard("dashboard-recovered")
        self.metrics("recovered")
        self.event("workshop-complete", faults_reset=True, alerts_inactive=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidence/runtime"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "k6.log").open("w") as traffic_log, sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1800, "height": 1400}, device_scale_factor=1)
        workshop = Workshop(args.output, page)
        # Esperar a que exista el contenedor evita la carrera entre pull, arranque y
        # limpieza. --no-deps conserva los procesos ya verificados por Compose.
        subprocess.run(["docker", "compose", "run", "-d", "--no-deps", "--rm", "--name", "dyas-workshop-k6", "-e", "DURACION=12m", "k6"], check=True)
        traffic = subprocess.Popen(["docker", "logs", "--follow", "dyas-workshop-k6"], stdout=traffic_log, stderr=subprocess.STDOUT)
        try:
            workshop.run()
        finally:
            # Siempre restablece el simulador, incluso si falla una captura o aserción.
            try:
                workshop.faults()
            finally:
                subprocess.run(["docker", "stop", "dyas-workshop-k6"], check=False, stdout=subprocess.DEVNULL)
                try:
                    traffic.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    traffic.terminate()
                    traffic.wait(timeout=10)
                browser.close()
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir()) if p.is_file()}
    workshop.save("manifest", {"utc": now(), "environment": "GitHub-hosted isolated runner" if os.getenv("GITHUB_ACTIONS") else "local laboratory", "repository": os.getenv("GITHUB_REPOSITORY"), "run_id": os.getenv("GITHUB_RUN_ID"), "source_commit": os.getenv("GITHUB_SHA"), "complete": True, "files_sha256": files})


if __name__ == "__main__":
    main()
