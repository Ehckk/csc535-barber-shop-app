from flask import flash, redirect, url_for
from ...utils.decorators import has_role
from ...queries import services, appointments
from ...utils.user import current_user
from .. import barber


@barber.route("/services/<int:service_id>/remove", methods=["GET"])
@has_role("Barber")
def barber_service_remove(service_id):
    user = current_user()
    current_service = services.retrieve_barber_service(
        barber_id=user.id, 
        service_id=service_id
    )
    if not current_service:
        flash("Service not found!", category="error")
    else:
        appointments.cancel_service_appointments(user.id, service_id)
        services.remove_barber_service(user.id, service_id)
        flash(f"'{current_service.name}' removed!", category="success")
    url_name = "barber.barber_services"
    return redirect(url_for(url_name))
