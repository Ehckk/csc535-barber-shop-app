from .service import Service


class BarberService(Service):
    def __init__(self, service_id: int, name: str, price: float) -> None:
        self.price = price
        super().__init__(service_id, name)

    def __str__(self) -> str:
        return f"{self.name}: ${self.price}"