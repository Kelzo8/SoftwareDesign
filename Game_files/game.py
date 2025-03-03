# game.py
import time
import pygame
import random
from .car_factory import CarFactory
from settings import *
from .game_state import GameState
from .command import MoveLeftCommand, MoveRightCommand, MoveUpCommand, MoveDownCommand, CheckPointCommand
from .leaderboard import Leaderboard
from .memento import Memento
from .caretaker import Caretaker
import pygame.locals
from abc import ABC, abstractmethod
import json
import os
from .UI import UI

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
        self.ui = UI(self.screen, self.font)
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
            pygame.K_s: CheckPointCommand()
        }
        self.leaderboard = Leaderboard()
        self.game_state.attach(self.leaderboard)
        self.caretaker = Caretaker()

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

    def save_checkpoint(self):
        if self.game_state.coin_count >= 5:
            self.game_state.coin_count -= 5
            memento = Memento(self.player_car_x, self.player_car_y, self.game_state.coin_count, self.enemy_cars, self.coins)
            self.caretaker.save_memento(memento)

    def load_checkpoint(self):
        memento = self.caretaker.get_last_memento()
        if memento:
            self.player_car_x, self.player_car_y, self.game_state.coin_count, self.enemy_cars, self.coins = memento.get_state()
        return memento is not None

    def run(self):
        # Add name input before starting the game
        player_name = ""
        name_entered = False
        
        while not name_entered and self.game_state.is_running:
            self.ui.draw_name_input(player_name)
            
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
                self.ui.draw_car_selection()
            else:
                self.ui.draw_road(self.road_offset)
                self.ui.draw_car(self.player_car_x, self.player_car_y, self.selected_car.__class__.__name__.lower())

                # Move enemy cars
                for enemy_car in self.enemy_cars:
                    enemy_car[1] += ENEMY_CAR_SPEED
                    self.ui.draw_car(enemy_car[0], enemy_car[1], "enemy")

                    # Check for collision
                    if (self.player_car_y < enemy_car[1] + ENEMY_CAR_HEIGHT and
                        self.player_car_y + PLAYER_CAR_HEIGHT > enemy_car[1] and
                        self.player_car_x < enemy_car[0] + ENEMY_CAR_WIDTH and
                        self.player_car_x + PLAYER_CAR_WIDTH > enemy_car[0]):

                        if not self.load_checkpoint():
                            self.game_state.stop_game()
                            waiting_for_input = True
                            while waiting_for_input:
                                self.ui.display_leaderboard(self.leaderboard, self.game_state.coin_count)
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
                    self.ui.draw_coin(coin[0], coin[1])

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
                self.ui.draw_coin_count(self.game_state.coin_count)

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