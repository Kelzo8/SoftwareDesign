# game.py
import time
import pygame
import random
from .car_factory import CarFactory
from settings import *
from .game_state import GameState
from .command import MoveLeftCommand, MoveRightCommand, MoveUpCommand, MoveDownCommand
from .leaderboard import Leaderboard
import pygame.locals
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
            if not isinstance(self.scores, list):
                self.scores = []
        except:
            self.scores = []
    
    def save_scores(self):
        with open('leaderboard.json', 'w') as file:
            json.dump(self.scores[:5], file)
    
    def update(self, player_name: str, score: int):
        should_add = len(self.scores) < 5
        
        if not should_add:
            lowest_score = min(score for _, score in self.scores)
            should_add = score > lowest_score
        
        if should_add:
            self.scores.append([player_name, score])
            self.scores.sort(key=lambda x: x[1], reverse=True)
            self.scores = self.scores[:5]
            self.save_scores()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Car Game")
        self.font = pygame.font.Font(None, 36)
        self.selected_car = None
        self.player_car_x = SCREEN_WIDTH // 2 - PLAYER_CAR_WIDTH // 2
        self.player_car_y = SCREEN_HEIGHT - PLAYER_CAR_HEIGHT - 10
        self.enemy_cars = []
        self.coins = []
        self.road_offset = 0
        self.clock = pygame.time.Clock()
        self.game_state = GameState()  # Singleton instance
        self.commands = {
            pygame.K_LEFT: MoveLeftCommand(),
            pygame.K_RIGHT: MoveRightCommand(),
            pygame.K_UP: MoveUpCommand(),
            pygame.K_DOWN: MoveDownCommand(),
        }
        self.leaderboard = Leaderboard()
        self.game_state.attach(self.leaderboard)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (x, y))

    def draw_car(self, x, y, car_type):
        color_map = {"ferrari": RED, "porsche": GREEN, "lambo": BLUE, "enemy": BLACK}
        color = color_map.get(car_type, BLACK)
        pygame.draw.rect(self.screen, color, [x, y, PLAYER_CAR_WIDTH, PLAYER_CAR_HEIGHT])

    def draw_road(self):
        self.screen.fill(GREY)
        for i in range(NUM_LANES + 1):
            lane_x = i * LANE_WIDTH
            for j in range(0, SCREEN_HEIGHT, ROAD_LINE_HEIGHT + ROAD_LINE_GAP):
                pygame.draw.line(self.screen, WHITE, (lane_x, j + self.road_offset), 
                                 (lane_x, j + ROAD_LINE_HEIGHT + self.road_offset), 2)
        self.road_offset = (self.road_offset + 5) % (ROAD_LINE_HEIGHT + ROAD_LINE_GAP)

    def create_enemy_car(self):
        lane = random.randint(0, NUM_LANES - 1)
        x = lane * LANE_WIDTH + (LANE_WIDTH - ENEMY_CAR_WIDTH) // 2
        y = -ENEMY_CAR_HEIGHT
        return [x, y]

    def create_coin(self):
        lane = random.randint(0, NUM_LANES - 1)
        x = lane * LANE_WIDTH + (LANE_WIDTH - PLAYER_CAR_WIDTH) // 2
        y = -PLAYER_CAR_HEIGHT
        return [x, y]

    def draw_coin(self, x, y):
        pygame.draw.circle(self.screen, (255, 215, 0), (x + PLAYER_CAR_WIDTH // 2, y + PLAYER_CAR_HEIGHT // 2), 
                           PLAYER_CAR_WIDTH // 4)

    def draw_name_input(self, player_name):
        self.screen.fill((240, 240, 245))  # Light blue-gray background
        
        # Title box with shadow
        title_box_width = 400
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        [SCREEN_WIDTH/2 - title_box_width/2 + 5, 105, 
                         title_box_width, 70])
        pygame.draw.rect(self.screen, WHITE,
                        [SCREEN_WIDTH/2 - title_box_width/2, 100, 
                         title_box_width, 70])
        
        # Title
        title = self.font.render("ENTER YOUR NAME", True, (50, 50, 50))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 135))
        self.screen.blit(title, title_rect)
        
        # Input box with shadow
        input_box_width = 300
        input_box_height = 50
        pygame.draw.rect(self.screen, (200, 200, 200),
                        [SCREEN_WIDTH/2 - input_box_width/2 + 5, 255,
                         input_box_width, input_box_height])
        pygame.draw.rect(self.screen, WHITE,
                        [SCREEN_WIDTH/2 - input_box_width/2, 250,
                         input_box_width, input_box_height])
        pygame.draw.rect(self.screen, (100, 100, 100),
                        [SCREEN_WIDTH/2 - input_box_width/2, 250,
                         input_box_width, input_box_height], 2)
        
        # Name text
        name_text = self.font.render(player_name + ("_" if time.time() % 1 > 0.5 else ""), 
                                    True, (50, 50, 50))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH/2, 275))
        self.screen.blit(name_text, name_rect)
        
        # Instructions
        inst = self.font.render("Press ENTER when done", True, (100, 100, 100))
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH/2, 350))
        self.screen.blit(inst, inst_rect)

    def draw_car_selection(self):
        self.screen.fill((240, 240, 245))
        
        # Title with decorative elements
        pygame.draw.rect(self.screen, WHITE, [150, 50, 500, 80])
        pygame.draw.rect(self.screen, (200, 200, 200), [155, 55, 500, 80], 3)
        title = self.font.render("SELECT YOUR CAR", True, (50, 50, 50))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 90))
        self.screen.blit(title, title_rect)
        
        cars = [("Red Ferrari", RED), ("Blue Porsche", BLUE), ("Green Lambo", GREEN)]
        
        for i, (car_name, color) in enumerate(cars):
            # Calculate positions
            box_width = 220
            box_height = 180
            margin = 20
            total_width = (box_width + margin) * len(cars)
            start_x = (SCREEN_WIDTH - total_width) / 2
            box_x = start_x + i * (box_width + margin)
            box_y = 200
            
            # Draw card shadow
            pygame.draw.rect(self.screen, (200, 200, 200),
                            [box_x + 5, box_y + 5, box_width, box_height])
            
            # Draw card background
            pygame.draw.rect(self.screen, WHITE,
                            [box_x, box_y, box_width, box_height])
            
            # Highlight on hover
            mouse_pos = pygame.mouse.get_pos()
            if (box_x <= mouse_pos[0] <= box_x + box_width and 
                box_y <= mouse_pos[1] <= box_y + box_height):
                pygame.draw.rect(self.screen, color,
                               [box_x, box_y, box_width, box_height], 4)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100),
                               [box_x, box_y, box_width, box_height], 2)
            
            # Draw car preview
            car_rect = pygame.draw.rect(self.screen, color,
                                      [box_x + box_width/2 - PLAYER_CAR_WIDTH/2,
                                       box_y + 40,
                                       PLAYER_CAR_WIDTH,
                                       PLAYER_CAR_HEIGHT])
            
            # Car name
            name_text = self.font.render(car_name, True, (50, 50, 50))
            name_rect = name_text.get_rect(center=(box_x + box_width/2, box_y + 120))
            self.screen.blit(name_text, name_rect)
            
            # Key instruction
            key_text = self.font.render(f"Press {i+1}", True, (100, 100, 100))
            key_rect = key_text.get_rect(center=(box_x + box_width/2, box_y + 150))
            self.screen.blit(key_text, key_rect)

    def display_leaderboard(self):
        # Background
        self.screen.fill((240, 240, 245))
        
        # Game Over Title - Moved up slightly
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("GAME OVER", True, (50, 50, 50))
        title_rect = title.get_rect(center=(self.screen.get_width()/2, 60))
        self.screen.blit(title, title_rect)
        
        # Leaderboard Title - Moved up slightly
        subtitle = self.font.render("LEADERBOARD", True, (50, 50, 50))
        subtitle_rect = subtitle.get_rect(center=(self.screen.get_width()/2, 110))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw decorative line - Moved up slightly
        pygame.draw.line(self.screen, (200, 200, 200),
                        (self.screen.get_width()/4, 140),
                        (self.screen.get_width()*3/4, 140), 3)
        
        # Reduced starting y_offset and spacing between boxes
        y_offset = 160
        box_height = 50  # Reduced box height
        box_width = 400
        spacing = 8  # Reduced spacing between boxes
        
        # Display top 5 scores
        for i, (name, score) in enumerate(self.leaderboard.scores[:5]):
            box_x = self.screen.get_width()/2 - box_width/2
            
            # Draw box shadow
            pygame.draw.rect(self.screen, (200, 200, 200),
                            [box_x+5, y_offset+5, box_width, box_height])
            
            # Draw main box
            pygame.draw.rect(self.screen, WHITE,
                            [box_x, y_offset, box_width, box_height])
            
            # Position number
            position = self.font.render(f"#{i + 1}", True, (50, 50, 50))
            self.screen.blit(position, (box_x + 20, y_offset + 10))
            
            # Player name and score
            name_text = self.font.render(name, True, (50, 50, 50))
            score_text = self.font.render(f"{score} coins", True, (255, 215, 0))
            self.screen.blit(name_text, (box_x + 80, y_offset + 10))
            self.screen.blit(score_text, (box_x + box_width - 120, y_offset + 10))
            
            y_offset += box_height + spacing

        # Current player's score box
        current_score_box_height = 70
        current_score_box_width = 500
        box_x = self.screen.get_width()/2 - current_score_box_width/2
        
        # Add spacing before current player's score
        y_offset += 10
        
        # Draw box shadow for current score
        pygame.draw.rect(self.screen, (200, 200, 200),
                        [box_x+5, y_offset+5, current_score_box_width, current_score_box_height])
        
        # Draw main box for current score with gold border
        pygame.draw.rect(self.screen, (230, 230, 240),
                        [box_x, y_offset, current_score_box_width, current_score_box_height])
        pygame.draw.rect(self.screen, GOLD,
                        [box_x, y_offset, current_score_box_width, current_score_box_height], 3)
        
        # Display current player's info
        your_name_text = self.font.render(f"Player: {self.game_state.player_name}", True, (50, 50, 50))
        your_score_text = self.font.render(f"Your Score: {self.game_state.coin_count} coins", True, (50, 50, 50))
        self.screen.blit(your_name_text, (box_x + 20, y_offset + 10))
        self.screen.blit(your_score_text, (box_x + 20, y_offset + 40))
        
        # Press any key text - Moved closer to bottom
        press_key = self.font.render("Press any key to continue", True, (100, 100, 100))
        press_key_rect = press_key.get_rect(center=(self.screen.get_width()/2, SCREEN_HEIGHT - 40))
        self.screen.blit(press_key, press_key_rect)

    def run(self):
        # Add name input before starting the game
        player_name = ""
        name_entered = False
        
        while not name_entered and self.game_state.is_running:
            self.draw_name_input(player_name)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state.stop_game()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        name_entered = True
                        self.game_state.set_player_name(player_name.strip())
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isalnum() or event.unicode.isspace():
                        player_name += event.unicode
            
            pygame.display.flip()
            self.clock.tick(60)

        while self.game_state.is_running:
            self.screen.fill(WHITE)

            if not self.selected_car:
                self.draw_car_selection()
            else:
                self.draw_road()
                self.draw_car(self.player_car_x, self.player_car_y, self.selected_car.__class__.__name__.lower())

                # Move enemy cars
                for enemy_car in self.enemy_cars:
                    enemy_car[1] += ENEMY_CAR_SPEED
                    self.draw_car(enemy_car[0], enemy_car[1], "enemy")

                    # Check for collision
                    if (self.player_car_y < enemy_car[1] + ENEMY_CAR_HEIGHT and
                        self.player_car_y + PLAYER_CAR_HEIGHT > enemy_car[1] and
                        self.player_car_x < enemy_car[0] + ENEMY_CAR_WIDTH and
                        self.player_car_x + PLAYER_CAR_WIDTH > enemy_car[0]):
                        self.game_state.stop_game()
                        waiting_for_input = True
                        while waiting_for_input:
                            self.display_leaderboard()
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    waiting_for_input = False
                                elif event.type == pygame.KEYDOWN:
                                    waiting_for_input = False

                # Remove off-screen enemy cars
                self.enemy_cars[:] = [car for car in self.enemy_cars if car[1] < SCREEN_HEIGHT]

                # Add new enemy cars
                if random.randint(1, 20) == 1:
                    self.enemy_cars.append(self.create_enemy_car())

                # Move coins
                for coin in self.coins:
                    coin[1] += ENEMY_CAR_SPEED
                    self.draw_coin(coin[0], coin[1])

                    # Check for coin collection
                    if (self.player_car_y < coin[1] + PLAYER_CAR_HEIGHT // 2 and
                        self.player_car_y + PLAYER_CAR_HEIGHT > coin[1] and
                        self.player_car_x < coin[0] + PLAYER_CAR_WIDTH // 2 and
                        self.player_car_x + PLAYER_CAR_WIDTH > coin[0]):
                        self.coins.remove(coin)
                        self.game_state.add_coin()

                # Remove off-screen coins
                self.coins[:] = [coin for coin in self.coins if coin[1] < SCREEN_HEIGHT]

                # Add new coins
                if random.randint(1, 50) == 1:
                    self.coins.append(self.create_coin())

                # Draw coin count
                pygame.draw.rect(self.screen, WHITE, [0, 0, 150, 50])
                pygame.draw.rect(self.screen, BLACK, [0, 0, 150, 50], 2)
                self.draw_text(f"Coins: {self.game_state.coin_count}", 10, 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state.stop_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_car = CarFactory.create_car("ferrari")
                    elif event.key == pygame.K_2:
                        self.selected_car = CarFactory.create_car("porsche")
                    elif event.key == pygame.K_3:
                        self.selected_car = CarFactory.create_car("lambo")

            keys = pygame.key.get_pressed()
            if self.selected_car:
                for key, command in self.commands.items():
                    if keys[key]:
                        command.execute(self)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()