import pygame
import sqlite3
from sys import exit
from random import randint, choice


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
        if Database.cursor is None:
            connection = sqlite3.connect("aquarium.db")
            self.cursor = connection.cursor()

    def add_player(self, name, score_):
        params = (name, score_)
        self.cursor.execute("INSERT INTO runner (name, score) VALUES (?, ?)", params)

    def get_data(self):
        rows = self.cursor.execute("SELECT name, score FROM runner order by score desc limit 5").fetchall()
        return rows


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/soldier_run_1.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.5)

        player_walk_2 = pygame.image.load('graphics/soldier_run_2.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.5)

        player_walk_3 = pygame.image.load('graphics/soldier_run_3.png').convert_alpha()
        player_walk_3 = pygame.transform.rotozoom(player_walk_3, 0, 0.5)

        player_walk_4 = pygame.image.load('graphics/soldier_run_4.png').convert_alpha()
        player_walk_4 = pygame.transform.rotozoom(player_walk_4, 0, 0.5)

        player_walk_5 = pygame.image.load('graphics/soldier_run_5.png').convert_alpha()
        player_walk_5 = pygame.transform.rotozoom(player_walk_5, 0, 0.5)

        player_walk_6 = pygame.image.load('graphics/soldier_run_6.png').convert_alpha()
        player_walk_6 = pygame.transform.rotozoom(player_walk_6, 0, 0.5)
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6]
        self.player_index = 0

        player_jump = pygame.image.load('graphics/soldier_jump.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(player_jump, 0, 0.65)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
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


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def display_text(data):
    tb = data[:]
    x, y = 550, 50
    word_surface = test_font.render('Top 5 players:', True, (64, 64, 64))
    screen.blit(word_surface, (x, y))

    if len(tb) < 5:
        tb = tb + [('None', 0)] * (5 - len(tb))

    for lines in tb:
        word_surface = test_font.render(f"{lines[0]}: {lines[1]}", True, (64, 64, 64))
        y += 50
        screen.blit(word_surface, (x, y))


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)

db = Database()
db.add_player('qw', 1)
db.add_player('qwe', 2)
db.add_player('qwer', 3)
db.add_player('qwert', 4)
db.add_player('qwerty', 5)
db.add_player('qwertyr', 6)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Intro screen
player_stand = pygame.image.load('graphics/soldier_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center=(300, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(300, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(300, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Input text

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['rocket', 'mine', 'mine', 'mine'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(300, 330))
        screen.blit(game_name, game_name_rect)
        display_text(db.get_data())

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            # db.add_player(user_text, score)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
