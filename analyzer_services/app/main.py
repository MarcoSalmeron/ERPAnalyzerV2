from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzer_services.app.api.routes import router
import os
from fastapi.staticfiles import StaticFiles
import asyncio
import sys
from contextlib import asynccontextmanager
from agents.supervisor import team
from langgraph.checkpoint.memory import MemorySaver
import os
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---

    print("🚀 Inicializando LangGraph")
    memory = MemorySaver()
    app.state.oracle_graph = team.compile(checkpointer=memory)
    print("✅ LangGraph inicializado")
    yield
    # --- SHUTDOWN ---
    print("🛑 Cerrando aplicación")


services = FastAPI(
    title="Oracle Cloud InsightReadinesss API",
    description="API para el análisis de Oracle Cloud Readiness",
    version="1.0.0",
    lifespan=lifespan,
)

services.mount("/static/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# CORS: restrict to an explicit allow-list loaded from the environment.
# Configure CORS_ALLOWED_ORIGINS as a comma-separated list of origins.
# Defaults to the local Vite dev server. Never use "*" in production.
_cors_env = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
_allowed_origins = [o.strip() for o in _cors_env.split(",") if o.strip()]

services.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Incluir rutas de la API
services.include_router(router)


@services.get("/")
def read_root():
    return {"message": "API de Oracle Cloud Readiness"}
