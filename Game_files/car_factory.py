from .car import Car, Ferrari, Porsche, Lambo

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

class Ferrari(Car):
    def drive(self):
        return "Driving a Ferrari"

class Porsche(Car):
    def drive(self):
        return "Driving a Porsche"

class Lambo(Car):
    def drive(self):
        return "Driving a Lambo"