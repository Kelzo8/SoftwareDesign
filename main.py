import pygame
from car_factory import CarFactory

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Factory")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Car options
car_options = ["ferrari", "porsche", "lambo"]
selected_car = None

def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def main():
    global selected_car
    running = True

    while running:
        screen.fill(WHITE)

        # Draw car options
        for i, car in enumerate(car_options):
            draw_text(f"{i + 1}. {car.capitalize()}", 50, 50 + i * 50)

        if selected_car:
            draw_text(f"Selected Car: {selected_car.drive()}", 50, 300)

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

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()