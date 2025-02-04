from car import Car, ferrari, porsche, lambo

class CarFactory:
    @staticmethod
    def create_car(car_type: str) -> Car:
        if car_type == "ferrari":
            return ferrari()
        elif car_type == "porsche":
            return porsche()
        elif car_type == "lambo":
            return lambo()
        else:
            raise ValueError(f"Unknown car type: {car_type}")