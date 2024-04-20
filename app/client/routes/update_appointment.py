from datetime import date
from flask import redirect, render_template, flash, url_for

from ...utils.decorators import has_role
from ...utils.user import current_user
from ...queries import services, appointments
from .. import client
from .forms.request import EditServicesForm, get_service_choices


@client.route("/<int:appt_id>/edit", methods=["GET", "POST"])
@has_role("Client")
def edit_appointment(appt_id: int):
    user = current_user()
    
    appointment = appointments.retrieve_appointment(appointment_id=appt_id)
    appointment_services = services.retrieve_appointment_services(appointment_id=appt_id)
    appointment_service_ids = list(map(lambda service: service.id, appointment_services))
    client_appointments = appointments.list_client_appointments(user.id)
    requested_appointments = appointments.list_client_appointments(user.id, is_booked=False)

    form = EditServicesForm()
    form.services.choices = get_service_choices(appointment.barber.id)
    if form.validate_on_submit():
        new_appointment_services = form.services.data
        if len(appointment_services) == 0:
            message = "Select at least one service!"
            flash(message, category="error")
        else:
            new_appointment_service_ids = list(map(int, new_appointment_services))
            new_service_ids = list(set(new_appointment_service_ids) - set(appointment_service_ids))
            services.update_appointment_services(
                appointment.id, 
                service_ids=new_appointment_service_ids,
                new_service_ids=new_service_ids
            )
            flash("Your changes have been saved!", category="success")
            return redirect(url_for("client.appointment_details", appt_id=appt_id))

    form.services.data = list(map(str, appointment_service_ids))

    return render_template(
        'client/edit_appointment.html',
        user=user,
        form=form,
        appointment=appointment,
        appointments=client_appointments,
        requested_appointments=requested_appointments
    )