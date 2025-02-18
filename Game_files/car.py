from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

class Ferrari(Car):
    def drive(self):
        return "Driving a ferrari"

class Porsche(Car):
    def drive(self):
        return "Driving an porsche"

class Lambo(Car):
    def drive(self):
        return "Driving a lambo"