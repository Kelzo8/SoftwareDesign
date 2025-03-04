from abc import ABC, abstractmethod
from settings import CarDimensions as cd

class Interceptor(ABC):
    @abstractmethod
    def intercept(self, player_car, enemy_car):
        pass

class NearMissInterceptor(Interceptor):
    def __init__(self):
        self.near_miss_count = 0
        self.counted_vehicles = []  # Track counted vehicles

    def intercept(self, player_pos, enemy_pos):
        player_x, player_y = player_pos
        enemy_x, enemy_y = enemy_pos
        buffer = 1  # Buffer for near miss detection

        # Create a unique identifier for the enemy vehicle
        enemy_id = (enemy_x, enemy_y)

        # Check for near miss
        if (abs(player_x - enemy_x) < cd.PLAYER_CAR_WIDTH.value + buffer and
            abs(player_y - enemy_y) < cd.PLAYER_CAR_HEIGHT.value + buffer):
            if not (abs(player_x - enemy_x) < cd.PLAYER_CAR_WIDTH.value and
                    abs(player_y - enemy_y) < cd.PLAYER_CAR_HEIGHT.value):
                if enemy_id not in self.counted_vehicles:
                    self.near_miss_count += 1
                    self.counted_vehicles.append(enemy_id)

    def get_near_miss_count(self):
        return self.near_miss_count

    def remove_off_screen_vehicles(self, enemy_cars):
        # Remove vehicles that are no longer on screen from the set
        self.counted_vehicles = [enemy_id for enemy_id in self.counted_vehicles if enemy_id in enemy_cars]

class InterceptorDispatcher:
    def __init__(self):
        self.interceptors = []

    def register_interceptor(self, interceptor):
        self.interceptors.append(interceptor)

    def execute_interceptors(self, player_car, enemy_car):
        for interceptor in self.interceptors:
            interceptor.intercept(player_car, enemy_car) 