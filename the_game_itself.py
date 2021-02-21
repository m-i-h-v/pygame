import pygame
import random

pygame.init()
pygame.mouse.set_visible(False)

COLORS = {'intro_part_1': pygame.Color((74, 212, 237)),
          'intro_part_2': pygame.Color((251, 232, 32)),
          'main_screen_button': pygame.Color((251, 232, 32)),
          'main_screen_button_back': pygame.Color((251, 232, 32, 50))
          }

game, score = False, 0
FPS = 60
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
CLOCK = pygame.time.Clock()
RIVAL_SPACESHIPS = pygame.sprite.Group()
CURSOR_SPRITE = pygame.sprite.Group()
PLAYER_SPACESHIP = pygame.sprite.Group()

resolution_fit_numbers = {'start_animation_font': int(70 * WIDTH / 1920)}

def load_level(level):
    with open('data/levels/level_map_{}.txt'.format(str(level)), mode='r', encoding='utf-8') as map_file:
        ships = [line.strip() for line in map_file]
        for ship_row in range(len(ships)):
            for ship in range(len(ships[ship_row])):
                if ships[ship_row][ship] == '#':
                    continue
                else:
                    RivalSpaceship(RIVAL_SPACESHIPS, int(ships[ship_row][ship]), (ship * 80 + 530, ship_row * 80 + 150))


def pause(background, scoreboard):
    global game
    pause_menu = pygame.Surface((600, 400))
    pause_menu.fill((32, 32, 32))
    resume_button = MainScreenButton('Продолжить', None, 55, 860, 390, 'main_screen_button')
    exit_button = MainScreenButton('Выйти', None, 55, 860, 590, 'main_screen_button')
    pause_on = True

    while pause_on:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                CURSOR_SPRITE.update(event.pos)
                resume_button.check_selected(event.pos[0], event.pos[1])
                exit_button.check_selected(event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.selected:
                    game = False
                    pause_on = False
                if resume_button.selected:
                    pause_on = False

        SCREEN.blit(background, (0, 0))
        RIVAL_SPACESHIPS.draw(SCREEN)
        PLAYER_SPACESHIP.draw(SCREEN)
        GAME_SPRITES.draw(SCREEN)
        SCREEN.blit(pause_menu, (WIDTH / 2 - 300, HEIGHT / 2 - 200))
        resume_button.update(SCREEN)
        exit_button.update(SCREEN)
        SCREEN.blit(scoreboard, (1500, 50))
        CURSOR_SPRITE.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)


def new_game():
    global game, score
    mod_80_nums = [i % 80 for i in range(50, 110)]
    game, moved, direction, level, score = True, 0, random.choice((1, -1)), 1, 0
    BULLET.rect.y = 2000
    able_to_shoot, bullet_flies, evasion = True, False, False
    player_movement = 0
    scoreboard = pygame.surface.Surface((200, 50), pygame.SRCALPHA)
    font = pygame.font.Font(None, 50)
    word_score = font.render('Счёт:', True, pygame.Color((255, 255, 255)))
    background = pygame.transform.smoothscale(pygame.image.load('data/backgrounds/background_start_game.png'), (WIDTH, HEIGHT))
    load_level(level)
    player_spaceship = PlayerSpaceship(PLAYER_SPACESHIP)

    while game:
        current_score = font.render(str(score), True, (255, 255, 255))
        scoreboard.fill(pygame.SRCALPHA)
        scoreboard.blit(word_score, (0, 0))
        scoreboard.blit(current_score, (100, 0))
        if len(RIVAL_SPACESHIPS) == 0:
            if level < 4:
                level += 1
                load_level(level)
                moved, direction, bullet_flies, able_to_shoot = 0, random.choice((1, -1)), False, True
                BULLET.rect.y = 2000
                new_level_animation()
            else:
                print('Victory')
                win_animation()
                break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(background, scoreboard)
        moved += direction
        if moved == -450 or moved == 450:
            direction *= -1
            moved += 2 * direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_movement > -900:
            player_movement -= 3
            PLAYER_SPACESHIP.update(-3)
        if keys[pygame.K_RIGHT] and player_movement < 940:
            player_movement += 3
            PLAYER_SPACESHIP.update(3)
        if keys[pygame.K_UP]:
            if able_to_shoot:
                bullet_flies = True
                able_to_shoot = False
                evasion = True if random.randrange(100) < 25 else False

        spacehips_before_update = len(RIVAL_SPACESHIPS)
        if bullet_flies and BULLET.rect.x in range(520 + moved, 1340 + moved) and evasion:
            mod_80_num = moved - direction
            if (BULLET.rect.x - mod_80_num) % 80 not in mod_80_nums and \
                    (BULLET.rect.x - mod_80_num + 6) % 80 not in mod_80_nums:
                moved -= direction
                RIVAL_SPACESHIPS.update(0, True)
            else:
                RIVAL_SPACESHIPS.update(direction, True)
        else:
            RIVAL_SPACESHIPS.update(direction, True)
        if spacehips_before_update != len(RIVAL_SPACESHIPS) or BULLET.rect.y < 0:
            bullet_flies, able_to_shoot = False, True
            BULLET.rect.y = 2000
        elif bullet_flies:
            if BULLET.rect.y == 2000:
                BULLET.rect.x = player_spaceship.rect.x + 36
                BULLET.rect.y = 920
            else:
                BULLET.rect.y -= 12

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(scoreboard, (1500, 50))
        GAME_SPRITES.draw(SCREEN)
        PLAYER_SPACESHIP.draw(SCREEN)
        RIVAL_SPACESHIPS.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)

    RIVAL_SPACESHIPS.empty()
    PLAYER_SPACESHIP.empty()


