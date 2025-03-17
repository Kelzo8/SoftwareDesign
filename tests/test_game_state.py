import unittest
from Game_files.game_state import GameState

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.game_state.reset()
    def test_add_coin(self):
        self.game_state.add_coin()
        self.assertEqual(self.game_state.coin_count, 1)

    def test_stop_game(self):
        self.game_state.stop_game()
        self.assertFalse(self.game_state.is_running)

    def test_reset(self):
        self.game_state.add_coin()
        self.game_state.reset()
        self.assertEqual(self.game_state.coin_count, 0)
        self.assertTrue(self.game_state.is_running)

if __name__ == '__main__':
    unittest.main()
