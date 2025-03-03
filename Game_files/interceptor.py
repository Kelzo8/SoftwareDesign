from abc import ABC, abstractmethod
from settings import CarDimensions as cd

class Interceptor(ABC):
    @abstractmethod
    def intercept(self, player_car, enemy_car):
        pass

class NearMissInterceptor(Interceptor):
    def __init__(self):
        self.near_miss_count = 0

    def intercept(self, player_car_pos, enemy_car_pos):
        player_x, player_y = player_car_pos
        enemy_x, enemy_y = enemy_car_pos

        # Define a buffer for near miss detection
        buffer = 1

        # Check for near miss
        if (abs(player_x - enemy_x) < cd.PLAYER_CAR_WIDTH.value + buffer and
            abs(player_y - enemy_y) < cd.PLAYER_CAR_HEIGHT.value + buffer):
            self.near_miss_count += 1

    def get_near_miss_count(self):
        return self.near_miss_count

class InterceptorDispatcher:
    def __init__(self):
        self.interceptors = []

    def register_interceptor(self, interceptor):
        self.interceptors.append(interceptor)

    def execute_interceptors(self, player_car, enemy_car):
        for interceptor in self.interceptors:
            interceptor.intercept(player_car, enemy_car) 