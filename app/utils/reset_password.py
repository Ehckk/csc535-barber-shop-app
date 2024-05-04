from flask import Flask, request, render_template, redirect, url_for, flash
from ..queries.update_user_password import update_user_password

app = Flask(__name__)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if new_password:
            if update_user_password(new_password):
                flash('Your password has been updated.')
                return redirect(url_for('home'))  
            else:
                flash("Failed to update password.", category="error")
        else:
            flash("Please enter a new password.", category="error")
    
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
