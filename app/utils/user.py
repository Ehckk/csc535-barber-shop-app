from flask import session
from ..models.user import User
from ..queries.users import retrieve_user


def current_user():
    if not session["user"]:
        return None
    id = int(session["user"]["id"])
    return retrieve_user(id) 
    