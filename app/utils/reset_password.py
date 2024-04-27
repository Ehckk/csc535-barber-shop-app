from flask import Flask, request, render_template, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

def reset_password(token):
    @app.route("/reset_password/<token>", methods=["GET", "POST"], endpoint='auth.reset_password')
    def reset_password_route(token):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, max_age=3600)  
        except SignatureExpired:
            flash("Invalid or expired token.", category="error")
            return redirect(url_for("auth.request_reset"))  

        if request.method == "POST":
            new_password = request.form['new_password']
            flash('Your password has been updated.')
            return redirect(url_for('auth.login')) 

        return render_template('reset_password.html', token=token)

    return reset_password_route(token)

if __name__ == '__main__':
    app.run(debug=True)