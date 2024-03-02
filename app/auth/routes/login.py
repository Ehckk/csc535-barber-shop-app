from .. import auth
from .forms.login import LoginForm


@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    return "Login"
