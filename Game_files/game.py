import time
import pygame
import random
from settings import *
from .command import MoveLeftCommand, MoveRightCommand, MoveUpCommand, MoveDownCommand, CheckPointCommand
from .leaderboard import Leaderboard
from .UI import UI
from .model import GameModel
from .car_factory import CarFactory
from settings import CarDimensions as cd

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Car Game")
        self.font = pygame.font.Font(None, 36)
        self.ui = UI(self.screen, self.font)
        self.model = GameModel()
        self.clock = pygame.time.Clock()
        self.commands = self.initialize_commands()
        self.car_selection = self.initialize_car_selection()
        self.leaderboard = Leaderboard()
        self.model.game_state.attach(self.leaderboard)

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

    def run(self):
        self.model.player.name = self.model.game_state.player_name
        name_entered = bool(self.model.player.name)

        while not name_entered and self.model.game_state.is_running:
            self.ui.draw_name_input(self.model.player.name)
            name_entered = self.handle_name_input()
            pygame.display.flip()
            self.clock.tick(60)

        while self.model.game_state.is_running:
            self.screen.fill(WHITE)
            if not self.model.player.selected_car:
                self.handle_car_selection()
            else:
                self.update_game_state()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_name_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.game_state.stop_game()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.model.player.name.strip():
                    self.model.game_state.set_player_name(self.model.player.name.strip())
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.model.player.name = self.model.player.name[:-1]
                elif event.unicode.isalnum() or event.unicode.isspace():
                    self.model.player.name += event.unicode
        return False

    def handle_car_selection(self):
        self.ui.draw_car_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.game_state.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.car_selection:
                    self.model.player.selected_car = CarFactory.create_car(self.car_selection[event.key])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                car_name = self.ui.handle_car_selection_click(event.pos)
                if car_name:
                    self.model.player.selected_car = CarFactory.create_car(car_name)

    def update_game_state(self):
        self.ui.draw_road(self.model.game_objects.road_offset)
        self.ui.draw_car(self.model.player.car_x, self.model.player.car_y, self.model.player.selected_car)
        self.move_and_draw_enemy_cars()
        self.model.check_near_misses()
        self.model.remove_off_screen_enemy_cars()
        self.model.add_new_enemy_cars()
        self.move_and_draw_coins()
        self.ui.draw_coin_count(self.model.game_state.coin_count)
        self.ui.draw_near_miss_count(self.model.near_miss_interceptor.get_near_miss_count())
        immunity_active, remaining_time = self.model.is_immunity_active()
        if immunity_active:
            self.ui.draw_immunity_timer(remaining_time)
        self.handle_events()

    def move_and_draw_enemy_cars(self):
        immunity_active, _ = self.model.is_immunity_active()
        for enemy_car in self.model.game_objects.enemy_cars:
            enemy_car.move(self.model.player.car_x, self.model.game_objects.enemy_cars, self.model.game_state.coin_count)
            enemy_car.draw(self.ui)
            if self.check_collision(enemy_car, immunity_active):
                if not self.model.load_checkpoint():
                    self.handle_collision()

    def check_collision(self, enemy_car, immunity_active):
        if not immunity_active:
            return (self.model.player.car_y < enemy_car.y + cd.ENEMY_CAR_HEIGHT.value and
                    self.model.player.car_y + cd.PLAYER_CAR_HEIGHT.value > enemy_car.y and
                    self.model.player.car_x < enemy_car.x + cd.ENEMY_CAR_WIDTH.value and
                    self.model.player.car_x + cd.PLAYER_CAR_WIDTH.value > enemy_car.x)
        return False

    def handle_collision(self):
        self.model.game_state.stop_game()
        waiting_for_input = True
        while waiting_for_input:
            self.ui.display_leaderboard(self.leaderboard, self.model.game_state.coin_count)
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
                        self.model.game_state.stop_game()
                        waiting_for_input = False
                        return

    def move_and_draw_coins(self):
        for coin in self.model.game_objects.coins:
            coin.move(ENEMY_CAR_SPEED)
            coin.draw(self.ui)
            if coin.check_collision(self.model.player):
                self.model.game_objects.coins.remove(coin)
                self.model.game_state.add_coin()
        self.model.game_objects.coins[:] = [coin for coin in self.model.game_objects.coins if coin.y < SCREEN_HEIGHT]
        if random.randint(1, NEW_COIN_PROBABILITY) == 1:
            self.model.game_objects.coins.append(self.model.create_coin())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.game_state.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.car_selection:
                    self.model.player.selected_car = CarFactory.create_car(self.car_selection[event.key])
                elif event.key in self.commands and self.model.player.selected_car:
                    self.commands[event.key].execute(model=self.model, player=self.model.player)
            elif event.type == pygame.KEYUP:
                if event.key in self.commands and self.model.player.selected_car:
                    self.commands[event.key].reset()

        keys = pygame.key.get_pressed()
        if self.model.player.selected_car:
            for key, command in self.commands.items():
                if keys[key] and key not in self.car_selection:
                    command.execute(player=self.model.player, game=self)

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
        self.model.player.selected_car = None
        self.model.player.car_x = SCREEN_WIDTH // 2 - cd.PLAYER_CAR_WIDTH.value // 2
        self.model.player.car_y = SCREEN_HEIGHT - cd.PLAYER_CAR_HEIGHT.value - 10
        self.model.game_objects.enemy_cars = []
        self.model.game_objects.coins = []
        self.model.game_objects.road_offset = 0
        self.model.near_miss_interceptor.near_miss_count = 0
        self.model.game_state.coin_count = 0
        self.model.game_state.is_running = True