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

    def intercept(self, player_car, enemy_car):
        # Extract player's position.
        if hasattr(player_car, 'x') and hasattr(player_car, 'y'):
            player_x, player_y = player_car.x, player_car.y
        else:
            player_x, player_y = player_car

        # Extract enemy's position.
        if hasattr(enemy_car, 'x') and hasattr(enemy_car, 'y'):
            enemy_x, enemy_y = enemy_car.x, enemy_car.y
        else:
            enemy_x, enemy_y = enemy_car

        buffer = 1  # Buffer for near miss detection

        # Create a unique identifier for the enemy vehicle.
        enemy_id = (enemy_x, enemy_y)

        # Check for near miss: the enemy is within a slightly larger area than a full collision,
        # but not a full collision.
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
        # Remove vehicles that are no longer on screen from the counted list.
        # Here, enemy_cars can be a list of EnemyCar objects or positions.
        valid_ids = []
        for car in enemy_cars:
            if hasattr(car, 'x') and hasattr(car, 'y'):
                valid_ids.append((car.x, car.y))
            else:
                valid_ids.append(car)
        self.counted_vehicles = [enemy_id for enemy_id in self.counted_vehicles if enemy_id in valid_ids]

class InterceptorDispatcher:
    def __init__(self):
        self.interceptors = []

    def register_interceptor(self, interceptor):
        self.interceptors.append(interceptor)

    def execute_interceptors(self, player_car, enemy_car):
        for interceptor in self.interceptors:
            interceptor.intercept(player_car, enemy_car)
