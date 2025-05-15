## Proyecto REDMINE -> Mails KAI
* Original por: Zeron
* Adaptación a tickets KAI por: Rhiwen
* Fecha: 2025/04/21
___
Una solución automatizada basada en FastAPI para generar reportes de tareas KAI en Redmine y enviarlos por correo.

## 🚀 Características

- Conexión con Redmine vía API
- Filtra específicamente tareas tipo KAI en estado abierto
- Excluye tareas en estados "8-QA Procesos" y "9-Realizado"
- Generación de HTML directo para el cuerpo del email
- Envío automático por email programado diariamente
- Interfaz web simple para visualización de reportes

## 📦 Requisitos

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## ⚙️ Variables de Entorno

Puede usar un archivo `.env` o definir en su entorno:

```env
REDMINE_URL=https://proyectos.kaizen2b.net
REDMINE_API_KEY=API_KEY_AQUI
EMAIL_SENDER=prueba123@kaizen2b.net
EMAIL_PASSWORD=CLAVE_CORREO
EMAIL_RECEIVERS=correo1@ejemplo.com,correo2@ejemplo.com
SMTP_SERVER=smtp.servidor.com
SMTP_PORT=465
REPORT_TIME=10:00   # Hora de envío automático (formato 24h)
```

## 🛠 Uso

Levantar el servidor:

```bash
uvicorn main:app --reload
```

Acceder a:
- `GET /`: Vista web del reporte actual
- `POST /generar-reporte-kai`: Genera el reporte y lo envía por email (opcional)
- `GET /descargar/{filename}`: Descarga el archivo generado

### Ejemplo de request con `curl`:

```bash
curl -X POST http://localhost:8000/generar-reporte-kai -H "Content-Type: application/json" -d '{"send_email": true}'
```

### ESTRUCTURA
```text
redmine_reporter_fastapi/
├── app/
│   ├── __init__.py
│   ├── schemas.py                 # Modelos Pydantic
│   ├── services/
│   │   └── report_service.py      # Lógica principal de reporte (simplificada)
│   ├── utils/
│   │   ├── redmine_client.py      # Acceso a Redmine y filtrado KAI
│   │   ├── file_manager.py        # Generación directa de HTML
│   │   └── email_utils.py         # Envío de correo electrónico (sin adjuntos)
├── main.py                        # FastAPI App y rutas + scheduler diario
├── requirements.txt
├── README.md
```
## 📧 Envío de Correos

El sistema envía el reporte directamente en el cuerpo HTML del correo (sin archivos adjuntos). El envío se realiza:
- Manualmente mediante el endpoint `/generar-reporte-kai`
- Automáticamente todos los días a la hora definida en `REPORT_TIME`

### .env

* REPORT_TIME=10:00   # ← poné la hora deseada, formato 24 h
---

**Desarrollado por:** [Kaizen2B](https://kaizen2b.com)

