from flask import current_app, render_template, url_for, redirect, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from .. import auth
from ...queries.users import verify_email


@auth.route("/confirm_email/<user_id>/<token>")
def confirm_email(user_id, token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        s.loads(token, max_age=60)
        verify_email(user_id)
    except SignatureExpired:
        flash("Invaild Token", category="error")
        return redirect(url_for("auth.login")) 
    return render_template("confirm.html")
