from abc import ABC, abstractmethod
from settings import CarDimensions as cd

class Interceptor(ABC):
    @abstractmethod
    def intercept(self, player_car, enemy_car):
        pass

class NearMissInterceptor(Interceptor):
    def __init__(self):
        self.near_miss_count = 0

    def intercept(self, player_car, enemy_car):
        # Buffer for near miss detection
        buffer = 20
        if (player_car[1] < enemy_car[1] + cd.ENEMY_CAR_HEIGHT.value + buffer and
            player_car[1] + cd.PLAYER_CAR_HEIGHT.value > enemy_car[1] - buffer and
            player_car[0] < enemy_car[0] + cd.ENEMY_CAR_WIDTH.value + buffer and
            player_car[0] + cd.PLAYER_CAR_WIDTH.value > enemy_car[0] - buffer):
            # Ensure it's not a collision
            if not (player_car[1] < enemy_car[1] + cd.ENEMY_CAR_HEIGHT.value and
                    player_car[1] + cd.PLAYER_CAR_HEIGHT.value > enemy_car[1] and
                    player_car[0] < enemy_car[0] + cd.ENEMY_CAR_WIDTH.value and
                    player_car[0] + cd.PLAYER_CAR_WIDTH.value > enemy_car[0]):
                self.near_miss_count += 1
                print(f"Near miss detected! Player car: {player_car}, Enemy car: {enemy_car}, Near misses: {self.near_miss_count}")
        else:
            print(f"No near miss. Player car: {player_car}, Enemy car: {enemy_car}")

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