# FILE: player.py (Python)
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.load_sprites([
            "assets/character_malePerson_run0.png",
            "assets/character_malePerson_run1.png",
            "assets/character_malePerson_run2.png"
        ])
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Movement Variables
        self.speed = 5
        self.gravity = 0.5
        self.jump_power = -10
        self.direction = pygame.Vector2(0, 0)
        self.on_ground = False

    def load_sprites(self, file_paths):
        for file_path in file_paths:
            frame = pygame.image.load(file_path).convert_alpha()
            self.sprites.append(frame)

    def update(self, keys, platforms):
        # Left/Right Movement
        self.direction.x = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        self.rect.x += self.direction.x * self.speed  # Apply movement

        # Jumping & Gravity
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_power
            self.on_ground = False

        self.direction.y += self.gravity  # Apply gravity
        self.rect.y += self.direction.y  # Apply vertical movement

        # Collision with Platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.direction.y > 0:
                self.rect.bottom = platform.rect.top
                self.direction.y = 0
                self.on_ground = True

        # Animation Update
        if self.direction.x != 0:
            self.current_frame = (self.current_frame + 0.1) % len(self.sprites)
            self.image = self.sprites[int(self.current_frame)]
        else:
            self.current_frame = 0
            self.image = self.sprites[self.current_frame]
