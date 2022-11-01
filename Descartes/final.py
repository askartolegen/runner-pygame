import pygame
from random import choice
import re
from objects import Player, Database, Obstacle


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = test_font.render(text, True, self.color)
        self.active = False
        self.res = ""

    def handle_event(self, event_):
        if event_.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event_.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_SPACE:
                    self.res = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = test_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen_):
        # Blit the text.
        screen_.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen_, self.color, self.rect, 2)

    def get_text(self):
        return self.res


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        db.add_player(name, score)
        return False
    else:
        return True


def display_text(data):
    tb = data[:]
    x, y = 580, 30
    word_surface = test_font.render('Top 5 players:', True, (64, 64, 64))
    screen.blit(word_surface, (x, y))

    if len(tb) < 5:
        tb = tb + [('None', 0)] * (5 - len(tb))

    for lines in tb:
        word_surface = test_font.render(f"{lines[0]}: {lines[1]}", True, (64, 64, 64))
        y += 50
        screen.blit(word_surface, (x, y))


def is_valid(name_):
    pattern = re.compile(r'^[A-Za-z0-9]*$')
    return bool(re.match(pattern, name_))


def static_elements():
    global valid
    valid = True
    error_message = test_font.render('Satisfied', False, (64, 64, 64))
    screen.blit(player_stand, player_stand_rect)
    display_text(db.get_data())
    input_box.draw(screen)
    screen.blit(input_message, input_message_rect)
    name_ = input_box.text
    if name_:
        if not is_valid(name_):
            error_message = test_font.render('Invalid Name', False, (64, 64, 64))
            valid = False
        if name_ in exist_players:
            error_message = test_font.render('This name already exist', False, (64, 64, 64))
            valid = False
        if len(name_) > 15:
            error_message = test_font.render('Too long', False, (64, 64, 64))
            valid = False
    else:
        error_message = test_font.render('Empty value', False, (64, 64, 64))
        valid = False
    error_message_rect = error_message.get_rect(center=(630, 370))
    screen.blit(error_message, error_message_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
player_alive = False
start_page = True
valid = True
mouse_pos = (-1, -1)
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)

db = Database()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Texts
player_stand = pygame.image.load('graphics/Player/soldier_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 0.55)
player_stand_rect = player_stand.get_rect(midbottom=(100, 300))

game_name = test_font.render('Pixel Runner', False, (64, 64, 64))
game_name_rect = game_name.get_rect(center=(350, 50))

game_over_img = pygame.image.load('graphics/game_over.png')
game_over_img = pygame.transform.rotozoom(game_over_img, 0, 1)
game_over_img_rect = game_over_img.get_rect(center=(350, 200))

replay_img = pygame.image.load('graphics/replay.png')
replay_img = pygame.transform.rotozoom(replay_img, 0, 1)
replay_img_rect = replay_img.get_rect(center=(350, 250))

game_message1 = test_font.render('Enter name', False, (64, 64, 64))
game_message1_rect = game_message1.get_rect(center=(350, 150))
game_message2 = test_font.render('and press space to run', False, (64, 64, 64))
game_message2_rect = game_message2.get_rect(center=(350, 200))

win_message = test_font.render("You WIN", False, 'Gold')
win_message_rect = win_message.get_rect(center=(400, 200))

input_message = test_font.render("Enter a name:", False, (64, 64, 64))
input_message_rect = input_message.get_rect(center=(200, 370))

exist_players = [x[0] for x in db.get_exist_name()]

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Input text
COLOR_INACTIVE = pygame.Color('Grey')
COLOR_ACTIVE = pygame.Color('White')
input_box = InputBox(310, 350, 100, 32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            db.commit()
            running = False

        if player_alive:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['rocket', 'mine', 'mine', 'mine'])))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE and valid:
                    if start_page:
                        start_page = False
                        player_alive = True
                        start_time = int(pygame.time.get_ticks() / 1000)
            input_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (-1, -1)

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    if start_page:
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message1, game_message1_rect)
        screen.blit(game_message2, game_message2_rect)
        input_box.update()
        static_elements()

    else:
        if player_alive:
            score = display_score()
            player.draw(screen)
            player.draw(screen)
            player.update()
            obstacle_group.draw(screen)
            obstacle_group.update()
            name = input_box.get_text()
            player_alive = collision_sprite()

            if score >= 100:
                screen.blit(win_message, win_message_rect)

        else:
            screen.blit(game_over_img, game_over_img_rect)
            screen.blit(replay_img, replay_img_rect)
            score_message = test_font.render(f'Your score: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(350, 50))
            screen.blit(score_message, score_message_rect)
            input_box.update()
            if replay_img_rect.collidepoint(mouse_pos) and valid:
                start_time = int(pygame.time.get_ticks() / 1000)
                player_alive = True
            static_elements()
    exist_players = [x[0] for x in db.get_exist_name()]
    pygame.display.update()
    clock.tick(60)

pygame.quit()
