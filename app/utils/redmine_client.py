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

# ["8-QA Procesos", "9-Realizado"]
def safe_issues(project_id):
    """Devuelve issues tipo 'KAI' excepto los que tienen estado 'QA Procesos' o 'Realizado', ordenados por fecha de creación ascendente."""
    try:
        issues = redmine.issue.filter(project_id=project_id)
        filtered = [
            i for i in issues
            if any(
                cf.name == "Tipo de tarea" and cf.value == "KAI"
                for cf in getattr(i, "custom_fields", [])
            )
            and i.status.name not in ["8-QA Procesos", "9-Realizado"]
        ]
        return sorted(filtered, key=lambda i: i.created_on)
    except (ForbiddenError, ResourceNotFoundError):
        return []

def _safe_assigned_to(issue):
    """Nombre del asignado o 'Sin asignar'."""
    try:
        return issue.assigned_to.name
    except (AttributeError, ResourceAttrError):
        return "Sin asignar"


def _format_date(date_obj):
    """Formatea fecha como DD/MM/YYYY."""
    if date_obj:
        return date_obj.strftime("%d/%m/%Y")
    return "N/A"


def _calculate_days_since(date_obj):
    """Calcula días transcurridos desde una fecha."""
    if date_obj:
        today = datetime.now().date()
        if hasattr(date_obj, 'date'):
            date_only = date_obj.date()
        else:
            date_only = date_obj
        return (today - date_only).days
    return 0


# ───── Procesamiento principal ─────────────────────────
def process_projects(projects):
    data = []
    
    for project in projects:
        issues = safe_issues(project.id)
        
        for issue in issues:
            created_on_date = getattr(issue, "created_on", None)
            updated_on_date = getattr(issue, "updated_on", None)
            
            # Por cada issue tipo KAI, creamos un registro en el formato solicitado
            data.append({
                "task_id": f"#{issue.id}",
                "project_name": project.name,
                "title": issue.subject,
                "priority": issue.priority.name,
                "status": issue.status.name,
                "assigned_to": _safe_assigned_to(issue),
                "created_on": _format_date(created_on_date),
                "updated_on": _format_date(updated_on_date),
                "created_on_datetime": created_on_date,
                "days_since_creation": _calculate_days_since(created_on_date),
                "days_since_update": _calculate_days_since(updated_on_date),
                "is_validation": issue.status.name == "7-Validar Cruzado"
            })
    
    # Ordenar por fecha de creación
    return sorted(data, key=lambda item: item["created_on_datetime"] or datetime.min)