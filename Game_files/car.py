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
    
class Enemy(Car):
    def __init__(self, x, y, speed, strategy, car_type='enemy'):
        self.x = x
        self.y = y
        self.speed = speed
        self.strategy = strategy
        self.car_type = car_type

    def move(self, player_x, enemy_cars, coin_count):
        self.strategy.move(self, player_x, enemy_cars, coin_count)

    def draw(self, ui):
        ui.draw_car(self.x, self.y, self)
    
    def drive(self):
        return "I am an enemy"
    
    def get_image(self):
        return "assets/enemy.png"