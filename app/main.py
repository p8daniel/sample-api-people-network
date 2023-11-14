""" main """
from typing import Dict

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app import VERSION
from app.api.api_v0.api import api_router
from app.api.exceptions_handler import GLOBAL_EXCEPTIONS_HANDLERS
from app.core.db_connection import close_neo4j_connection

app = FastAPI(
    title="Applicant-screener",
    description="API built for Neo4j with FastAPI",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    exception_handlers=GLOBAL_EXCEPTIONS_HANDLERS,
)
app.add_middleware(middleware_class=CorrelationIdMiddleware)
app.add_middleware(
    middleware_class=PrometheusMiddleware, app_name="application-screener", group_paths=True
)
app.add_route("/metrics", handle_metrics)


@app.on_event("shutdown")
async def close_connection() -> None:
    """Shutdown event"""
    await close_neo4j_connection()


@app.get("/ping")
async def ping() -> Dict[str, str]:
    """Ping function"""
    return {"status": "OK"}


app.include_router(api_router, prefix="/v0")
