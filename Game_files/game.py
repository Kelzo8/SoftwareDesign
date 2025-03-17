import pygame
from settings import *
from .UI import UI
from .model import GameModel
from .game_controller import GameController
from settings import CarDimensions as cd

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Car Game")
        self.font = pygame.font.Font(None, 36)
        self.ui = UI(self.screen, self.font)
        self.model = GameModel()
        self.controller = GameController(self.model, self.ui)
        self.clock = pygame.time.Clock()

    def run(self):
        self.model.player.name = self.model.game_state.player_name
        name_entered = bool(self.model.player.name)

        while not name_entered and self.model.game_state.is_running:
            self.ui.draw_name_input(self.model.player.name)
            name_entered = self.controller.handle_name_input()
            pygame.display.flip()
            self.clock.tick(60)

        while self.model.game_state.is_running:
            self.screen.fill(WHITE)
            if not self.model.player.selected_car:
                self.controller.handle_car_selection()
            else:
                self.update_game_state()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def update_game_state(self):
        self.ui.draw_road(self.model.game_objects.road_offset)
        self.ui.draw_car(self.model.player.car_x, self.model.player.car_y, self.model.player.selected_car)
        self.controller.update_game_state()
        self.ui.draw_coin_count(self.model.game_state.coin_count)
        self.ui.draw_near_miss_count(self.model.near_miss_interceptor.get_near_miss_count())