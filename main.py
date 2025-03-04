# FILE: main.py (Python)
import pygame
import sqlite3
from player import Player
from level import Platform, Goal
from database import Database  # Import Database
from levels import levels  # Import levels

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Quest")

# Initialize Database
db = Database()
current_level = db.get_latest_level()  # Load last saved level

# Initialize Player & Objects
def load_level(level_index):
    level = levels[level_index]
    platforms, goal, background = level.create_level()
    player = Player(100, HEIGHT - 150)
    all_sprites = pygame.sprite.Group(player, goal, *platforms)
    return player, goal, platforms, all_sprites, background

try:
    player, goal, platforms, all_sprites, background = load_level(current_level - 1)
except Exception as e:
    print(f"Error loading level: {e}")
    pygame.quit()
    exit()

# Function to display score and time taken
def display_score_and_time(score, time_taken):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render(f"Level Complete!", True, (0, 255, 0))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    time_text = font.render(f"Time Taken: {time_taken:.2f} seconds", True, BLACK)
    screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.update()
    pygame.time.delay(3000)  # Display for 3 seconds

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# TextBox Class
class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 0, 0) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.fill(self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, BLACK, self.rect, 2)

def sign_up_screen():
    username_box = TextBox(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
    password_box = TextBox(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    sign_up_button = Button("Sign Up", WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, lambda: sign_up(username_box.text, password_box.text))

    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            username_box.handle_event(event)
            password_box.handle_event(event)
            sign_up_button.handle_event(event)

        username_box.draw(screen)
        password_box.draw(screen)
        sign_up_button.draw(screen)

        pygame.display.flip()

def login_screen():
    username_box = TextBox(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
    password_box = TextBox(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    login_button = Button("Login", WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, lambda: login(username_box.text, password_box.text))

    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            username_box.handle_event(event)
            password_box.handle_event(event)
            login_button.handle_event(event)

        username_box.draw(screen)
        password_box.draw(screen)
        login_button.draw(screen)

        pygame.display.flip()

def sign_up(username, password):
    db.add_user(username, password)
    print("User signed up:", username)

def login(username, password):
    if db.check_user(username, password):
        print("User logged in:", username)
        global in_home_screen
        in_home_screen = False
    else:
        print("Invalid credentials")

# Home Screen
def home_screen():
    def start_game():
        global running, in_home_screen
        in_home_screen = False

    start_button = Button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50, start_game)
    login_button = Button("Login", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, login_screen)
    sign_up_button = Button("Sign Up", WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, sign_up_screen)

    buttons = [start_button, login_button, sign_up_button]

    while in_home_screen:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        # Draw Title
        font = pygame.font.Font(None, 74)
        title_surf = font.render("Code Quest", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_surf, title_rect)

        # Draw Buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                return
            for button in buttons:
                button.handle_event(event)

# Main Game Loop
clock = pygame.time.Clock()
running = True
in_home_screen = True
score = 0
start_time = pygame.time.get_ticks()

while running:
    if in_home_screen:
        home_screen()
    else:
        clock.tick(FPS)
        screen.blit(background, (0, 0))  # Draw the background image

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player Movement
        keys = pygame.key.get_pressed()
        player.update(keys, platforms)

        # Check if Player Reaches Goal
        if pygame.sprite.collide_rect(player, goal):
            end_time = pygame.time.get_ticks()
            time_taken = (end_time - start_time) / 1000  # Convert to seconds
            score += 100  # Increment score (example logic)
            display_score_and_time(score, time_taken)
            db.save_progress(current_level + 1)  # Move to next level
            current_level += 1
            if current_level > len(levels):
                print("Congratulations! You've completed all levels!")
                running = False
            else:
                try:
                    player, goal, platforms, all_sprites, background = load_level(current_level - 1)
                except Exception as e:
                    print(f"Error loading level: {e}")
                    running = False
                start_time = pygame.time.get_ticks()  # Reset start time for next level

        # Draw Everything
        all_sprites.update()  # Ensure all sprites are updated
        all_sprites.draw(screen)
        pygame.display.flip()  # Update the display

# Close Database & Pygame
db.close()
pygame.quit()
