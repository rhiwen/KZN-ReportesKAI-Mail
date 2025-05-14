# app/utils/redmine_client.py
import os
from datetime import datetime
from redminelib import Redmine
from redminelib.exceptions import (
    ForbiddenError,
    ResourceNotFoundError,
    ResourceBadMethodError,
    ResourceAttrError,
)

REDMINE_URL = os.getenv("REDMINE_URL")
API_KEY = os.getenv("REDMINE_API_KEY")

if not REDMINE_URL or not API_KEY:
    raise RuntimeError("⚠️  REDMINE_URL o REDMINE_API_KEY no configurados en .env")

redmine = Redmine(REDMINE_URL.rstrip("/"), key=API_KEY)


# ───── Helpers ──────────────────────────────────────────
def get_projects():
    """Devuelve los proyectos accesibles; fallback si el servidor no soporta membership='*'."""
    try:
        return redmine.project.filter(membership="*")
    except ResourceBadMethodError:
        return redmine.project.all()


def safe_issues(project_id, start_date, end_date):
    """Devuelve issues dentro de rango o lista vacía si no hay permiso."""
    try:
        issues = redmine.issue.filter(project_id=project_id, status_id="*")
        return [i for i in issues if start_date <= i.updated_on <= end_date]
    except (ForbiddenError, ResourceNotFoundError):
        return []


def _safe_version(issue):
    """Nombre de versión o 'Sin versión'."""
    try:
        return issue.fixed_version.name
    except (AttributeError, ResourceAttrError):
        return "Sin versión"


# ───── Procesamiento principal ─────────────────────────
def process_projects(projects):
    today = datetime.today()
    start_of_month = today.replace(day=1)
    end_of_month = today

    data = []
    for project in projects:
        rec = {
            "project_name": project.name,
            "total_issues": 0,
            "total_open_issues": 0,
            "total_closed_issues": 0,
            "issues_closed_this_month": 0,
            "issues_opened_this_month": 0,
            "total_hours": 0,
            "versions": set(),
        }

        for issue in safe_issues(project.id, start_of_month, end_of_month):
            rec["total_issues"] += 1

            if issue.status.id in (1, 2, 8):  # abiertos
                rec["total_open_issues"] += 1
                if start_of_month <= issue.created_on <= end_of_month:
                    rec["issues_opened_this_month"] += 1
            else:                             # cerrados
                rec["total_closed_issues"] += 1
                if start_of_month <= issue.updated_on <= end_of_month:
                    rec["issues_closed_this_month"] += 1

            # horas imputadas
            for entry in redmine.time_entry.filter(issue_id=issue.id):
                rec["total_hours"] += round(entry.hours, 2)

            # versión segura
            rec["versions"].add(_safe_version(issue))

        if rec["total_issues"] == 0:
            continue  # sin datos útiles (o sin permisos)

        rec["progress_percentage"] = (
            f"{(rec['total_closed_issues'] / rec['total_issues'] * 100):.2f}%"
        )
        data.append(rec)

    return data