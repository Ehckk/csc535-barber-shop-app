from flask import session


class User:
    def __init__(self, id, first_name, last_name, email, verified=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.verified = verified

    def logout(self):
        session["user"] = None

    def reset_password(self):
        return