class RivalSpaceship(pygame.sprite.Sprite):
    rival_spaceship_tier_1 = pygame.transform.smoothscale(pygame.image.load('data/sprites/rival_spaceship_tier_1.png'), (60, 60))
    rival_spaceship_tier_1 = pygame.transform.flip(rival_spaceship_tier_1, False, True)
    rival_spaceship_tier_1 = rival_spaceship_tier_1.convert_alpha()

    rival_spaceship_tier_2 = pygame.transform.smoothscale(pygame.image.load('data/sprites/rival_spaceship_tier_2.png'), (60, 60))
    rival_spaceship_tier_2 = pygame.transform.flip(rival_spaceship_tier_2, False, True)
    rival_spaceship_tier_2 = rival_spaceship_tier_2.convert_alpha()

    rival_spaceship_tier_3 = pygame.transform.smoothscale(pygame.image.load('data/sprites/rival_spaceship_tier_3.png'), (60, 60))
    rival_spaceship_tier_3 = pygame.transform.flip(rival_spaceship_tier_3, False, True)
    rival_spaceship_tier_3 = rival_spaceship_tier_3.convert_alpha()

    rival_spaceship_tier_4 = pygame.transform.smoothscale(pygame.image.load('data/sprites/rival_spaceship_tier_4.png'), (60, 60))
    rival_spaceship_tier_4 = pygame.transform.flip(rival_spaceship_tier_4, False, True)
    rival_spaceship_tier_4 = rival_spaceship_tier_4.convert_alpha()

    def __init__(self, group, tier, current_pos):
        super().__init__(group)
        self.tier, self.current_pos = tier, current_pos
        if tier == 1:
            self.image = RivalSpaceship.rival_spaceship_tier_1
        elif tier == 2:
            self.image = RivalSpaceship.rival_spaceship_tier_2
        elif tier == 3:
            self.image = RivalSpaceship.rival_spaceship_tier_3
        else:
            self.image = RivalSpaceship.rival_spaceship_tier_4
        self.rect = self.image.get_rect()
        self.rect.x = current_pos[0]
        self.rect.y = current_pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dir, check_death=None):
        global score
        self.rect.x += dir
        if check_death is not None:
            if pygame.sprite.collide_mask(self, BULLET):
                self.kill()
                score += self.tier * 25


class PlayerSpaceship(pygame.sprite.Sprite):
    player_spaceship_tier_1 = pygame.transform.smoothscale(pygame.image.load('data/sprites/player_spaceship_tier_1.png'), (80, 80))
    player_spaceship_tier_1 = player_spaceship_tier_1.convert_alpha()

    def __init__(self, group):
        super().__init__(group)
        self.tier, self.current_pos = 1, (900, 900)
        self.image = self.player_spaceship_tier_1
        self.rect = self.image.get_rect()
        self.rect.x = self.current_pos[0]
        self.rect.y = self.current_pos[1]

    def update(self, dir):
        self.rect.x += dir


