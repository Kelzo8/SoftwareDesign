# command.py
from abc import ABC, abstractmethod
from settings import SCREEN_WIDTH, PLAYER_CAR_SPEED, SCREEN_HEIGHT, CarDimensions

# Use CarDimensions enum for player car dimensions
PLAYER_CAR_WIDTH = CarDimensions.PLAYER_CAR_WIDTH.value
PLAYER_CAR_HEIGHT = CarDimensions.PLAYER_CAR_HEIGHT.value

class Command(ABC):
    @abstractmethod
    def execute(self, **params):
        pass
    def reset(self):
        pass

class MoveLeftCommand(Command):
    def execute(self, **params):
        player = params.get('player')
        if player.car_x > 0:
            player.car_x -= PLAYER_CAR_SPEED  # Define PLAYER_CAR_SPEED in settings.py

class MoveRightCommand(Command):
    def execute(self, **params):
        player = params.get('player')
        if player.car_x < SCREEN_WIDTH - PLAYER_CAR_WIDTH:
            player.car_x += PLAYER_CAR_SPEED

class MoveUpCommand(Command):
    def execute(self, **params):
        player = params.get('player')
        if player.car_y > 0:
            player.car_y -= PLAYER_CAR_SPEED

class MoveDownCommand(Command):
    def execute(self, **params):
        player = params.get('player')
        if player.car_y < SCREEN_HEIGHT - PLAYER_CAR_HEIGHT:
            player.car_y += PLAYER_CAR_SPEED

class CheckPointCommand(Command):
    def __init__(self):
        self.key_pressed = False

    def execute(self, **params):
        model = params.get('model')
        if not self.key_pressed:
            model.save_checkpoint()
            self.key_pressed = True

    def reset(self):
        self.key_pressed = False