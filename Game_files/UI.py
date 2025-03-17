import pygame
import random
from settings import *
import time
from settings import CarDimensions as cd

class UI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (x, y))

    def draw_car(self, x, y, car):
        car_image = pygame.image.load(car.get_image()).convert_alpha()
        car_image = pygame.transform.scale(car_image, (cd.PLAYER_CAR_WIDTH.value, cd.PLAYER_CAR_HEIGHT.value))
        self.screen.blit(car_image, (x, y))

    def draw_road(self, road_offset):
        self.screen.fill(GREY)
        for i in range(NUM_LANES + 1):
            lane_x = i * LANE_WIDTH
            for j in range(0, SCREEN_HEIGHT, ROAD_LINE_HEIGHT + ROAD_LINE_GAP):
                pygame.draw.line(self.screen, WHITE, (lane_x, j + road_offset), 
                                 (lane_x, j + ROAD_LINE_HEIGHT + road_offset), 2)

    def draw_coin(self, x, y):
        pygame.draw.circle(self.screen, (255, 215, 0), (x + cd.PLAYER_CAR_WIDTH.value // 2, y + cd.PLAYER_CAR_HEIGHT.value // 2), 
                           cd.PLAYER_CAR_WIDTH.value // 4)

    def draw_name_input(self, player_name):
        self.screen.fill((240, 240, 245))  # Light blue-gray background
        
        # Title box with shadow
        title_box_width = 400
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        [SCREEN_WIDTH/2 - title_box_width/2 + 5, 105, 
                         title_box_width, 70])
        pygame.draw.rect(self.screen, WHITE,
                        [SCREEN_WIDTH/2 - title_box_width/2, 100, 
                         title_box_width, 70])
        
        # Title
        title = self.font.render("ENTER YOUR NAME", True, (50, 50, 50))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 135))
        self.screen.blit(title, title_rect)
        
        # Input box with shadow
        input_box_width = 300
        input_box_height = 50
        pygame.draw.rect(self.screen, (200, 200, 200),
                        [SCREEN_WIDTH/2 - input_box_width/2 + 5, 255,
                         input_box_width, input_box_height])
        pygame.draw.rect(self.screen, WHITE,
                        [SCREEN_WIDTH/2 - input_box_width/2, 250,
                         input_box_width, input_box_height])
        pygame.draw.rect(self.screen, (100, 100, 100),
                        [SCREEN_WIDTH/2 - input_box_width/2, 250,
                         input_box_width, input_box_height], 2)
        
        # Name text
        name_text = self.font.render(player_name + ("_" if time.time() % 1 > 0.5 else ""), 
                                    True, (50, 50, 50))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH/2, 275))
        self.screen.blit(name_text, name_rect)
        
        # Instructions
        inst = self.font.render("Press ENTER when done", True, (100, 100, 100))
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH/2, 350))
        self.screen.blit(inst, inst_rect)

    def draw_replay_quit_buttons(self):
        # Define button properties
        button_width = 200
        button_height = 50
        replay_button_x = SCREEN_WIDTH / 2 - button_width - 10
        quit_button_x = SCREEN_WIDTH / 2 + 10
        button_y = SCREEN_HEIGHT / 2 + 150  # Adjusted to move up by 20 pixels

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine button colors based on hover
        replay_color = LIGHT_GRAY if replay_button_x <= mouse_pos[0] <= replay_button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height else WHITE
        quit_color = LIGHT_GRAY if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height else WHITE

        # Draw replay button
        pygame.draw.rect(self.screen, replay_color, [replay_button_x, button_y, button_width, button_height])
        pygame.draw.rect(self.screen, BLACK, [replay_button_x, button_y, button_width, button_height], 2)
        replay_text = self.font.render("Replay", True, BLACK)
        replay_rect = replay_text.get_rect(center=(replay_button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(replay_text, replay_rect)

        # Draw quit button
        pygame.draw.rect(self.screen, quit_color, [quit_button_x, button_y, button_width, button_height])
        pygame.draw.rect(self.screen, BLACK, [quit_button_x, button_y, button_width, button_height], 2)
        quit_text = self.font.render("Quit", True, BLACK)
        quit_rect = quit_text.get_rect(center=(quit_button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(quit_text, quit_rect)

    def draw_car_selection(self):
        self.screen.fill((240, 240, 245))
        
        # Title with decorative elements
        pygame.draw.rect(self.screen, WHITE, [150, 50, 500, 80])
        pygame.draw.rect(self.screen, (200, 200, 200), [155, 55, 500, 80], 3)
        title = self.font.render("SELECT YOUR CAR", True, (50, 50, 50))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 90))
        self.screen.blit(title, title_rect)
        
        cars = [("Red Ferrari", RED), ("Blue Porsche", BLUE), ("Green Lambo", GREEN)]
        
        for i, (car_name, color) in enumerate(cars):
            # Calculate positions
            box_width = 220
            box_height = 180
            margin = 20
            total_width = (box_width + margin) * len(cars)
            start_x = (SCREEN_WIDTH - total_width) / 2
            box_x = start_x + i * (box_width + margin)
            box_y = 200
            
            # Draw card shadow
            pygame.draw.rect(self.screen, (200, 200, 200),
                            [box_x + 5, box_y + 5, box_width, box_height])
            
            # Draw card background
            pygame.draw.rect(self.screen, WHITE,
                            [box_x, box_y, box_width, box_height])
            
            # Highlight on hover
            mouse_pos = pygame.mouse.get_pos()
            if (box_x <= mouse_pos[0] <= box_x + box_width and 
                box_y <= mouse_pos[1] <= box_y + box_height):
                pygame.draw.rect(self.screen, color,
                               [box_x, box_y, box_width, box_height], 4)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100),
                               [box_x, box_y, box_width, box_height], 2)
            
            # Draw car preview
            car_rect = pygame.draw.rect(self.screen, color,
                                      [box_x + box_width/2 - cd.PLAYER_CAR_WIDTH.value/2,
                                       box_y + 40,
                                       cd.PLAYER_CAR_WIDTH.value,
                                       cd.PLAYER_CAR_HEIGHT.value])
            
            # Car name
            name_text = self.font.render(car_name, True, (50, 50, 50))
            name_rect = name_text.get_rect(center=(box_x + box_width/2, box_y + 120))
            self.screen.blit(name_text, name_rect)
            
            # Key instruction
            key_text = self.font.render(f"Press {i+1}", True, (100, 100, 100))
            key_rect = key_text.get_rect(center=(box_x + box_width/2, box_y + 150))
            self.screen.blit(key_text, key_rect)

    def handle_car_selection_click(self, mouse_pos):
        cars = ["ferrari", "lambo", "porsche"]
        box_width = 220
        box_height = 180
        margin = 20
        total_width = (box_width + margin) * len(cars)
        start_x = (SCREEN_WIDTH - total_width) / 2
        box_y = 200

        for i, car_name in enumerate(cars):
            box_x = start_x + i * (box_width + margin)
            if (box_x <= mouse_pos[0] <= box_x + box_width and 
                box_y <= mouse_pos[1] <= box_y + box_height):
                return car_name
        return None

    def display_leaderboard(self, leaderboard, current_score):
        # Background
        self.screen.fill((240, 240, 245))
        
        # Game Over Title - moved up
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("GAME OVER", True, (50, 50, 50))
        title_rect = title.get_rect(center=(self.screen.get_width()/2, 50))  # Changed from 80
        self.screen.blit(title, title_rect)
        
        # Leaderboard Title - moved up
        subtitle = self.font.render("LEADERBOARD", True, (50, 50, 50))
        subtitle_rect = subtitle.get_rect(center=(self.screen.get_width()/2, 100))  # Changed from 130
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw decorative line - moved up
        pygame.draw.line(self.screen, (200, 200, 200),
                        (self.screen.get_width()/4, 130),  # Changed from 160
                        (self.screen.get_width()*3/4, 130), 3)
        
        # Start leaderboard entries higher up
        y_offset = 150  # Changed from 200
        
        # Reduce spacing between entries
        spacing = 5  # Changed from 10
        box_height = 50  # Changed from 60

        # Display scores with reduced spacing
        for i, (name, score) in enumerate(leaderboard.scores[:5]):
            box_width = 400
            box_x = self.screen.get_width()/2 - box_width/2
            
            # Draw box shadow
            pygame.draw.rect(self.screen, (200, 200, 200),
                            [box_x+5, y_offset+5, box_width, box_height])
            
            # Draw main box
            pygame.draw.rect(self.screen, WHITE,
                            [box_x, y_offset, box_width, box_height])
            
            # Position number
            position = self.font.render(f"#{i + 1}", True, (50, 50, 50))
            self.screen.blit(position, (box_x + 20, y_offset + 10))
            
            # Player name
            name_text = self.font.render(name, True, (50, 50, 50))
            self.screen.blit(name_text, (box_x + 80, y_offset + 10))
            
            # Score
            score_text = self.font.render(f"{score} coins", True, GOLD)
            self.screen.blit(score_text, (box_x + box_width - 120, y_offset + 10))
            
            y_offset += box_height + spacing

        # Current score display with fixed position from bottom
        if current_score is not None:
            score_box_height = 80
            score_box_width = 300
            score_box_x = self.screen.get_width()/2 - score_box_width/2
            score_box_y = SCREEN_HEIGHT - 120  # Changed from 150 to move it lower

            # Box shadow
            pygame.draw.rect(self.screen, (180, 180, 180),
                            [score_box_x+8, score_box_y+8, score_box_width, score_box_height])

            # Main box
            pygame.draw.rect(self.screen, (245, 245, 255),
                            [score_box_x, score_box_y, score_box_width, score_box_height])
            pygame.draw.rect(self.screen, GOLD,
                            [score_box_x, score_box_y, score_box_width, score_box_height], 3)

            # "Your Score" label
            label_font = pygame.font.Font(None, 42)
            your_score_label = label_font.render("Your Score", True, (50, 50, 50))
            label_rect = your_score_label.get_rect(centerx=self.screen.get_width()/2, 
                                                 top=score_box_y + 10)
            self.screen.blit(your_score_label, label_rect)

            # Score number
            score_font = pygame.font.Font(None, 60)
            score_text = score_font.render(f"{current_score} coins", True, GOLD)
            score_rect = score_text.get_rect(centerx=self.screen.get_width()/2,
                                           top=score_box_y + 40)
            self.screen.blit(score_text, score_rect)

    def draw_coin_count(self, coin_count):
        pygame.draw.rect(self.screen, WHITE, [0, 0, 150, 50])
        pygame.draw.rect(self.screen, BLACK, [0, 0, 150, 50], 2)
        self.draw_text(f"Coins: {coin_count}", 10, 10)
        self.draw_text(f"Coins: {coin_count}", 10, 10)

    def draw_near_miss_count(self, near_miss_count):
        text = f"Near Misses: {near_miss_count}"
        text_surface = self.font.render(text, True, BLACK)
        text_width, text_height = text_surface.get_size()
        padding = 10  # Reduced padding for better visibility
        box_width = text_width + 2 * padding
        box_height = text_height + 2 * padding
        x_position = SCREEN_WIDTH - box_width - padding  # Adjusted position
        y_position = padding
        
        pygame.draw.rect(self.screen, WHITE, [x_position, y_position, box_width, box_height])
        pygame.draw.rect(self.screen, BLACK, [x_position, y_position, box_width, box_height], 2)
        self.screen.blit(text_surface, (x_position + padding, y_position + padding))
    
    def draw_immunity_timer(self, remaining_time):
        timer_text = f"Immunity: {remaining_time:.1f}s"
        text_surface = self.font.render(timer_text, True, (255, 0, 0))  # Red color for visibility
        text_width, text_height = text_surface.get_size()
        padding = 10
        box_width = text_width + 2 * padding
        box_height = text_height + 2 * padding
        x_position = (SCREEN_WIDTH - box_width) / 2  # Centered position
        y_position = padding
        pygame.draw.rect(self.screen, WHITE, [x_position, y_position, box_width, box_height])
        pygame.draw.rect(self.screen, BLACK, [x_position, y_position, box_width, box_height], 2)
        self.screen.blit(text_surface, (x_position + padding, y_position + padding))