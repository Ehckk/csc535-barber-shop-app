from flask import session

from ..utils.email import send_mail


class User:
    def __init__(
        self, 
        user_id, 
        first_name, 
        last_name, 
        email, 
        role, 
        verified=False
    ):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.verified = verified

    def logout(self):
        session["user"] = None

    def send_reset_email(self):
        send_mail(
            subject="Password Reset", 
            recipients=[self.email], 
            body="""
                You have requested to reset your password.

                ADD LINK HERE
            """
        )

    def reset_password(self, new_password):
        
        return 
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}"
