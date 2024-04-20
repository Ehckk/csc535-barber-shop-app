from ..models.barber_service import BarberService


def get_services_table(barber_services: list[BarberService]):
    columns = ["Service", "Price"]
    services = list(map(lambda s: [s.name], barber_services))
    prices = list(map(lambda s: [f"${s.price}"], barber_services))
    data = list(zip(services, prices))
    print(data)
    return columns, data
