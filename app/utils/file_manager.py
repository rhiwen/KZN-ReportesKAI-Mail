# app/utils/file_manager.py
def data_to_html(data):
    """Convierte los datos del reporte directamente a HTML sin crear archivos intermedios."""
    html = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    
    # Estilos para la tabla HTML
    html += '<style>'
    html += 'th { background-color: #f2f2f2; padding: 8px; text-align: left; }'
    html += 'td { padding: 8px; }'
    html += 'tr:nth-child(even) { background-color: #f9f9f9; }'
    html += '</style>'
    
    # Columnas del reporte
    columns = ['TAREA', 'PROYECTO', 'TÍTULO', 'ESTADO', 'ASIGNADO A', 
            'FH CREACION', 'FH ACTUALIZACION']
    
    # Cabeceras con <th>
    html += '<tr>' + ''.join(f'<th>{col}</th>' for col in columns) + '</tr>'
    
    # Datos con <td>
    for item in data:
        html += '<tr>'
        html += f'<td>{item["task_id"]}</td>'
        html += f'<td>{item["project_name"]}</td>'
        html += f'<td>{item["title"]}</td>'
        html += f'<td>{item["status"]}</td>'
        html += f'<td>{item["assigned_to"]}</td>'
        html += f'<td>{item["created_on"]}</td>'
        html += f'<td>{item["updated_on"]}</td>'
        html += '</tr>'
    
    html += '</table>'
    return html