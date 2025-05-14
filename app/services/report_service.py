# app/services/report_service.py
import logging
from datetime import datetime
from typing import Optional

from fastapi import BackgroundTasks
from redminelib.exceptions import ForbiddenError, AuthError

from app.utils.redmine_client import get_projects, process_projects
from app.utils.file_manager import save_files, xlsx_to_html
from app.utils.email_utils import send_report_email


def generate_report(send_email: bool = True, background_tasks: Optional[BackgroundTasks] = None):
    """Genera CSV/XLSX, devuelve HTML y opcionalmente envía email.
    Si `background_tasks` es None (ejecución del scheduler), el correo se envía inmediatamente.
    """
    logging.info("🔄 Generando reporte…")

    try:
        logging.info("📡 Obteniendo proyectos…")
        projects = get_projects()
        data = process_projects(projects)
        logging.info("✅ Proyectos procesados: %s", len(data))
    except (ForbiddenError, AuthError) as e:
        logging.error("🚫 Permisos insuficientes: %s", e)
        raise
    except Exception as e:
        logging.exception("💥 Error inesperado: %s", e)
        raise

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file, xlsx_file = save_files(data, timestamp)
    html_content = xlsx_to_html(xlsx_file)

    if send_email:
        subject = f"Reporte de Redmine {timestamp}"
        if background_tasks is not None:
            logging.info("📨 Programando envío de email (BackgroundTasks)…")
            background_tasks.add_task(send_report_email, subject, html_content, [csv_file, xlsx_file])
        else:
            logging.info("📨 Enviando email inmediatamente (scheduler)…")
            send_report_email(subject, html_content, [csv_file, xlsx_file])

    logging.info("🎉 Reporte generado correctamente")
    return html_content

def get_file(filename: str):
    """Devuelve la ruta absoluta del archivo en /data o None si no existe."""
    import os
    path = os.path.join("data", filename)
    return path if os.path.exists(path) else None
