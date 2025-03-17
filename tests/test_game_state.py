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

    def test_set_player_name(self):
        self.game_state.set_player_name("TestPlayer")
        self.assertEqual(self.game_state.player_name, "TestPlayer")

    def test_attach_observer(self):
        class MockObserver:
            def update(self, player_name, score):
                self.player_name = player_name
                self.score = score

        observer = MockObserver()
        self.game_state.attach(observer)
        self.game_state.notify_observers()
        self.assertEqual(observer.player_name, "")
        self.assertEqual(observer.score, 0)

if __name__ == '__main__':
    unittest.main()
