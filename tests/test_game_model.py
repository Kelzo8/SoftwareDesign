import unittest
from Game_files.model import GameModel
from Game_files.car_factory import CarFactory
from Game_files.coin import Coin
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CarDimensions as cd
import time

class TestGameModel(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_create_enemy_car(self):
        enemy_car = self.model.create_enemy_car()
        self.assertIsNotNone(enemy_car)
        self.assertEqual(enemy_car.car_type, 'enemy')

    def test_is_overlap(self):
        self.model.game_objects.enemy_cars.append(CarFactory.create_car(car_type='enemy', x=100, y=100, speed=5, strategy=None))
        self.assertTrue(self.model.is_overlap(100, 100))
        self.assertFalse(self.model.is_overlap(200, 200))

    def test_create_coin(self):
        coin = self.model.create_coin()
        self.assertIsInstance(coin, Coin)

    def test_save_checkpoint(self):
        self.model.game_state.coin_count = 10
        self.model.save_checkpoint()
        self.assertEqual(self.model.game_state.coin_count, 5)

    def test_load_checkpoint(self):
        self.model.game_state.coin_count = 10
        self.model.save_checkpoint()
        self.model.player.car_x = 0
        self.model.load_checkpoint()
        self.assertEqual(self.model.player.car_x, SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2)

    def test_is_immunity_active(self):
        self.model.checkpoint_loaded_time = time.time()
        immunity_active, remaining_time = self.model.is_immunity_active()
        self.assertTrue(immunity_active)
        self.assertGreater(remaining_time, 0)

    def test_remove_off_screen_enemy_cars(self):
        self.model.game_objects.enemy_cars.append(CarFactory.create_car(car_type='enemy', x=100, y=SCREEN_HEIGHT + 10, speed=5, strategy=None))
        self.model.remove_off_screen_enemy_cars()
        self.assertEqual(len(self.model.game_objects.enemy_cars), 0)

    def test_add_new_enemy_cars(self):
        initial_count = len(self.model.game_objects.enemy_cars)
        self.model.add_new_enemy_cars()
        self.assertGreaterEqual(len(self.model.game_objects.enemy_cars), initial_count)

if __name__ == '__main__':
    unittest.main()
