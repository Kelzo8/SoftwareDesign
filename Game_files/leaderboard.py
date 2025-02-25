from abc import ABC, abstractmethod
import json
import os

class Observer(ABC):
    @abstractmethod
    def update(self, player_name: str, score: int):
        pass

class Leaderboard(Observer):
    def __init__(self):
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        try:
            if os.path.exists('leaderboard.json'):
                with open('leaderboard.json', 'r') as file:
                    self.scores = json.load(file)
            # Ensure we start with valid data
            if not isinstance(self.scores, list):
                self.scores = []
        except:
            self.scores = []
    
    def save_scores(self):
        with open('leaderboard.json', 'w') as file:
            json.dump(self.scores[:5], file)  # Only save top 5
    
    def update(self, player_name: str, score: int):
        # Check if new score should be added
        should_add = len(self.scores) < 5  # Add if we have less than 5 scores
        
        if not should_add:
            # Check if new score is higher than the lowest score
            lowest_score = min(score for _, score in self.scores)
            should_add = score > lowest_score
        
        if should_add:
            # Add new score
            self.scores.append([player_name, score])
            # Sort by score in descending order
            self.scores.sort(key=lambda x: x[1], reverse=True)
            # Keep only top 5
            self.scores = self.scores[:5]
            # Save to file
            self.save_scores()
        
    def display(self, screen, font):
        y_offset = 200
        screen.fill((255, 255, 255))  # White background
        title = font.render("GAME OVER - LEADERBOARD", True, (0, 0, 0))
        screen.blit(title, (200, 150))
        
        for i, (name, score) in enumerate(self.scores[:5]):  # Only display top 5
            text = font.render(f"#{i + 1}: {name} - {score} coins", True, (0, 0, 0))
            screen.blit(text, (300, y_offset))
            y_offset += 50