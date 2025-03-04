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
from .interceptor import NearMissInterceptor, InterceptorDispatcher
from settings import CarDimensions as cd

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
        self.player_car_x = SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2
        self.player_car_y = SCREEN_HEIGHT - cd.PLAYER_CAR_HEIGHT.value - 10
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
        self.car_selection = {
            pygame.K_1: "ferrari",
            pygame.K_2: "porsche",
            pygame.K_3: "lambo"
        }
        self.leaderboard = Leaderboard()
        self.game_state.attach(self.leaderboard)
        self.caretaker = Caretaker()
        self.interceptor_dispatcher = InterceptorDispatcher()
        self.near_miss_interceptor = NearMissInterceptor()
        self.interceptor_dispatcher.register_interceptor(self.near_miss_interceptor)
        self.enemy_cars_to_check = []  # List to track cars being checked for near misses

    def create_enemy_car(self):
        while True:
            lane = random.randint(0, NUM_LANES - 1)
            x = lane * LANE_WIDTH + (LANE_WIDTH - cd.ENEMY_CAR_WIDTH.value) // 2
            y = -cd.ENEMY_CAR_HEIGHT.value
            # Check for overlap with coins
            if not any(abs(x - coin[0]) < cd.ENEMY_CAR_WIDTH.value and abs(y - coin[1]) < cd.ENEMY_CAR_HEIGHT.value for coin in self.coins):
                return [x, y]

    def create_coin(self):
        while True:
            lane = random.randint(0, NUM_LANES - 1)
            x = lane * LANE_WIDTH + (LANE_WIDTH - cd.PLAYER_CAR_WIDTH.value  ) // 2
            y = -cd.PLAYER_CAR_HEIGHT.value
            # Check for overlap with enemy cars
            if not any(abs(x - enemy_car[0]) < cd.PLAYER_CAR_WIDTH.value and abs(y - enemy_car[1]) < cd.PLAYER_CAR_HEIGHT.value for enemy_car in self.enemy_cars):
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
        player_name = self.game_state.player_name  # Use existing player name if available
        name_entered = bool(player_name)  # Determine if name was previously entered
        
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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        car_name = self.ui.handle_car_selection_click(event.pos)
                        if car_name:
                            self.selected_car = CarFactory.create_car(car_name)
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
                # Check for near misses
                for enemy_car in self.enemy_cars_to_check[:]:  # Iterate over a copy of the list
                    # Use dispatcher to handle near misses
                    self.interceptor_dispatcher.execute_interceptors(
                        (self.player_car_x, self.player_car_y), enemy_car)
                    # Check if the enemy car was counted as a near miss
                    if (enemy_car[0], enemy_car[1]) in self.near_miss_interceptor.counted_vehicles:
                        self.enemy_cars_to_check.remove(enemy_car)

                # Check for collision
                for enemy_car in self.enemy_cars:
                    if (self.player_car_y < enemy_car[1] + cd.ENEMY_CAR_HEIGHT.value and
                        self.player_car_y + cd.PLAYER_CAR_HEIGHT.value > enemy_car[1] and
                        self.player_car_x < enemy_car[0] + cd.ENEMY_CAR_WIDTH.value and
                        self.player_car_x + cd.PLAYER_CAR_WIDTH.value > enemy_car[0]):
                        self.game_state.stop_game()
                        waiting_for_input = True
                        while waiting_for_input:
                            self.ui.display_leaderboard(self.leaderboard)
                            self.ui.draw_replay_quit_buttons()
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    waiting_for_input = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if self.is_replay_button_clicked(event.pos):
                                        self.reset_game()
                                        waiting_for_input = False
                                    elif self.is_quit_button_clicked(event.pos):
                                        self.game_state.stop_game()
                                        waiting_for_input = False
                                        return  # Exit the game loop

                # Remove off-screen enemy cars
                self.enemy_cars[:] = [car for car in self.enemy_cars if car[1] < SCREEN_HEIGHT]

                # Add new enemy cars
                if random.randint(1, 20) == 1:
                    new_car = self.create_enemy_car()
                    self.enemy_cars.append(new_car)
                    self.enemy_cars_to_check.append(new_car)

                # Move coins
                for coin in self.coins:
                    coin[1] += ENEMY_CAR_SPEED
                    self.ui.draw_coin(coin[0], coin[1])

                    # Check for coin collection
                    if (self.player_car_y < coin[1] + cd.PLAYER_CAR_HEIGHT.value // 2 and
                        self.player_car_y + cd.PLAYER_CAR_HEIGHT.value > coin[1] and
                        self.player_car_x < coin[0] + cd.PLAYER_CAR_WIDTH.value // 2 and
                        self.player_car_x + cd.PLAYER_CAR_WIDTH.value > coin[0]):
                        self.coins.remove(coin)
                        self.game_state.add_coin()

                # Remove off-screen coins
                self.coins[:] = [coin for coin in self.coins if coin[1] < SCREEN_HEIGHT]

                # Add new coins
                if random.randint(1, 50) == 1:
                    self.coins.append(self.create_coin())

                # Draw coin count
                self.ui.draw_coin_count(self.game_state.coin_count)

                # Draw near miss count
                self.ui.draw_near_miss_count(self.near_miss_interceptor.get_near_miss_count())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state.stop_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.car_selection:
                        self.selected_car = CarFactory.create_car(self.car_selection[event.key])
                    elif event.key in self.commands and self.selected_car:
                        self.commands[event.key].execute(self)
                elif event.type == pygame.KEYUP:
                    if event.key in self.commands and self.selected_car:
                        self.commands[event.key].reset()
    

            keys = pygame.key.get_pressed()
            if self.selected_car:
                for key, command in self.commands.items():
                    if keys[key] and key not in self.car_selection:
                        print(key)
                        command.execute(self)


            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def is_replay_button_clicked(self, mouse_pos):
        button_width = 200
        button_height = 50
        replay_button_x = SCREEN_WIDTH / 2 - button_width - 10
        button_y = SCREEN_HEIGHT / 2 + 250  # Adjusted to match the new button position
        return (replay_button_x <= mouse_pos[0] <= replay_button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height)

    def is_quit_button_clicked(self, mouse_pos):
        button_width = 200
        button_height = 50
        quit_button_x = SCREEN_WIDTH / 2 + 10
        button_y = SCREEN_HEIGHT / 2 + 250  # Adjusted to match the new button position
        return (quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height)

    def reset_game(self):
        self.selected_car = None
        self.player_car_x = SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2
        self.player_car_y = SCREEN_HEIGHT - cd.PLAYER_CAR_HEIGHT.value - 10
        self.enemy_cars = []
        self.coins = []
        self.road_offset = 0
        self.near_miss_interceptor.near_miss_count = 0  # Reset near miss count
        self.game_state.coin_count = 0  # Reset coin count
        # Set flag to prompt for name entry again
        self.game_state.is_running = True
        name_entered = False  # Reset name entry flag