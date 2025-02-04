from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

class ferrari(Car):
    def drive(self):
        return "Driving a ferrari"

class porsche(Car):
    def drive(self):
        return "Driving an porsche"

class lambo(Car):
    def drive(self):
        return "Driving a lambo"