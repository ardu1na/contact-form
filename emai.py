import smtplib
import os
import django
from email.message import EmailMessage
from decouple import config

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

from vimacon.models import Message

def send_test_email():

    #mails de recibidos
    solicitudes_recibidas = Message.objects.filter(
        reenviado=False,
    )

    for solicitud in solicitudes_recibidas:
        subject = 'NUEVO MENSAJE desde el SITIO DE VIMACON'
        
        body = (f"¡Hola! "
                f"Ha llegado el siguiente mensaje el {solicitud.fecha}:"
		f"REMITENTE: {solicitud.nombre} - {solicitud.email}"
		f"ASUNTO: {solicitud.asunto}"
		f"MENSAJE: {solicitud.texto)"
        from_email = 'no-responder@vimacon.com'
        to_email = 'hola@vimacon.com'

        # Create the email message
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # SMTP server configuration
        smtp_server = 'smtp.ionos.es'
        smtp_port = 587
        smtp_username = 'no-responder@vimacon.com'
        smtp_password = 'meb@2025'

        try:
            # Send the email
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            print(f"Email {solicitud.id} enviado exitosamente.")

            # Update the request status
            solicitud.reenviado = True
            solicitud.save()

        except Exception as e:
            print(f"Se produjo un error al enviar el email {solicitud.id}: {e}")


if __name__ == "__main__":
    send_test_email()
