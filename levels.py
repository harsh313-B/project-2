import pygame
from level import Platform, Goal

class Level:
    def __init__(self, platforms, goal_position, background_image):
        self.platforms = platforms
        self.goal_position = goal_position
        self.background_image = background_image

    def create_level(self):
        platforms = pygame.sprite.Group()
        for platform in self.platforms:
            platforms.add(Platform(*platform))
        goal = Goal(*self.goal_position)
        background = pygame.image.load(self.background_image).convert()
        return platforms, goal, background

# Define levels with their respective background images
levels = [
    Level(
        platforms=[
            (100, 400, 200, 20),
            (350, 300, 200, 20),
            (600, 200, 200, 20)
        ],
        goal_position=(700, 150),
        background_image="assets/level1_background.png"
    ),
    Level(
        platforms=[
            (50, 450, 150, 20),
            (250, 350, 150, 20),
            (450, 250, 150, 20),
            (650, 150, 150, 20)
        ],
        goal_position=(750, 100),
        background_image="assets/level2_background.png"
    ),
    Level(
        platforms=[
            (100, 500, 200, 20),
            (300, 400, 200, 20),
            (500, 300, 200, 20),
            (700, 200, 200, 20)
        ],
        goal_position=(800, 150),
        background_image="assets/level3_background.png"
    ),
    Level(
        platforms=[
            (150, 450, 200, 20),
            (350, 350, 200, 20),
            (550, 250, 200, 20),
            (750, 150, 200, 20)
        ],
        goal_position=(850, 100),
        background_image="assets/level4_background.png"
    ),
    Level(
        platforms=[
            (200, 400, 200, 20),
            (400, 300, 200, 20),
            (600, 200, 200, 20),
            (800, 100, 200, 20)
        ],
        goal_position=(900, 50),
        background_image="assets/level5_background.png"
    ),
    Level(
        platforms=[
            (250, 350, 200, 20),
            (450, 250, 200, 20),
            (650, 150, 200, 20),
            (850, 50, 200, 20)
        ],
        goal_position=(950, 0),
        background_image="assets/level6_background.png"
    )
]
