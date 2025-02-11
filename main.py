import pygame
import random
from car_factory import CarFactory

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Car options
car_options = ["ferrari", "porsche", "lambo"]
selected_car = None

# Player car settings
player_car_width = 50
player_car_height = 100
player_car_x = SCREEN_WIDTH // 2 - player_car_width // 2
player_car_y = SCREEN_HEIGHT - player_car_height - 10
player_car_speed = 5

# Enemy car settings
enemy_car_width = 50
enemy_car_height = 100
enemy_car_speed = 5
enemy_cars = []

def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def draw_car(x, y, color):
    pygame.draw.rect(screen, color, [x, y, player_car_width, player_car_height])

def create_enemy_car():
    x = random.randint(0, SCREEN_WIDTH - enemy_car_width)
    y = -enemy_car_height
    return [x, y]

def main():
    global selected_car, player_car_x, player_car_y
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Draw car options
        for i, car in enumerate(car_options):
            draw_text(f"{i + 1}. {car.capitalize()}", 50, 50 + i * 50)

        if selected_car:
            draw_text(f"Selected Car: {selected_car.drive()}", 50, 300)
            draw_car(player_car_x, player_car_y, RED)

            # Move enemy cars
            for enemy_car in enemy_cars:
                enemy_car[1] += enemy_car_speed
                draw_car(enemy_car[0], enemy_car[1], BLACK)

                # Check for collision
                if (player_car_y < enemy_car[1] + enemy_car_height and
                    player_car_y + player_car_height > enemy_car[1] and
                    player_car_x < enemy_car[0] + enemy_car_width and
                    player_car_x + player_car_width > enemy_car[0]):
                    draw_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False

            # Remove off-screen enemy cars
            enemy_cars[:] = [car for car in enemy_cars if car[1] < SCREEN_HEIGHT]

            # Add new enemy cars
            if random.randint(1, 20) == 1:
                enemy_cars.append(create_enemy_car())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_car = CarFactory.create_car("ferrari")
                elif event.key == pygame.K_2:
                    selected_car = CarFactory.create_car("porsche")
                elif event.key == pygame.K_3:
                    selected_car = CarFactory.create_car("lambo")

        keys = pygame.key.get_pressed()
        if selected_car:
            if keys[pygame.K_LEFT] and player_car_x > 0:
                player_car_x -= player_car_speed
            if keys[pygame.K_RIGHT] and player_car_x < SCREEN_WIDTH - player_car_width:
                player_car_x += player_car_speed
            if keys[pygame.K_UP] and player_car_y > 0:
                player_car_y -= player_car_speed
            if keys[pygame.K_DOWN] and player_car_y < SCREEN_HEIGHT - player_car_height:
                player_car_y += player_car_speed

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()