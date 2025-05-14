# app/utils/file_manager.py
import os
import csv
from openpyxl import Workbook, load_workbook

os.makedirs("data", exist_ok=True)

def save_files(data, timestamp):
    csv_file = f"data/reporte_{timestamp}.csv"
    xlsx_file = f"data/reporte_{timestamp}.xlsx"

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Nombre Proyecto', 'Total Issues', 'Issues Abiertos', 'Issues Cerrados',
            'Issues Cerrados Este Mes', 'Issues Abiertos Este Mes',
            'Horas Dedicadas', 'Avance (%)', 'Versión'
        ])
        for d in data:
            writer.writerow([
                d['project_name'], d['total_issues'], d['total_open_issues'],
                d['total_closed_issues'], d['issues_closed_this_month'],
                d['issues_opened_this_month'], f"{d['total_hours']:.2f}",
                d['progress_percentage'], ", ".join(d['versions'])
            ])

    workbook = Workbook()
    sheet = workbook.active
    sheet.append([
        'Nombre Proyecto', 'Total Issues', 'Issues Abiertos', 'Issues Cerrados',
        'Issues Cerrados Este Mes', 'Issues Abiertos Este Mes',
        'Horas Dedicadas', 'Avance (%)', 'Versión'
    ])
    for d in data:
        sheet.append([
            d['project_name'], d['total_issues'], d['total_open_issues'],
            d['total_closed_issues'], d['issues_closed_this_month'],
            d['issues_opened_this_month'], f"{d['total_hours']:.2f}",
            d['progress_percentage'], ", ".join(d['versions'])
        ])
    workbook.save(xlsx_file)

    return csv_file, xlsx_file

def xlsx_to_html(xlsx_path):
    wb = load_workbook(xlsx_path)
    sheet = wb.active
    html = '<table border="1">'
    for row in sheet.iter_rows(values_only=True):
        html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    html += '</table>'
    return html