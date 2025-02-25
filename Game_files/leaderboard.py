from .observer import Observer

class Leaderboard(Observer):
    def __init__(self):
        self.scores = []

    def update(self, player_name: str, score: int):
        self.scores.append((player_name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        self.display()

    def display(self):
        print("Leaderboard:")
        for i, (player_name, score) in enumerate(self.scores[:10], start=1):
            print(f"{i}. {player_name}: {score}")