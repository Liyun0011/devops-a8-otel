# Task 3 (Grade O): send traces AND logs over OTLP; logs carry the trace_id
# pip install opentelemetry-sdk opentelemetry-exporter-otlp
import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

ENDPOINT = "http://localhost:4317"
resource = Resource.create({"service.name": "a8-demo"})

# traces
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=ENDPOINT, insecure=True)))
trace.set_tracer_provider(tracer_provider)

# logs: Python's logging module -> OTel LoggingHandler -> OTLP
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=ENDPOINT, insecure=True)))
set_logger_provider(logger_provider)

log = logging.getLogger("a8.demo")
log.setLevel(logging.INFO)
log.addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))

tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout"):
    log.info("checkout started")                      # this log gets checkout's trace_id/span_id
    with tracer.start_as_current_span("charge-card"):
        log.warning("card charged: amount=299")       # same trace_id, charge-card's span_id
    print("trace_id:", format(trace.get_current_span().get_span_context().trace_id, "032x"))

tracer_provider.shutdown()
logger_provider.shutdown()
