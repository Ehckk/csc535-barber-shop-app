from flask_mail import Message, Mail
from flask import current_app


def send_mail(subject: str, recipients: list[str], body: str):
    mail = Mail(current_app)
    message = Message(
        subject=f"Barber App: {subject}", 
        sender="noreply@barberapp.com",
        body=body
    )
    for recipient in recipients:
        message.add_recipient(recipient)
    mail.send(message)