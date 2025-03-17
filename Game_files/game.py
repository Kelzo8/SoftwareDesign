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
from .UI import UI
from .interceptor import NearMissInterceptor, InterceptorDispatcher
from settings import CarDimensions as cd
# Import the strategy pattern classes
from .strategy import StraightMovement, ZigZagMovement, ChaseMovement

class Player:
    def __init__(self):
        self.selected_car = None
        self.car_x = SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2
        self.car_y = SCREEN_HEIGHT - cd.PLAYER_CAR_HEIGHT.value - 10
        self.name = ""

class GameObjects:
    def __init__(self):
        self.enemy_cars = []
        self.coins = []
        self.road_offset = 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Car Game")
        self.font = pygame.font.Font(None, 36)
        self.ui = UI(self.screen, self.font)
        self.player = Player()
        self.game_objects = GameObjects()
        self.clock = pygame.time.Clock()
        self.game_state = GameState()  # Singleton instance
        self.commands = self.initialize_commands()
        self.car_selection = self.initialize_car_selection()
        self.leaderboard = Leaderboard()
        self.game_state.attach(self.leaderboard)
        self.caretaker = Caretaker()
        self.interceptor_dispatcher = InterceptorDispatcher()
        self.near_miss_interceptor = NearMissInterceptor()
        self.interceptor_dispatcher.register_interceptor(self.near_miss_interceptor)
        self.enemy_cars_to_check = []  # List to track enemy cars for near misses
        self.checkpoint_loaded_time = None
        self.player_name = ""

    def initialize_commands(self):
        return {
            pygame.K_LEFT: MoveLeftCommand(),
            pygame.K_RIGHT: MoveRightCommand(),
            pygame.K_UP: MoveUpCommand(),
            pygame.K_DOWN: MoveDownCommand(),
            pygame.K_s: CheckPointCommand()
        }

    def initialize_car_selection(self):
        return {
            pygame.K_1: "ferrari",
            pygame.K_2: "lambo",
            pygame.K_3: "porsche"
        }

    def create_enemy_car(self):
        max_attempts = 100
        attempt = 0
        while attempt < max_attempts:
            lane = random.randint(0, NUM_LANES - 1)
            x = lane * LANE_WIDTH + (LANE_WIDTH - cd.ENEMY_CAR_WIDTH.value) // 2
            y = -cd.ENEMY_CAR_HEIGHT.value
            if not self.is_overlap(x, y):
                strategy = random.choice([StraightMovement(), ZigZagMovement(), ChaseMovement()])
                return CarFactory.create_car(x=x, y=y, speed=ENEMY_CAR_SPEED, strategy=strategy, car_type='enemy')
            attempt += 1
        return None

    def is_overlap(self, x, y):
        for enemy_car in self.game_objects.enemy_cars:
            if (abs(x - enemy_car.x) < cd.ENEMY_CAR_WIDTH.value and
                abs(y - enemy_car.y) < cd.ENEMY_CAR_HEIGHT.value):
                return True
        return False

    def create_coin(self):
        while True:
            lane = random.randint(0, NUM_LANES - 1)
            x = lane * LANE_WIDTH + (LANE_WIDTH - cd.PLAYER_CAR_WIDTH.value) // 2
            y = -cd.PLAYER_CAR_HEIGHT.value
            if not self.is_coin_overlap(x, y):
                return [x, y]

    def is_coin_overlap(self, x, y):
        return any(abs(x - enemy_car.x) < cd.PLAYER_CAR_WIDTH.value and abs(y - enemy_car.y) < cd.PLAYER_CAR_HEIGHT.value for enemy_car in self.game_objects.enemy_cars)

    def save_checkpoint(self):
        if self.game_state.coin_count >= CHECKPOINT_COIN_COUNT:
            self.game_state.coin_count -= CHECKPOINT_COIN_COUNT
            memento = Memento(self.player.car_x, self.player.car_y, self.game_state.coin_count, self.game_objects.enemy_cars, self.game_objects.coins)
            self.caretaker.save_memento(memento)

    def load_checkpoint(self):
        memento = self.caretaker.get_last_memento()
        if memento:
            self.player.car_x, self.player.car_y, self.game_state.coin_count, enemy_car_states, self.game_objects.coins = memento.get_state()
            self.game_objects.enemy_cars = [CarFactory.create_car(x=state.x, y=state.y, speed=state.speed, strategy=StraightMovement(), car_type='enemy') for state in enemy_car_states]
            self.checkpoint_loaded_time = time.time()
        return memento is not None

    def run(self):
        self.player.name = self.game_state.player_name
        name_entered = bool(self.player.name)

        while not name_entered and self.game_state.is_running:
            self.ui.draw_name_input(self.player.name)
            # print("Player name: ", player_name)
            name_entered = self.handle_name_input()
            pygame.display.flip()
            self.clock.tick(60)

        while self.game_state.is_running:
            self.screen.fill(WHITE)
            if not self.player.selected_car:
                self.handle_car_selection()
            else:
                self.update_game_state()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_name_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.stop_game()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player.name.strip():
                    self.game_state.set_player_name(self.player.name.strip())
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.player.name = self.player.name[:-1]
                elif event.unicode.isalnum() or event.unicode.isspace():
                    self.player.name += event.unicode
        return False

    def handle_car_selection(self):
        self.ui.draw_car_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.car_selection:
                    self.player.selected_car = CarFactory.create_car(self.car_selection[event.key])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                car_name = self.ui.handle_car_selection_click(event.pos)
                if car_name:
                    self.player.selected_car = CarFactory.create_car(car_name)

    def is_immunity_active(self):
        if self.checkpoint_loaded_time is None:
            return False, None
        remaining_time = CHECKPOINT_IMMUNE_TIME - (time.time() - self.checkpoint_loaded_time)
        return remaining_time > 0, remaining_time

    def update_game_state(self):
        self.ui.draw_road(self.game_objects.road_offset)
        self.ui.draw_car(self.player.car_x, self.player.car_y, self.player.selected_car)
        self.move_and_draw_enemy_cars()
        self.check_near_misses()
        self.remove_off_screen_enemy_cars()
        self.add_new_enemy_cars()
        self.move_and_draw_coins()
        self.ui.draw_coin_count(self.game_state.coin_count)
        self.ui.draw_near_miss_count(self.near_miss_interceptor.get_near_miss_count())
        immunity_active, remaining_time = self.is_immunity_active()
        if immunity_active:
            self.ui.draw_immunity_timer(remaining_time)
        self.handle_events()

    def move_and_draw_enemy_cars(self):
        immunity_active, _ = self.is_immunity_active()
        for enemy_car in self.game_objects.enemy_cars:
            enemy_car.move(self.player.car_x, self.game_objects.enemy_cars, self.game_state.coin_count)
            enemy_car.draw(self.ui)
            if self.check_collision(enemy_car, immunity_active):
                if not self.load_checkpoint():
                    self.handle_collision()

    def check_collision(self, enemy_car, immunity_active):
        if not immunity_active:
            return (self.player.car_y < enemy_car.y + cd.ENEMY_CAR_HEIGHT.value and
                    self.player.car_y + cd.PLAYER_CAR_HEIGHT.value > enemy_car.y and
                    self.player.car_x < enemy_car.x + cd.ENEMY_CAR_WIDTH.value and
                    self.player.car_x + cd.PLAYER_CAR_WIDTH.value > enemy_car.x)
        return False

    def handle_collision(self):
        self.game_state.stop_game()
        waiting_for_input = True
        while waiting_for_input:
            self.ui.display_leaderboard(self.leaderboard, self.game_state.coin_count)
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
                        return

    def check_near_misses(self):
        for enemy_car in self.enemy_cars_to_check[:]:
            self.interceptor_dispatcher.execute_interceptors((self.player.car_x, self.player.car_y), enemy_car)
            if (enemy_car.x, enemy_car.y) in self.near_miss_interceptor.counted_vehicles:
                self.enemy_cars_to_check.remove(enemy_car)

    def remove_off_screen_enemy_cars(self):
        self.game_objects.enemy_cars[:] = [car for car in self.game_objects.enemy_cars if car.y < SCREEN_HEIGHT]

    def add_new_enemy_cars(self):
        if random.randint(1, 20) == 1:
            new_car = self.create_enemy_car()
            if new_car:
                self.game_objects.enemy_cars.append(new_car)
                self.enemy_cars_to_check.append(new_car)

    def move_and_draw_coins(self):
        for coin in self.game_objects.coins:
            coin[1] += ENEMY_CAR_SPEED
            self.ui.draw_coin(coin[0], coin[1])
            if self.check_coin_collision(coin):
                self.game_objects.coins.remove(coin)
                self.game_state.add_coin()
        self.game_objects.coins[:] = [coin for coin in self.game_objects.coins if coin[1] < SCREEN_HEIGHT]
        if random.randint(1, 50) == 1:
            self.game_objects.coins.append(self.create_coin())

    def check_coin_collision(self, coin):
        return (self.player.car_y < coin[1] + cd.PLAYER_CAR_HEIGHT.value // 2 and
                self.player.car_y + cd.PLAYER_CAR_HEIGHT.value > coin[1] and
                self.player.car_x < coin[0] + cd.PLAYER_CAR_WIDTH.value // 2 and
                self.player.car_x + cd.PLAYER_CAR_WIDTH.value > coin[0])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.car_selection:
                    self.player.selected_car = CarFactory.create_car(self.car_selection[event.key])
                elif event.key in self.commands and self.player.selected_car:
                    self.commands[event.key].execute(game=self, player=self.player)
            elif event.type == pygame.KEYUP:
                if event.key in self.commands and self.player.selected_car:
                    self.commands[event.key].reset()

        keys = pygame.key.get_pressed()
        if self.player.selected_car:
            for key, command in self.commands.items():
                if keys[key] and key not in self.car_selection:
                    command.execute(player=self.player, game=self)

    def is_replay_button_clicked(self, mouse_pos):
        button_width = 200
        button_height = 50
        replay_button_x = SCREEN_WIDTH / 2 - button_width - 10
        button_y = SCREEN_HEIGHT / 2 + 150
        return (replay_button_x <= mouse_pos[0] <= replay_button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height)

    def is_quit_button_clicked(self, mouse_pos):
        button_width = 200
        button_height = 50
        quit_button_x = SCREEN_WIDTH / 2 + 10
        button_y = SCREEN_HEIGHT / 2 + 150
        return (quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height)

    def reset_game(self):
        self.player.selected_car = None
        self.player.car_x = SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2
        self.player.car_y = SCREEN_HEIGHT - cd.PLAYER_CAR_HEIGHT.value - 10
        self.game_objects.enemy_cars = []
        self.game_objects.coins = []
        self.game_objects.road_offset = 0
        self.near_miss_interceptor.near_miss_count = 0
        self.game_state.coin_count = 0
        self.game_state.is_running = True
