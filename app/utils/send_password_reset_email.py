from flask_mail import Message, Mail
from flask import current_app

def send_password_reset_email(recipient_email: str, reset_link: str):
    mail = Mail(current_app)
    message = Message(
        subject="Password Reset Request", 
        sender="noreply@barberapp.com",
        recipients=[recipient_email],
        body=f"""
            You have requested a password reset for your account.
            
            Please follow the link below to reset your password:
            {reset_link}
            
            If you did not request this, please ignore this email.
        """
    )
    mail.send(message)
