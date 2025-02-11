from car import Car, Ferrari, Porsche, Lambo

class CarFactory:
    @staticmethod
    def create_car(car_type: str) -> Car:
        if car_type == "ferrari":
            return Ferrari()
        elif car_type == "porsche":
            return Porsche()
        elif car_type == "lambo":
            return Lambo()
        else:
            raise ValueError(f"Unknown car type: {car_type}")