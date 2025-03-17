import pygame
from settings import CarDimensions as cd
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, speed):
        self.y += speed

    def draw(self, ui):
        ui.draw_coin(self.x, self.y)
    def check_collision(self, player):
        return (player.car_y < self.y + cd.PLAYER_CAR_HEIGHT.value // 2 and
                player.car_y + cd.PLAYER_CAR_HEIGHT.value > self.y and
                player.car_x < self.x + cd.PLAYER_CAR_WIDTH.value // 2 and
                player.car_x + cd.PLAYER_CAR_WIDTH.value > self.x)