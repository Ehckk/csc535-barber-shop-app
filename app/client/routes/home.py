from flask import render_template
from ...utils.user import current_user
from .. import client


@client.route("/", methods=["GET", "POST"])
def client_home():
    user = current_user()
    return render_template('home.html', user=user)
