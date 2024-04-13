from flask import flash, redirect, render_template, url_for
from ...utils.user import current_user
from ...queries import schedules, users
from .. import client
from .forms.request import RequestForm


@client.route("/", methods=["GET", "POST"])
def client_home():
    user = current_user()
    form = RequestForm()
    if form.validate_on_submit():
        barber_id = form.barber.data
        booked_date = form.date.data
        if not barber_id:        
            flash("Select a barber!", category="error")
        else:
            barber = users.retrieve_user(barber_id)
            if schedules.is_available_for_date(barber_id, booked_date):
                return redirect(url_for(
                    "client.request_appointment", 
                    barber_id=barber.id,
                    booked_date=booked_date.strftime("%Y%m%d")
                ))
            message = f"{barber.display_name()} is unavailable on {booked_date}"
            flash(message, category="error")
    return render_template(
        'client/create_appointment.html',
        user=user,
        form=form
    )
