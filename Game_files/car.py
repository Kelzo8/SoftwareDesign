from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def drive(self):
        pass
    @abstractmethod
    def get_image(self):
        pass

class Ferrari(Car):
    def drive(self):
        return "Driving a ferrari"
    def get_image(self):
        return "assets/ferrari.png"

class Porsche(Car):
    def drive(self):
        return "Driving an porsche"
    def get_image(self):
        return "assets/porsche.png"

class Lambo(Car):
    def drive(self):
        return "Driving a lambo"
    def get_image(self):
        return "assets/lambo.png"