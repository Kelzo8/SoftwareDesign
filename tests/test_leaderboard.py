import unittest
from Game_files.leaderboard import Leaderboard

class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard()

    def test_update(self):
        self.leaderboard.scores = []
        self.leaderboard.update("test_player", 10)
        self.assertIn(["test_player", 10], self.leaderboard.scores)

    def test_load_scores(self):
        self.leaderboard.load_scores()
        self.assertIsInstance(self.leaderboard.scores, list)

    def test_save_scores(self):
        self.leaderboard.scores = []
        self.leaderboard.update("test_player", 10)
        self.leaderboard.save_scores()
        self.leaderboard.load_scores()
        self.assertIn(["test_player", 10], self.leaderboard.scores)

if __name__ == '__main__':
    unittest.main()
