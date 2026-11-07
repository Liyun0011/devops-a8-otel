# DevOps Assignment 8: OpenTelemetry Observability

Student: 劉芳瑜 (B11309036)

This repo has the full source code for the A8 report. It instruments a Python app with the OpenTelemetry SDK, sends telemetry over OTLP to a Dockerized Collector, and shows log–trace correlation.

| File | Task | What it does |
|---|---|---|
| `task1_console.py` | Task 1 (A) | Parent span `checkout` with child span `charge-card`, printed by `ConsoleSpanExporter` |
| `task2_otlp.py` | Task 2 (E) | Sends the same spans over OTLP/gRPC to `localhost:4317` |
| `otel-collector-config.yaml` | Task 2 (E) | Pipeline: `otlp` receiver → `batch` processor → `debug` + `file` exporters |
| `task3_traces_and_logs.py` | Task 3 (O) | Sends traces **and** logs over OTLP; logs written inside spans carry the trace ID and span ID |
| `otel-collector-config-task3.yaml` | Task 3 (O) | Two pipelines (traces, logs), `resource/env` processor, separate output files |

## Environment

- Windows 11, VS Code, Python 3.13
- `opentelemetry-sdk` 1.45.2 and `opentelemetry-exporter-otlp` 1.45.2
- Docker Desktop 4.98.0 (WSL 2)
- `otel/opentelemetry-collector:0.164.0`

## How to run (PowerShell)

```powershell
py -m pip install opentelemetry-sdk opentelemetry-exporter-otlp

# Task 1
py task1_console.py

# Task 2: terminal 1
mkdir out
docker run --rm --name otelcol -p 4317:4317 -p 4318:4318 `
  -v "${PWD}\otel-collector-config.yaml:/etc/otelcol/config.yaml" `
  -v "${PWD}\out:/out" otel/opentelemetry-collector:0.164.0
# Task 2: terminal 2
py task2_otlp.py

# Task 3: restart the Collector with otel-collector-config-task3.yaml, then:
py task3_traces_and_logs.py
```

On Windows, `chmod 777 out` is not needed because Docker Desktop bind mounts are writable by default.

Output files are written to `out/`: `telemetry.json` (Task 2), and `traces.json` and `logs.json` (Task 3).
