from flask import Flask, request, render_template, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash

from .. import auth
from ...queries.find_user_by_email import find_user_by_email
from ...queries.update_user_password import update_user_password
from ...utils.send_password_reset_email import send_password_reset_email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

@auth.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    if request.method == "POST":
        email = request.form['email']
        user = find_user_by_email(email)
        if user:
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = serializer.dumps(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            # Send the password reset email
            send_password_reset_email(email, reset_url)
            
            flash('Please check your email for the password reset link.')
            return redirect(url_for('auth.login'))
    return render_template('request_reset.html')

@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, max_age=3600)  # Token expires after 1 hour
    except SignatureExpired:
        flash("Invalid Token", category="error")
        return redirect(url_for("auth.login")) 

    if request.method == "POST":
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)
        update_user_password(email, hashed_password)
        flash('Your password has been updated.')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)