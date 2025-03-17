import random
import time
from .car_factory import CarFactory
from settings import *
from .game_state import GameState
from .memento import Memento
from .caretaker import Caretaker
from .interceptor import NearMissInterceptor, InterceptorDispatcher
from settings import CarDimensions as cd
from .coin import Coin
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

class GameModel:
    def __init__(self):
        self.player = Player()
        self.game_objects = GameObjects()
        self.game_state = GameState()  # Singleton instance
        self.caretaker = Caretaker()
        self.interceptor_dispatcher = InterceptorDispatcher()
        self.near_miss_interceptor = NearMissInterceptor()
        self.interceptor_dispatcher.register_interceptor(self.near_miss_interceptor)
        self.enemy_cars_to_check = []  # List to track enemy cars for near misses
        self.checkpoint_loaded_time = None

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
                return Coin(x, y)

    def is_coin_overlap(self, x, y):
        return any(abs(x - enemy_car.x) < cd.PLAYER_CAR_WIDTH.value and abs(y - enemy_car.y) < cd.PLAYER_CAR_HEIGHT.value for enemy_car in self.game_objects.enemy_cars)

    def save_checkpoint(self):
        if self.game_state.coin_count >= CHECKPOINT_COIN_COUNT:
            self.game_state.coin_count -= CHECKPOINT_COIN_COUNT
            memento = Memento(self.player.car_x, self.player.car_y, self.game_objects.enemy_cars, self.game_objects.coins)
            self.caretaker.save_memento(memento)

    def load_checkpoint(self):
        memento = self.caretaker.get_last_memento()
        if memento:
            self.player.car_x, self.player.car_y, enemy_car_states, self.game_objects.coins = memento.get_state()
            self.game_objects.enemy_cars = [CarFactory.create_car(x=state.x, y=state.y, speed=state.speed, strategy=StraightMovement(), car_type='enemy') for state in enemy_car_states]
            self.checkpoint_loaded_time = time.time()
        return memento is not None

    def is_immunity_active(self):
        if self.checkpoint_loaded_time is None:
            return False, None
        remaining_time = CHECKPOINT_IMMUNE_TIME - (time.time() - self.checkpoint_loaded_time)
        return remaining_time > 0, remaining_time

    def check_near_misses(self):
        for enemy_car in self.enemy_cars_to_check[:]:
            self.interceptor_dispatcher.execute_interceptors((self.player.car_x, self.player.car_y), enemy_car)
            if (enemy_car.x, enemy_car.y) in self.near_miss_interceptor.counted_vehicles:
                self.enemy_cars_to_check.remove(enemy_car)

    def remove_off_screen_enemy_cars(self):
        self.game_objects.enemy_cars[:] = [car for car in self.game_objects.enemy_cars if car.y < SCREEN_HEIGHT]

    def add_new_enemy_cars(self):
        if random.randint(1, NEW_ENEMY_CAR_PROBABILITY) == 1:
            new_car = self.create_enemy_car()
            if new_car:
                self.game_objects.enemy_cars.append(new_car)
                self.enemy_cars_to_check.append(new_car)

    def move_and_draw_coins(self):
        for coin in self.game_objects.coins:
            coin.move(ENEMY_CAR_SPEED)
            if coin.check_collision(self.player):
                self.game_objects.coins.remove(coin)
                self.game_state.add_coin()
        self.game_objects.coins[:] = [coin for coin in self.game_objects.coins if coin.y < SCREEN_HEIGHT]
        if random.randint(1, NEW_COIN_PROBABILITY) == 1:
            self.game_objects.coins.append(self.create_coin())