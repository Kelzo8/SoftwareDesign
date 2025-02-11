import pygame
import random
from car_factory import CarFactory
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Car Game")
        self.font = pygame.font.Font(None, 36)
        self.selected_car = None
        self.player_car_x = SCREEN_WIDTH // 2 - PLAYER_CAR_WIDTH // 2
        self.player_car_y = SCREEN_HEIGHT - PLAYER_CAR_HEIGHT - 10
        self.enemy_cars = []
        self.coins = []
        self.road_offset = 0
        self.running = True
        self.clock = pygame.time.Clock()
        self.coin_count = 0

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (x, y))

    def draw_car(self, x, y, car_type):
        if car_type == "ferrari":
            color = RED
        elif car_type == "porsche":
            color = GREEN
        elif car_type == "lambo":
            color = BLUE
        elif car_type == "enemy":
            color = BLACK
        pygame.draw.rect(self.screen, color, [x, y, PLAYER_CAR_WIDTH, PLAYER_CAR_HEIGHT])

    def draw_road(self):
        self.screen.fill(GREY)
        for i in range(NUM_LANES + 1):
            lane_x = i * LANE_WIDTH
            for j in range(0, SCREEN_HEIGHT, ROAD_LINE_HEIGHT + ROAD_LINE_GAP):
                pygame.draw.line(self.screen, WHITE, (lane_x, j + self.road_offset), (lane_x, j + ROAD_LINE_HEIGHT + self.road_offset), 2)
        self.road_offset = (self.road_offset + 5) % (ROAD_LINE_HEIGHT + ROAD_LINE_GAP)

    def create_enemy_car(self):
        lane = random.randint(0, NUM_LANES - 1)
        x = lane * LANE_WIDTH + (LANE_WIDTH - ENEMY_CAR_WIDTH) // 2
        y = -ENEMY_CAR_HEIGHT
        return [x, y]

    def create_coin(self):
        lane = random.randint(0, NUM_LANES - 1)
        x = lane * LANE_WIDTH + (LANE_WIDTH - PLAYER_CAR_WIDTH) // 2
        y = -PLAYER_CAR_HEIGHT
        return [x, y]

    def draw_coin(self, x, y):
        pygame.draw.circle(self.screen, (255, 215, 0), (x + PLAYER_CAR_WIDTH // 2, y + PLAYER_CAR_HEIGHT // 2), PLAYER_CAR_WIDTH // 4)

    def run(self):
        while self.running:
            if not self.selected_car:
                self.screen.fill(WHITE)
                # Draw car options
                for i, car in enumerate(["ferrari", "porsche", "lambo"]):
                    self.draw_text(f"{i + 1}. {car.capitalize()}", 50, 50 + i * 50)
            else:
                self.draw_road()
                self.draw_car(self.player_car_x, self.player_car_y, self.selected_car.__class__.__name__.lower())

                # Move enemy cars
                for enemy_car in self.enemy_cars:
                    enemy_car[1] += ENEMY_CAR_SPEED
                    self.draw_car(enemy_car[0], enemy_car[1], "enemy")

                    # Check for collision
                    if (self.player_car_y < enemy_car[1] + ENEMY_CAR_HEIGHT and
                        self.player_car_y + PLAYER_CAR_HEIGHT > enemy_car[1] and
                        self.player_car_x < enemy_car[0] + ENEMY_CAR_WIDTH and
                        self.player_car_x + PLAYER_CAR_WIDTH > enemy_car[0]):
                        self.draw_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        self.running = False

                # Remove off-screen enemy cars
                self.enemy_cars[:] = [car for car in self.enemy_cars if car[1] < SCREEN_HEIGHT]

                # Add new enemy cars
                if random.randint(1, 20) == 1:
                    self.enemy_cars.append(self.create_enemy_car())

                # Move coins
                for coin in self.coins:
                    coin[1] += ENEMY_CAR_SPEED
                    self.draw_coin(coin[0], coin[1])

                    # Check for coin collection
                    if (self.player_car_y < coin[1] + PLAYER_CAR_HEIGHT // 2 and
                        self.player_car_y + PLAYER_CAR_HEIGHT > coin[1] and
                        self.player_car_x < coin[0] + PLAYER_CAR_WIDTH // 2 and
                        self.player_car_x + PLAYER_CAR_WIDTH > coin[0]):
                        self.coins.remove(coin)
                        self.coin_count += 1

                # Remove off-screen coins
                self.coins[:] = [coin for coin in self.coins if coin[1] < SCREEN_HEIGHT]

                # Add new coins
                if random.randint(1, 50) == 1:
                    self.coins.append(self.create_coin())

                # Draw coin count
                pygame.draw.rect(self.screen, WHITE, [0, 0, 150, 50])
                pygame.draw.rect(self.screen, BLACK, [0, 0, 150, 50], 2)
                self.draw_text(f"Coins: {self.coin_count}", 10, 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_car = CarFactory.create_car("ferrari")
                    elif event.key == pygame.K_2:
                        self.selected_car = CarFactory.create_car("porsche")
                    elif event.key == pygame.K_3:
                        self.selected_car = CarFactory.create_car("lambo")

            keys = pygame.key.get_pressed()
            if self.selected_car:
                if keys[pygame.K_LEFT] and self.player_car_x > 0:
                    self.player_car_x -= PLAYER_CAR_SPEED
                if keys[pygame.K_RIGHT] and self.player_car_x < SCREEN_WIDTH - PLAYER_CAR_WIDTH:
                    self.player_car_x += PLAYER_CAR_SPEED
                if keys[pygame.K_UP] and self.player_car_y > 0:
                    self.player_car_y -= PLAYER_CAR_SPEED
                if keys[pygame.K_DOWN] and self.player_car_y < SCREEN_HEIGHT - PLAYER_CAR_HEIGHT:
                    self.player_car_y += PLAYER_CAR_SPEED

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()