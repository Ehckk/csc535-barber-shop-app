from flask import render_template
from ...queries import services
from ...utils.user import current_user
from .. import barber


@barber.route("/services/<int:service_id>", methods=["GET"])
def barber_service_details(service_id):
    user = current_user()

    barber_services = services.list_barber_services(user.id)
    current_service = services.retrieve_barber_service(
        barber_id=user.id, 
        service_id=service_id
    )

    return render_template(
        "barber/services_edit.html", 
        user=user,
        services=barber_services,
        current_service=current_service,
        current_service_id=service_id
    )
