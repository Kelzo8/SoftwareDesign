import unittest
from Game_files.command import MoveLeftCommand, MoveRightCommand, MoveUpCommand, MoveDownCommand, CheckPointCommand
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_CAR_SPEED, CarDimensions as cd
from Game_files.model import GameModel
class MockPlayer:
    def __init__(self):
        self.car_x = SCREEN_WIDTH // 2
        self.car_y = SCREEN_HEIGHT // 2

class MockModel:
    def __init__(self):
        self.player = MockPlayer()
        self.game_state = MockGameState()

class MockGameState:
    def __init__(self):
        self.coin_count = 10

    def save_checkpoint(self):
        self.coin_count -= 5

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.player = MockPlayer()
        self.model = GameModel()
        self.model.game_state = MockGameState()

    def test_move_left(self):
        command = MoveLeftCommand()
        command.execute(player=self.player)
        self.assertEqual(self.player.car_x, SCREEN_WIDTH // 2 - PLAYER_CAR_SPEED)

    def test_move_right(self):
        command = MoveRightCommand()
        command.execute(player=self.player)
        self.assertEqual(self.player.car_x, SCREEN_WIDTH // 2 + PLAYER_CAR_SPEED)

    def test_move_up(self):
        command = MoveUpCommand()
        command.execute(player=self.player)
        self.assertEqual(self.player.car_y, SCREEN_HEIGHT // 2 - PLAYER_CAR_SPEED)

    def test_move_down(self):
        command = MoveDownCommand()
        command.execute(player=self.player)
        self.assertEqual(self.player.car_y, SCREEN_HEIGHT // 2 + PLAYER_CAR_SPEED)

    def test_checkpoint_command(self):
        
        command = CheckPointCommand()
        command.execute(model=self.model)
        self.assertEqual(self.model.game_state.coin_count, 5)

if __name__ == '__main__':
    unittest.main()
