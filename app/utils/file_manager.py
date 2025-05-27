# app/utils/file_manager.py
def data_to_html(data, report_title=None):
    """Convierte los datos del reporte directamente a HTML separando en dos secciones."""
    
    # Separar datos en dos grupos
    pendientes = [item for item in data if not item["is_validation"]]
    validacion = [item for item in data if item["is_validation"]]
    
    html = ""
    
    # Agregar título del reporte si se proporciona
    if report_title:
        html += f'<h2 style="color: #333; margin-bottom: 20px;">{report_title}</h2>'
    
    # Estilos para la tabla HTML --- Parece que Gmail no acepta estilos en bloque?
    html += '<style>'
    html += 'body { font-family: Arial, sans-serif; }'
    html += 'h3 { color: #333; margin-top: 25px; margin-bottom: 15px; }'
    html += 'table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }'
    html += 'th { background-color: #f2f2f2; padding: 8px; text-align: left; border: 1px solid #ddd; font-weight: bold; }'
    html += 'td { padding: 8px; border: 1px solid #ddd; }'
    html += 'tr:nth-child(even) { background-color: #f9f9f9; }'
    html += 'tr:hover { background-color: #f5f5f5; }'
    html += '</style>'
    
    # Columnas del reporte (con las nuevas columnas)
    columns = ['TAREA', 'PROYECTO', 'TÍTULO', 'PRIORIDAD', 'ESTADO', 'ASIGNADO A', 
            'FH CREACION', 'FH ACTUALIZACION', 'DÍAS DSD CREACIÓN', 'DÍAS DSD ÚLT. ACTUALIZACIÓN']
    
    def generate_table(data_section, section_title):
        section_html = f'<h3>{section_title}</h3>'
        section_html += '<table border="1" style="border-collapse: collapse; width: 100%; border: 1px solid #000;">'
        
        # Cabeceras
        section_html += '<tr>' + ''.join(f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{col}</th>' for col in columns) + '</tr>'
        
        # Datos
        for item in data_section:
            section_html += '<tr>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["task_id"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["project_name"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["title"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["priority"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["status"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["assigned_to"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["created_on"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["updated_on"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["days_since_creation"]}</td>'
            section_html += f'<th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #000;">{item["days_since_update"]}</td>'
            section_html += '</tr>'
        
        section_html += '</table>'
        return section_html
    
    # Generar sección "Pendientes / En curso"
    if pendientes:
        html += generate_table(pendientes, "Pendientes / En curso")
    
    # Generar sección "En Validación"
    if validacion:
        html += generate_table(validacion, "En Validación")
    
    # Si no hay datos en ninguna sección
    if not pendientes and not validacion:
        html += '<p>No se encontraron tareas tipo KAI</p>'
    
    return html