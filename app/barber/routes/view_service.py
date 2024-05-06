from flask import flash, redirect, render_template
from ...utils.decorators import has_role
from ...queries import services
from ...utils.user import current_user
from .forms.service import ServiceForm 
from .. import barber


@barber.route("/services/<int:service_id>", methods=["GET", "POST"])
@has_role("Barber")
def barber_service_details(service_id):
    user = current_user()

    barber_services = services.list_barber_services(user.id)
    current_service = services.retrieve_barber_service(
        barber_id=user.id, 
        service_id=service_id
    )
    if not current_service:
        url_name = "barber.barber_services"
        return redirect(url_name)

    form = ServiceForm()
    delattr(form, "name")
    if form.validate_on_submit():
        new_price = form.price.data
        new_description = form.description.data
        current_service = services.update_barber_service(user.id, service_id, new_price, new_description)
        flash(f"{current_service.name} service updated!", category="success")

    form.price.data = current_service.price
    form.price.description = current_service.description
    return render_template(
        "barber/services_details.html", 
        user=user,
        services=barber_services,
        current_service=current_service,
        current_service_id=service_id,
        form=form
    )
