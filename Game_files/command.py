# command.py
from abc import ABC, abstractmethod
from settings import SCREEN_WIDTH, PLAYER_CAR_SPEED, SCREEN_HEIGHT, CarDimensions

# Use CarDimensions enum for player car dimensions
PLAYER_CAR_WIDTH = CarDimensions.PLAYER_CAR_WIDTH.value
PLAYER_CAR_HEIGHT = CarDimensions.PLAYER_CAR_HEIGHT.value

class Command(ABC):
    @abstractmethod
    def execute(self, game):
        pass

class MoveLeftCommand(Command):
    def execute(self, game):
        if game.player_car_x > 0:
            game.player_car_x -= PLAYER_CAR_SPEED  # Define PLAYER_CAR_SPEED in settings.py

class MoveRightCommand(Command):
    def execute(self, game):
        if game.player_car_x < SCREEN_WIDTH - PLAYER_CAR_WIDTH:
            game.player_car_x += PLAYER_CAR_SPEED

class MoveUpCommand(Command):
    def execute(self, game):
        if game.player_car_y > 0:
            game.player_car_y -= PLAYER_CAR_SPEED

class MoveDownCommand(Command):
    def execute(self, game):
        if game.player_car_y < SCREEN_HEIGHT - PLAYER_CAR_HEIGHT:
            game.player_car_y += PLAYER_CAR_SPEED
