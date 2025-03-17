from .car import Car, Ferrari, Porsche, Lambo, Enemy

class CarFactory:
    @staticmethod
    def create_car(car_type: str, **params) -> Car:
        if car_type == "ferrari":
            return Ferrari()
        elif car_type == "porsche":
            return Porsche()
        elif car_type == "lambo":
            return Lambo()
        elif car_type == "enemy":
            return Enemy(**params)
        else:
            raise ValueError(f"Unknown car type: {car_type}")