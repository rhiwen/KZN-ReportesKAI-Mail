# app/utils/email_utils.py
import os
import ssl
import smtplib
from email.message import EmailMessage
import logging

EMAIL_SENDER    = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS", "").split(",")
SMTP_SERVER     = os.getenv("SMTP_SERVER")
SMTP_PORT       = int(os.getenv("SMTP_PORT", 465))
USE_STARTTLS    = os.getenv("SMTP_USE_STARTTLS", "false").lower() == "true"
SKIP_VERIFY     = os.getenv("SMTP_SKIP_VERIFY", "false").lower() == "true"


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if SKIP_VERIFY:
        logging.warning("⚠️  SSL verification & hostname check disabled for SMTP")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def send_report_email(subject: str, html_content: str, files: list[str]) -> None:
    # ---------- construir mensaje ----------
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER

    # limpia espacios y cadenas vacías
    recipients = [addr.strip() for addr in EMAIL_RECEIVERS if addr.strip()]
    msg["To"] = ", ".join(recipients)

    msg.set_content("Adjunto los reportes de Redmine.")
    msg.add_alternative(html_content, subtype="html")

    for file in files:
        with open(file, "rb") as f:
            data = f.read()
            name = os.path.basename(file)
            maintype, subtype = (
                ("text", "csv") if name.endswith(".csv")
                else ("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            )
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=name)

    ctx = _ssl_context()

    # ---------- enviar ----------
    if USE_STARTTLS:
        logging.info("📧 SMTP STARTTLS %s:%s", SMTP_SERVER, SMTP_PORT)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls(context=ctx)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg, to_addrs=recipients)   # <- lista explícita
    else:
        logging.info("📧 SMTP_SSL %s:%s", SMTP_SERVER, SMTP_PORT)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx, timeout=30) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg, to_addrs=recipients)   # <- lista explícita