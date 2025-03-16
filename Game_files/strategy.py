import random
from abc import ABC, abstractmethod
from settings import *
from settings import CarDimensions as cd

class MovementStrategy(ABC):
    @abstractmethod
    def move(self, car, player_x, other_cars, coin_count):
        """
        Move the car given the player's x position, list of other enemy cars,
        and the player's coin count.
        """
        pass

class StraightMovement(MovementStrategy):
    def move(self, car, player_x, other_cars, coin_count):
        # Moves straight down.
        car.y += car.speed

class ZigZagMovement(MovementStrategy):
    def move(self, car, player_x, other_cars, coin_count):
        # Always move down.
        car.y += car.speed
        # Only attempt lane changes if the player has 5 or more coins.
        if coin_count >= 5:
            # Lower chance of lane change for smoother, more predictable behavior.
            if random.random() < 0.02:  # Was 0.05 before.
                lane_change = random.choice([-1, 1])
                target_x = car.x + lane_change * LANE_WIDTH
                # Check boundaries.
                if 0 <= target_x <= SCREEN_WIDTH - cd.ENEMY_CAR_WIDTH.value:
                    # Ensure no collision with other enemy cars.
                    if not any(
                        abs(other.x - target_x) < cd.ENEMY_CAR_WIDTH.value and
                        abs(other.y - car.y) < cd.ENEMY_CAR_HEIGHT.value
                        for other in other_cars if other != car
                    ):
                        # Gradually adjust the car's x position for a smoother lane change.
                        car.x += (target_x - car.x) * 0.25  # Reduced from 0.5 to 0.25.

class ChaseMovement(MovementStrategy):
    def move(self, car, player_x, other_cars, coin_count):
        # Always move down.
        car.y += car.speed
        # Only adjust lane toward the player when coin count is at least 5.
        if coin_count >= 5:
            # Lower chance to adjust lane.
            if random.random() < 0.01:  # Was 0.02 before.
                direction = 1 if player_x > car.x else -1
                target_x = car.x + direction * LANE_WIDTH
                if 0 <= target_x <= SCREEN_WIDTH - cd.ENEMY_CAR_WIDTH.value:
                    if not any(
                        abs(other.x - target_x) < cd.ENEMY_CAR_WIDTH.value and
                        abs(other.y - car.y) < cd.ENEMY_CAR_HEIGHT.value
                        for other in other_cars if other != car
                    ):
                        # Gradually adjust the car's x position.
                        car.x += (target_x - car.x) * 0.25  # Reduced from 0.5 to 0.25.

class EnemyCar:
    def __init__(self, x, y, speed, strategy, car_type='enemy'):
        self.x = x
        self.y = y
        self.speed = speed
        self.strategy = strategy
        self.car_type = car_type

    def move(self, player_x, enemy_cars, coin_count):
        self.strategy.move(self, player_x, enemy_cars, coin_count)

    def draw(self, ui):
        ui.draw_car(self.x, self.y, self.car_type)
