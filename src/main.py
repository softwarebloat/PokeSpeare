from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

from pokespeare.routers import shakespearean_pokemon

app = FastAPI(
    title="PokeSpeare",
    description="REST API that given a Pokemon name return its Shakespearean description",
)

trace.set_tracer_provider(TracerProvider())

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:55681", insecure=True))
)
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace)

app.include_router(shakespearean_pokemon.router)
