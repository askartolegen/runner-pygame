import sqlite3
import pygame
from random import randint


class Database:
    __instance = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if Database.__instance is None:
            Database.__instance = super().__new__(cls)
        return Database.__instance

    def __del__(self):
        Database.__instance = None

    def __init__(self):
        self.connection = sqlite3.connect("aquarium.db")
        self.cursor = self.connection.cursor()
        if Database.__instance is None:
            self.cursor.execute("CREATE TABLE runner (name TEXT, score INTEGER)")

    def add_player(self, name_, score_):
        params = (name_, score_)
        self.cursor.execute("INSERT INTO runner (name, score) VALUES (?, ?)", params)

    def get_data(self):
        rows = self.cursor.execute("SELECT name, score FROM runner order by score desc limit 5").fetchall()
        return rows

    def update_data(self, name_, score_):
        params = (str(score_), name_)
        self.cursor.execute("UPDATE runner SET score = ? WHERE name = ?", params)

    def commit(self):
        self.connection.commit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/soldier_run_1.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.5)

        player_walk_2 = pygame.image.load('graphics/Player/soldier_run_2.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.5)

        player_walk_3 = pygame.image.load('graphics/Player/soldier_run_3.png').convert_alpha()
        player_walk_3 = pygame.transform.rotozoom(player_walk_3, 0, 0.5)

        player_walk_4 = pygame.image.load('graphics/Player/soldier_run_4.png').convert_alpha()
        player_walk_4 = pygame.transform.rotozoom(player_walk_4, 0, 0.5)

        player_walk_5 = pygame.image.load('graphics/Player/soldier_run_5.png').convert_alpha()
        player_walk_5 = pygame.transform.rotozoom(player_walk_5, 0, 0.5)

        player_walk_6 = pygame.image.load('graphics/Player/soldier_run_6.png').convert_alpha()
        player_walk_6 = pygame.transform.rotozoom(player_walk_6, 0, 0.5)
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6]
        self.player_index = 0

        player_jump = pygame.image.load('graphics/Player/soldier_jump.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(player_jump, 0, 0.65)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def reset(self):
        pass


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        if obstacle_type == 'rocket':
            rocket = pygame.image.load('graphics/rocket.png').convert_alpha()
            rocket = pygame.transform.scale(rocket, (72, 36))
            self.frames = [rocket]
            y_pos = 180
        else:
            mine = pygame.image.load('graphics/mine.png').convert_alpha()
            mine = pygame.transform.scale(mine, (54, 18))
            self.frames = [mine]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
