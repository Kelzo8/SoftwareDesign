import unittest
from Game_files.coin import Coin
from settings import CarDimensions as cd

class TestCoin(unittest.TestCase):
    def setUp(self):
        self.coin = Coin(100, 100)

    def test_move(self):
        self.coin.move(5)
        self.assertEqual(self.coin.y, 105)

    def test_check_collision(self):
        class MockPlayer:
            car_x = 100
            car_y = 100

        player = MockPlayer()
        self.assertTrue(self.coin.check_collision(player))
        player.car_x = 200
        self.assertFalse(self.coin.check_collision(player))

if __name__ == '__main__':
    unittest.main()