class Cursor(pygame.sprite.Sprite):
    cursor = pygame.image.load('data/cursor4.png')
    cursor = cursor.convert_alpha()
    cursor = pygame.transform.smoothscale(cursor, (50, 50))

    def __init__(self, group, current_pos):
        super().__init__(group)
        self.image = Cursor.cursor
        self.rect = self.image.get_rect()
        self.rect.x = current_pos[0] - 25
        self.rect.y = current_pos[1] - 3


    def update(self, pos):
        self.rect.x = pos[0] - 25
        self.rect.y = pos[1]


class MainScreenButton:
    def __init__(self, text, font_name, size, x, y, color):
        self.text, self.x, self.y, self.color = text, x, y, color
        self.selected = False
        self.font = pygame.font.Font(font_name, size)

    def update(self, screen):
        button_surface = pygame.Surface((250, 50), pygame.SRCALPHA)
        if self.selected:
            color = COLORS[self.color + '_back']
            button_surface.fill(color)
            pygame.draw.rect(button_surface, COLORS[self.color], (0, 0, 250, 50), 1)
        string_rendered = self.font.render(self.text, True, COLORS[self.color])
        rectangle = string_rendered.get_rect(center=(125, 25))
        button_surface.blit(string_rendered, rectangle)

        screen.blit(button_surface, (self.x, self.y))

    def check_selected(self, x, y):
        self.selected = (x in range(self.x, self.x + 250) and y in range(self.y - 35, self.y + 50))


def main_screen():
    background = pygame.transform.smoothscale(pygame.image.load('data/backgrounds/main_menu.png'), (WIDTH, HEIGHT))

    while True:
        SCREEN.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if EXIT_BUTTON.selected:
                    quit()
                elif START_GAME_BUTTON.selected:
                    new_game()
            if event.type == pygame.MOUSEMOTION:
                CURSOR.update(pygame.mouse.get_pos())
                EXIT_BUTTON.check_selected(event.pos[0], event.pos[1])
                START_GAME_BUTTON.check_selected(event.pos[0], event.pos[1])

        EXIT_BUTTON.update(SCREEN)
        START_GAME_BUTTON.update(SCREEN)
        CURSOR_SPRITE.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)


def start_animation():
    intro_part_1, intro_part_2 = True, False
    first_intro, text_top_coord = pygame.USEREVENT + 1, 0
    pygame.time.set_timer(first_intro, 4000)
    brightness = pygame.USEREVENT + 2
    pygame.time.set_timer(brightness, 10)

    SCREEN.fill((0, 0, 0))
    font = pygame.font.Font('data/intro_font.ttf', 70)
    color = COLORS['intro_part_1']
    hsv = color.hsva
    color.hsva = (hsv[0], hsv[1], 4, hsv[3])

    pygame.display.flip()

    while intro_part_1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                intro_part_1 = event.key != pygame.K_ESCAPE and event.key != pygame.K_SPACE
            if event.type == first_intro:
                intro_part_1 = False
            if event.type == brightness:
                hsv = color.hsva
                if hsv[2] > 99:
                    pygame.time.set_timer(brightness, 0)
                else:
                    color.hsva = (hsv[0], hsv[1], hsv[2] + 1, hsv[3])

        string_rendered = font.render('A long time ago in a galaxy far,', True, color)
        intro_rect = string_rendered.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 40))
        SCREEN.blit(string_rendered, intro_rect)

        string_rendered = font.render('far away...', True, color)
        intro_rect = string_rendered.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 40))
        SCREEN.blit(string_rendered, intro_rect)

        pygame.display.flip()

    pygame.time.set_timer(first_intro, 0)
    main_screen()


def win_animation():
    pass


def new_level_animation():
    pass


EXIT_BUTTON = MainScreenButton('Выход', None, 55, 150, 800, 'main_screen_button')
START_GAME_BUTTON = MainScreenButton('Играть', None, 55, 150, 500, 'main_screen_button')
CURSOR = Cursor(CURSOR_SPRITE, pygame.mouse.get_pos())
BULLET = pygame.sprite.Sprite()
bullet_image = pygame.transform.smoothscale(pygame.image.load('data/new_bullet.png'), (6, 20))
bullet_image = bullet_image.convert_alpha()
BULLET.image = bullet_image
BULLET.rect = BULLET.image.get_rect()
BULLET.rect.x = 930
BULLET.rect.y = -20
BULLET.mask = pygame.mask.from_surface(BULLET.image)
GAME_SPRITES = pygame.sprite.Group()
GAME_SPRITES.add(BULLET)

start_animation()