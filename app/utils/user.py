from flask import session
from ..queries.users import retrieve_user
from ..queries.appointments import cancel_prev_unbooked


def current_user():
    cancel_prev_unbooked()
    if not session["user"]:
        return None
    id = int(session["user"]["id"])
    # Validate Appointment
    return retrieve_user(id) 
    