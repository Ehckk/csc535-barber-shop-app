from flask_mail import Message, Mail
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer


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


def send_verification_email(user_id, email: str):
    secret_key = current_app.config['SECRET_KEY']
    s = URLSafeTimedSerializer(secret_key)
    token = s.dumps(email)
    send_mail(
		"Verify Your Email Address", 
		recipients=[email],
		body=f"""
			Use the following link to verify your email address:

			{url_for('auth.confirm_email', user_id=user_id, token=token, _external=True)}
		"""
	)