from flask import redirect, render_template, render_template, url_for

from .. import auth
from .forms.register import Registration
from ...utils.email import send_mail
from ...queries.users import create_user

@auth.route("/register", methods=["GET","POST"])
def register():
	form = Registration()
	if form.validate_on_submit():
		first_name = form.first_name.data
		last_name = form.last_name.data
		email = form.email.data
		password = form.password.data
		role = form.role.data

		user_id = create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
			role=role
		)
		# Verify Emails
		return redirect(url_for("auth.verify", user_id=user_id))
	return render_template("register.html", form=form)