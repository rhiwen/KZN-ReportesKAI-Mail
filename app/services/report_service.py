# app/services/report_service.py
import logging
from datetime import datetime
from typing import Optional

from fastapi import BackgroundTasks
from redminelib.exceptions import ForbiddenError, AuthError

from app.utils.redmine_client import get_projects, process_projects
from app.utils.file_manager import data_to_html
from app.utils.email_utils import send_report_email


def generate_report(send_email: bool = True, background_tasks: Optional[BackgroundTasks] = None):
    """Genera HTML del reporte y opcionalmente envía email.
    Si `background_tasks` es None (ejecución del scheduler), el correo se envía inmediatamente.
    """
    logging.info("🔄 Generando reporte de tareas KAI…")

    try:
        logging.info("📡 Obteniendo proyectos…")
        projects = get_projects()
        data = process_projects(projects)
        logging.info("✅ Tareas tipo KAI procesadas: %s", len(data))
        
        if not data:
            logging.warning("⚠️ No se encontraron tareas tipo KAI")
            return "<p>No se encontraron tareas tipo KAI</p>"
            
    except (ForbiddenError, AuthError) as e:
        logging.error("🚫 Permisos insuficientes: %s", e)
        raise
    except Exception as e:
        logging.exception("💥 Error inesperado: %s", e)
        raise

    # Generar título del reporte
    timestamp = datetime.now().strftime("%Y-%m-%d - %H%M")
    report_title = f"KZN KAI - Reporte Tickets de KAI Abiertos al {timestamp}"
    
    # Convertir datos directamente a HTML con título
    html_content = data_to_html(data, report_title)

    if send_email:
        subject = report_title
        
        if background_tasks is not None:
            logging.info("📨 Programando envío de email (BackgroundTasks)…")
            background_tasks.add_task(send_report_email, subject, html_content)
        else:
            logging.info("📨 Enviando email inmediatamente (scheduler)…")
            send_report_email(subject, html_content)

    logging.info("🎉 Reporte de tareas KAI generado correctamente")
    return html_content


def get_file(filename: str):
    """Esta función ya no es necesaria sin la generación de archivos,
    pero se mantiene por compatibilidad con las rutas existentes."""
    import os
    path = os.path.join("data", filename)
    return path if os.path.exists(path) else None