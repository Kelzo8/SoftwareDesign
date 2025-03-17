import unittest
from Game_files.car_factory import CarFactory
from Game_files.car import Ferrari, Porsche, Lambo, Enemy

class TestCarFactory(unittest.TestCase):
    def test_create_ferrari(self):
        car = CarFactory.create_car(car_type="ferrari")
        self.assertIsInstance(car, Ferrari)

    def test_create_porsche(self):
        car = CarFactory.create_car(car_type="porsche")
        self.assertIsInstance(car, Porsche)

    def test_create_lambo(self):
        car = CarFactory.create_car(car_type="lambo")
        self.assertIsInstance(car, Lambo)

    def test_create_enemy(self):
        car = CarFactory.create_car(car_type="enemy", x=0, y=0, speed=5, strategy=None)
        self.assertIsInstance(car, Enemy)

if __name__ == '__main__':
    unittest.main()
