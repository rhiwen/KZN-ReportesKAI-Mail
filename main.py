# main.py
from pathlib import Path
from dotenv import load_dotenv
import logging
import os

# 1. Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# 2. Configurar logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 3. FastAPI + APScheduler
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.schemas import EmailRequest
from app.services.report_service import generate_report, get_file

app = FastAPI(title="Redmine KAI Tasks Reporter API")

# 4. Scheduler diario
report_time = os.getenv("REPORT_TIME", "10:00")
hour, minute = map(int, report_time.split(":"))
scheduler = BackgroundScheduler()


def daily_job() -> None:
    """Genera y envía el reporte automáticamente (sin BackgroundTasks)."""
    logging.info("⏰ Iniciando job programado diario para tareas KAI")
    try:
        generate_report(send_email=True, background_tasks=None)
        logging.info("✅ Job diario de tareas KAI completado con éxito")
    except Exception as exc:
        logging.exception("❌ Job diario falló: %s", exc)


scheduler.add_job(
    daily_job,
    CronTrigger(hour=hour, minute=minute, timezone="America/Argentina/Buenos_Aires"),
    id="daily_report_kai",
)
scheduler.start()

# 5. Endpoints
@app.post("/generar-reporte-kai", response_class=HTMLResponse)
def generar_reporte(request: EmailRequest, background_tasks: BackgroundTasks):
    logging.info("📥 Solicitud manual de reporte de tareas KAI recibida")
    return generate_report(request.send_email, background_tasks)


@app.get("/descargar/{filename}")
def descargar_archivo(filename: str):
    logging.info("📤 Descarga solicitada: %s", filename)
    path = get_file(filename)
    return FileResponse(path) if path else {"error": "Archivo no encontrado"}

# Nuevo endpoint - web
@app.get("/", response_class=HTMLResponse)
def vista_reporte():
    return generate_report(send_email=False)