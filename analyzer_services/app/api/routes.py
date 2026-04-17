import asyncio
import re
import uuid

from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect

from analyzer_services.app.models.schemas import AnalysisRequest
from analyzer_services.app.process.ConnectionManager import manager
from analyzer_services.app.process.Tasks_analyzer import run_oracle_analysis
from common.common_utl import es_consulta_valida_oracle

router = APIRouter(prefix="/impact", tags=["Impact"])

# Thread IDs we generate match this pattern. We only accept WebSocket
# connections for thread IDs of the exact shape produced by the analyze
# endpoint to prevent clients from subscribing to arbitrary keys.
_THREAD_ID_RE = re.compile(r"^oracle_project_[a-f0-9]{8}$")


@router.post("/analyze")
async def start_analysis(request: AnalysisRequest, http_request: Request):
    # Domain guardrail: reject prompts that are clearly outside the Oracle
    # Cloud Readiness scope before spending LLM credits on them.
    if not es_consulta_valida_oracle(request.query):
        raise HTTPException(
            status_code=400,
            detail=(
                "La consulta debe estar relacionada con Oracle Cloud "
                "Readiness (incluir una versión como 24D/25A o palabras "
                "clave del dominio)."
            ),
        )

    oracle_app = http_request.app.state.oracle_graph

    thread_id = f"oracle_project_{uuid.uuid4().hex[:8]}"

    # Lanzar el proceso de los 4 agentes sin bloquear la API
    asyncio.create_task(
        run_oracle_analysis(thread_id, request.query, oracle_app)
    )

    return {"thread_id": thread_id, "message": "Análisis en curso..."}


@router.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    # Validate the thread_id shape before accepting, so callers can't
    # subscribe to arbitrary/malformed keys or attempt to hijack an
    # existing session by racing on a well-known id.
    if not _THREAD_ID_RE.match(thread_id):
        await websocket.close(code=1008)  # policy violation
        return
    if not await manager.connect(websocket, thread_id):
        return
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(thread_id)
