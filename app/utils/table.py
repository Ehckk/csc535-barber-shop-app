from ..models.barber_service import BarberService


def get_services_table(barber_services: list[BarberService]):
    columns = ["Service", "Price"]
    data = {
        "Service": [map(lambda service: [service.name], barber_services)],
        "Price": [map(lambda service: [f"${service.price}"], barber_services)]
    }
    return columns, data
