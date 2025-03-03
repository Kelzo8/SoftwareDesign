from abc import ABC, abstractmethod

class Interceptor(ABC):
    @abstractmethod
    def intercept(self, player_car, enemy_car):
        pass

class NearMissInterceptor(Interceptor):
    def __init__(self):
        self.near_miss_count = 0

    def intercept(self, player_car, enemy_car):
        # Increase the margin for a near miss
        near_miss_margin = 10  # Adjusted margin
        if (abs(player_car[0] - enemy_car[0]) < near_miss_margin and
            abs(player_car[1] - enemy_car[1]) < near_miss_margin):
            self.near_miss_count += 1

    def get_near_miss_count(self):
        return self.near_miss_count 