import unittest
from Game_files.leaderboard import Leaderboard
from settings import LEADERBOARD_COUNT

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

    def test_update_existing_score(self):
        self.leaderboard.scores = [["test_player", 5] for _ in range(LEADERBOARD_COUNT)]
        self.leaderboard.update("test_player", 10)
        self.assertIn(["test_player", 10], self.leaderboard.scores)
        self.assertNotIn(["test_player", 5], self.leaderboard.scores[0])

    def test_update_with_lower_score(self):
        self.leaderboard.scores = [["test_player", 10] for _ in range(LEADERBOARD_COUNT)]
        self.leaderboard.update("test_player", 5)
        self.assertIn(["test_player", 10], self.leaderboard.scores)
        self.assertNotIn(["test_player", 5], self.leaderboard.scores)

if __name__ == '__main__':
    unittest.main()
