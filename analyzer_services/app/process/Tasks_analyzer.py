
from analyzer_services.app.process.ConnectionManager import manager
from langchain_core.messages import HumanMessage
from agents.supervisor import team


from common.common_utl import get_embeddings_model
import asyncio
import logging
import time

# ===============================
# LOGGING
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
    

    
##memory = MemorySaver()
##oracle_app = team.compile(checkpointer=checkpointer)
get_embeddings_model()

# --- Función de Ejecución del Grafo (Lógica Pesada) ---
async def run_oracle_analysis(thread_id: str, query: str,oracle_app):
    

    await asyncio.sleep(10) # Pausa para mostrar el monitor visual
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [HumanMessage(content=query)]}
    
    try:
        step_agent=1
        # 1. Notificar al Monitor: Supervisor Iniciado (Paso 1 en imagen)
        await manager.send_update(thread_id, {
            "step": step_agent,
            "agent": "supervisor",
            "status": "active",
            "log": "Iniciando orquestación..."
        })
        
        async for event in oracle_app.astream(inputs, config=config, stream_mode="values"):
            try:
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    
                    # Detectamos qué agente está trabajando
                    if hasattr(last_msg, 'name') and last_msg.name:
                        agent_name = last_msg.name.lower()
                        logger.info(f"Detección de agente: {agent_name}")
                        
                        # Mapeo  (1.Supervisor, 2.Investigador, 3.Analista, 4.Redactor)
                        steps = {"transfer_back_to_supervisor": 1, "transfer_to_investigador": 2, "transfer_to_analista": 3, "transfer_to_redactor": 4}
                        current_step = steps.get(agent_name, 1)

                        # 2. ENVIAR AL WEBSOCKET
                        await manager.send_update(thread_id, {
                            "step": current_step,
                            "agent": agent_name,
                            "status": "active",
                            "content": last_msg.content, # El texto que sale en el chat central
                            "log": f"Ejecutando tareas de {agent_name}..." # Texto pequeño del monitor
                        })
            except Exception as e:
                print(f"Rate limit exceded. Pausando tareas para evitar bloqueo...{e}")
                if "429" in str(e):
                    logger.error(f"Rate limit exceded. Pausando tareas para evitar bloqueo...")
                    time.sleep(2)
                else:
                    raise e
                
            # 3. Notificación Final: El Redactor terminó el PDF
        filename = f"reporte_{thread_id}.pdf"
        await manager.send_update(thread_id, {
                "step": 4,
                "agent": "redactor",
                "status": "completed",
                "pdf_ready": True,
                "pdf_url": f"/static/reports/{filename}"
            })
        await  manager.close_connection(thread_id)
            
    except Exception as e:
        logger.error(f"Error en el flujo de trabajo: {str(e)}")
        await manager.send_update(thread_id, {"error": str(e)})