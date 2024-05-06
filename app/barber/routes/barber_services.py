from flask import flash, redirect, render_template

from ...utils.decorators import has_role
from ...utils.user import current_user
from ...queries import services
from .forms.service import ServiceForm
from .. import barber


@barber.route("/services", methods=["GET", "POST"])
@has_role("Barber")
def barber_services():
    user = current_user()
    barber_services = services.list_barber_services(user.id)
    
    form = ServiceForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        try:
            new_service = services.add_barber_service(user.id, name, price, description)
            url_name = "barber.barber_service_details"
            return redirect(url_name, service_id=new_service.id)
        except AssertionError as error:
            flash(error, category="error")

    return render_template(
        "barber/services_add.html",
        user=user,
        services=barber_services,
        form=form
    )