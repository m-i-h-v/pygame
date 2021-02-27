import pygame
import random

pygame.init()
pygame.mouse.set_visible(False)

pygame.mixer.init()
explosion_sound = pygame.mixer.Sound('data/sounds/explosion.mp3')
shot_sound = pygame.mixer.Sound('data/sounds/shot.mp3')

COLORS = {'intro_part_1': pygame.Color((74, 212, 237)),
          'intro_part_2': pygame.Color((251, 232, 32)),
          'main_screen_button': pygame.Color((251, 232, 32)),
          'main_screen_button_back': pygame.Color((251, 232, 32, 50))}

game, score = False, 0
FPS = 60

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

CLOCK = pygame.time.Clock()

RIVAL_SPACESHIPS = pygame.sprite.Group()
CURSOR_SPRITE = pygame.sprite.Group()
PLAYER_SPACESHIP = pygame.sprite.Group()
PLAYER_BULLET = pygame.sprite.Group()
RIVAL_BULLETS = pygame.sprite.Group()
EXPLOSIONS = pygame.sprite.Group()
HEALTH_POINTS = pygame.sprite.Group()

devided_width = WIDTH / 1920
DEVIDED_WIDTH = WIDTH / 1920
DEVIDED_HEIGHT = HEIGHT / 1080
RESULUTION_FIT_NUMBERS = {'start_animation_font': int(70 * devided_width),
                          'start_animation_text': int(40 * devided_width),
                          'main_screen_x': int(150 * devided_width),
                          'main_screen_font': int(55 * devided_width),
                          'main_screen_button': int(250 * devided_width)}


class Cursor(pygame.sprite.Sprite):
    cursor = pygame.image.load('data/sprites/cursor.png')
    cursor = cursor.convert_alpha()
    cursor = pygame.transform.smoothscale(cursor, (int(50 * DEVIDED_WIDTH), int(50 * DEVIDED_WIDTH)))

    def __init__(self, group, current_pos):
        super().__init__(group)
        self.image = Cursor.cursor
        self.rect = self.image.get_rect()
        self.rect.x = current_pos[0] - int(25 * DEVIDED_WIDTH)
        self.rect.y = current_pos[1]

    def update(self, pos):
        self.rect.x = pos[0] - int(25 * DEVIDED_WIDTH)
        self.rect.y = pos[1]


class MainScreenButton:
    def __init__(self, text, font_name, size, x, y, color, pause=False, type=None):
        self.text, self.x, self.y, self.color = text, x, y, color
        self.pause, self.type = pause, type
        self.selected = False
        self.font = pygame.font.Font(font_name, size)

    def update(self, screen):
        button_surface = pygame.Surface((int(250 * DEVIDED_WIDTH), int(50 * DEVIDED_WIDTH)), pygame.SRCALPHA)
        if self.selected:
            color = COLORS[self.color + '_back']
            button_surface.fill(color)
            pygame.draw.rect(button_surface, COLORS[self.color],
                             (0, 0, int(250 * DEVIDED_WIDTH), int(50 * DEVIDED_WIDTH)), 1)
        string_rendered = self.font.render(self.text, True, COLORS[self.color])
        rectangle = string_rendered.get_rect(center=(int(125 * DEVIDED_WIDTH), int(25 * DEVIDED_WIDTH)))
        button_surface.blit(string_rendered, rectangle)

        if not self.pause:
            screen.blit(button_surface, (self.x, self.y))
        else:
            if self.type == 'exit':
                rect = button_surface.get_rect(center=(int(WIDTH * DEVIDED_WIDTH / 2),
                                                       int(HEIGHT * DEVIDED_HEIGHT / 2) + int(50 * DEVIDED_HEIGHT)))
            else:
                rect = button_surface.get_rect(center=(int(WIDTH * DEVIDED_WIDTH / 2),
                                                       int(HEIGHT * DEVIDED_HEIGHT / 2) - int(50 * DEVIDED_HEIGHT)))
            self.x, self.y = rect.x, rect.y
            screen.blit(button_surface, rect)

    def check_selected(self, x, y):
        self.selected = (x in range(self.x, self.x + int(250 * DEVIDED_WIDTH))
                         and y in range(self.y - int(35 * DEVIDED_WIDTH), self.y + int(50 * DEVIDED_WIDTH)))


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.smoothscale(pygame.image.load('data/sprites/bullet.png'),
                                        (int(6 * DEVIDED_WIDTH), int(20 * DEVIDED_WIDTH)))
    image.convert_alpha()

    def __init__(self, group, owner, x_pos, y_pos):
        super().__init__(group)
        if owner == 'rival_spaceship':
            self.direction = 12
            self.image = pygame.transform.flip(Bullet.image, False, True)
        else:
            self.direction = -12
            self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()
        else:
            self.rect.y += self.direction


class PlayerSpaceship(pygame.sprite.Sprite):
    image = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/player_spaceship.png'),
                                         (int(80 * DEVIDED_WIDTH), int(80 * DEVIDED_WIDTH)))
    image = image.convert_alpha()

    def __init__(self, group):
        super().__init__(group)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 300))

    def update(self, direction):
        if self.rect.x + direction in range(WIDTH - int(80 * DEVIDED_WIDTH)):
            self.rect.x += direction


class RivalSpaceship(pygame.sprite.Sprite):
    rival_spaceship_tier_1 = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/rival_spaceship_tier_1.png'),
                                                          (int(60 * DEVIDED_WIDTH), int(60 * DEVIDED_WIDTH)))
    rival_spaceship_tier_1 = pygame.transform.flip(rival_spaceship_tier_1, False, True)
    rival_spaceship_tier_1 = rival_spaceship_tier_1.convert_alpha()

    rival_spaceship_tier_2 = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/rival_spaceship_tier_2.png'),
                                                          (int(60 * DEVIDED_WIDTH), int(60 * DEVIDED_WIDTH)))
    rival_spaceship_tier_2 = pygame.transform.flip(rival_spaceship_tier_2, False, True)
    rival_spaceship_tier_2 = rival_spaceship_tier_2.convert_alpha()

    rival_spaceship_tier_3 = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/rival_spaceship_tier_3.png'),
                                                          (int(60 * DEVIDED_WIDTH), int(60 * DEVIDED_WIDTH)))
    rival_spaceship_tier_3 = pygame.transform.flip(rival_spaceship_tier_3, False, True)
    rival_spaceship_tier_3 = rival_spaceship_tier_3.convert_alpha()

    rival_spaceship_tier_4 = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/rival_spaceship_tier_4.png'),
                                                          (int(60 * DEVIDED_WIDTH), int(60 * DEVIDED_WIDTH)))
    rival_spaceship_tier_4 = pygame.transform.flip(rival_spaceship_tier_4, False, True)
    rival_spaceship_tier_4 = rival_spaceship_tier_4.convert_alpha()

    explosion = pygame.transform.smoothscale(pygame.image.load('data/sprites/explosion.png'),
                                             (int(480 * DEVIDED_WIDTH),
                                              int(360 * DEVIDED_HEIGHT)))
    explosion = explosion.convert_alpha()

    def __init__(self, group, tier, current_pos):
        super().__init__(group)
        self.tier, self.current_pos = tier, current_pos
        self.mode = 'just_moving'
        if tier == 1:
            self.image = RivalSpaceship.rival_spaceship_tier_1
        elif tier == 2:
            self.image = RivalSpaceship.rival_spaceship_tier_2
        elif tier == 3:
            self.image = RivalSpaceship.rival_spaceship_tier_3
        else:
            self.image = RivalSpaceship.rival_spaceship_tier_4
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = current_pos[0], current_pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, direction, player_spaceship):
        global score, health
        if self.mode == 'just_moving':
            self.rect.x += direction
        elif self.mode == 'getting_back':
            if self.rect.x != self.destination:
                if abs(self.rect.x - self.destination) < 3:
                    self.rect.x += 1 if self.destination - self.rect.x > 0 else -1
                else:
                    self.rect.x += 2 if self.destination - self.rect.x > 0 else -2
            if self.rect.y != self.take_off_position_y:
                self.rect.y += 2
            if self.rect.x == self.destination and self.rect.y == self.take_off_position_y:
                self.mode = 'just_moving'
        elif self.mode == 'attacking':
            if self.rect.y % 300 in range(3, 5):
                Bullet(RIVAL_BULLETS, 'rival_spaceship', self.rect.x + int(30 * DEVIDED_WIDTH), self.rect.y)
                shot_sound.play()
            if self.rect.y % HEIGHT != int(80 * DEVIDED_WIDTH):
                self.rect.y = (self.rect.y + 2) % HEIGHT
                if self.rect.x > self.points[self.num]:
                    if self.rect.x - self.points[self.num] < 10:
                        self.rect.x -= 1
                    else:
                        self.rect.x -= 2
                elif self.rect.x == self.points[self.num]:
                    self.num = (self.num + 1) % 2
                else:
                    if self.points[self.num] - self.rect.x < 10:
                        self.rect.x += 1
                    else:
                        self.rect.x += 2
            else:
                self.mode = 'getting_back'

        if len(PLAYER_BULLET):
            if pygame.sprite.collide_mask(self, PLAYER_BULLET.sprites()[0]):
                score += self.tier * 25
                self.mode = 'dead'
                explosion_sound.play()
                AnimatedSprite(RivalSpaceship.explosion, 8, 6, self.rect.x, self.rect.y)
                PLAYER_BULLET.empty()
                self.kill()
        if len(PLAYER_SPACESHIP):
            if pygame.sprite.collide_mask(self, player_spaceship):
                AnimatedSprite(RivalSpaceship.explosion, 8, 6, self.rect.x, self.rect.y)
                self.mode = 'dead'
                explosion_sound.play()
                self.kill()
                health -= 1


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(EXPLOSIONS)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.cur_frame == 47:
            self.kill()


def start_animation():
    intro_part_1, intro_part_2 = True, False
    first_intro, text_top_coord = pygame.USEREVENT + 1, 0
    pygame.time.set_timer(first_intro, 4000)
    brightness = pygame.USEREVENT + 2
    pygame.time.set_timer(brightness, 10)

    SCREEN.fill((0, 0, 0))
    font = pygame.font.Font('data/intro_font.ttf', int(70 * DEVIDED_WIDTH))
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
        intro_rect = string_rendered.get_rect(center=(WIDTH / 2,
                                                      HEIGHT / 2 - int(40 * DEVIDED_WIDTH)))
        SCREEN.blit(string_rendered, intro_rect)

        string_rendered = font.render('far away...', True, color)
        intro_rect = string_rendered.get_rect(center=(WIDTH / 2,
                                                      HEIGHT / 2 + int(40 * DEVIDED_WIDTH)))
        SCREEN.blit(string_rendered, intro_rect)

        pygame.display.flip()

    pygame.time.set_timer(first_intro, 0)
    main_screen()


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


def load_level(level):
    with open('data/levels/level_map_{}.txt'.format(str(level)), mode='r', encoding='utf-8') as map_file:
        ships = [line.strip() for line in map_file]
        for ship_row in range(len(ships)):
            for ship in range(len(ships[ship_row])):
                if ships[ship_row][ship] == '#':
                    continue
                else:
                    RivalSpaceship(RIVAL_SPACESHIPS, int(ships[ship_row][ship]),
                                   (int((ship * 90 + 530) * DEVIDED_WIDTH), int((ship_row * 90 + 150) * DEVIDED_WIDTH)))


def pause(background, scoreboard, attack, death_cooldown):
    global game
    start_time = pygame.time.get_ticks()
    attack_timer = death_cooldown_timer = False
    pause_menu = pygame.Surface((int(600 * DEVIDED_WIDTH), int(400 * DEVIDED_HEIGHT)))
    menu_rect = pause_menu.get_rect(center=(int(WIDTH * DEVIDED_WIDTH / 2), int(HEIGHT * DEVIDED_HEIGHT / 2)))
    pause_menu.fill((32, 32, 32))
    resume_button = MainScreenButton('Продолжить', None, int(55 * DEVIDED_WIDTH),
                                     None, None, 'main_screen_button', True, 'resume')
    exit_button = MainScreenButton('Выйти', None, int(55 * DEVIDED_WIDTH),
                                   None, None, 'main_screen_button', True, 'exit')
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
            if event.type == attack:
                attack_timer = True
                attack_timer_time = pygame.time.get_ticks() - start_time
            if event.type == death_cooldown:
                death_cooldown_timer = True
                death_cooldown_timer_time = pygame.time.get_ticks() - start_time

        SCREEN.blit(background, (0, 0))
        PLAYER_BULLET.draw(SCREEN)
        RIVAL_BULLETS.draw(SCREEN)
        RIVAL_SPACESHIPS.draw(SCREEN)
        PLAYER_SPACESHIP.draw(SCREEN)
        EXPLOSIONS.draw(SCREEN)

        SCREEN.blit(pause_menu, menu_rect)
        resume_button.update(SCREEN)
        exit_button.update(SCREEN)
        HEALTH_POINTS.draw(SCREEN)


        SCREEN.blit(scoreboard, (int(1500 * DEVIDED_WIDTH), int(50 * DEVIDED_HEIGHT)))
        CURSOR_SPRITE.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)

    if attack_timer:
        pygame.time.set_timer(attack, attack_timer_time, 1)
    if death_cooldown_timer:
        pygame.time.set_timer(death_cooldown, death_cooldown_timer_time, 1)


def new_game():
    global game, score, health
    health_icon = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/player_spaceship.png'),
                                               (int(35 * DEVIDED_WIDTH), int(30 * DEVIDED_WIDTH)))
    health_icon.convert_alpha()
    explosion = pygame.transform.smoothscale(pygame.image.load('data/sprites/explosion.png'),
                                             (int(480 * DEVIDED_WIDTH),
                                              int(360 * DEVIDED_HEIGHT)))
    explosion = explosion.convert_alpha()

    health = 3
    for i in range(health):
        sprite = pygame.sprite.Sprite()
        sprite.image = health_icon
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = int(1200 * DEVIDED_WIDTH + 55 * DEVIDED_WIDTH * i)
        sprite.rect.y = int(50 * DEVIDED_WIDTH)
        HEALTH_POINTS.add(sprite)

    death_cooldown = pygame.USEREVENT + 3
    attack = pygame.USEREVENT + 4
    someone_is_attacking = someone_is_getting_back = False
    pygame.time.set_timer(attack, random.randrange(8000, 12000), 1)
    mod_nums = [i % int(90 * DEVIDED_WIDTH) for i in range(int(530 * DEVIDED_WIDTH) % int(90 * DEVIDED_WIDTH),
                                                           int(530 * DEVIDED_WIDTH) % int(90 * DEVIDED_WIDTH) +
                                                           int(60 * DEVIDED_WIDTH))]
    game, moved, direction, level, score = True, 0, random.choice((1, -1)), 1, 0
    able_to_shoot, bullet_flies, evasion = True, False, False
    scoreboard = pygame.surface.Surface((int(200 * DEVIDED_WIDTH), int(50 * DEVIDED_WIDTH)), pygame.SRCALPHA)
    font = pygame.font.Font(None, int(50 * DEVIDED_WIDTH))
    word_score = font.render('Счёт:', True, pygame.Color((255, 255, 255)))
    background = pygame.transform.smoothscale(pygame.image.load('data/backgrounds/background_start_game.png'), (WIDTH, HEIGHT))
    load_level(level)
    player_spaceship = PlayerSpaceship(PLAYER_SPACESHIP)

    while game:
        current_score = font.render(str(score), True, (255, 255, 255))
        scoreboard.fill(pygame.SRCALPHA)
        scoreboard.blit(word_score, (0, 0))
        scoreboard.blit(current_score, (int(100 * DEVIDED_WIDTH), 0))
        if len(RIVAL_SPACESHIPS) == 0:
            if level < 4:
                level += 1
                load_level(level)
                moved, direction, bullet_flies, able_to_shoot = 0, random.choice((1, -1)), False, True
                PLAYER_BULLET.empty()
                RIVAL_BULLETS.empty()
                new_level_animation()
            else:
                PLAYER_BULLET.empty()
                RIVAL_BULLETS.empty()
                victory_animation()
                break
        spaceships = sorted(RIVAL_SPACESHIPS, key=lambda x: x.rect.x)
        left, right = spaceships[0].rect.x, spaceships[-1].rect.x
        left_border, right_border = left - moved, int(1920 * DEVIDED_WIDTH) - (right + int(60 * DEVIDED_WIDTH) - moved)
        moved += direction
        if moved == -left_border or moved == right_border:
            direction *= -1
            moved += 2 * direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(background, scoreboard, attack, death_cooldown)
            if event.type == death_cooldown:
                player_spaceship = PlayerSpaceship(PLAYER_SPACESHIP)
            if event.type == attack:
                attacking_candidates = list(filter(lambda x: abs(x.rect.x - player_spaceship.rect.x) < 70,
                                                   RIVAL_SPACESHIPS))
                if len(attacking_candidates):
                    main_attacking_spaceship = sorted(attacking_candidates, key=lambda x: x.rect.y)[0]
                    other_candidates = list(filter(lambda x: abs(x.rect.x -
                                                                 main_attacking_spaceship.rect.x) == int(90 *
                                                                                                         DEVIDED_WIDTH),
                                                   RIVAL_SPACESHIPS))
                    if len(other_candidates) == 1 and main_attacking_spaceship.tier > 2:
                        other_attacking_spaceships = [other_candidates[0]]
                    elif len(other_candidates) > 1 and main_attacking_spaceship.tier > 2:
                        other_candidates = sorted(other_candidates, key=lambda x: x.rect.y)
                        other_attacking_spaceships = [other_candidates[0], other_candidates[1]]
                    else:
                        other_attacking_spaceships = []
                    main_attacking_spaceship.mode = 'attacking'
                    main_attacking_spaceship.points = [main_attacking_spaceship.rect.x - 200,
                                                       main_attacking_spaceship.rect.x + 200]
                    main_attacking_spaceship.moved = moved
                    main_attacking_spaceship.take_off_position_y = main_attacking_spaceship.rect.y
                    main_attacking_spaceship.num = 0
                    main_attacking_spaceship.take_off_position_x = main_attacking_spaceship.rect.x + direction
                    for spaceship in other_attacking_spaceships:
                        spaceship.mode = 'attacking'
                        spaceship.num = 0
                        spaceship.take_off_position_y = spaceship.rect.y
                        spaceship.points = [spaceship.rect.x - 200, spaceship.rect.x + 200]
                        spaceship.moved = moved
                        spaceship.take_off_position_x = spaceship.rect.x + direction
                    someone_is_attacking = True
                else:
                    pygame.time.set_timer(attack, (random.randrange(10000, 14000, 1)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_spaceship is not None:
            PLAYER_SPACESHIP.update(-3)
        if keys[pygame.K_RIGHT] and player_spaceship is not None:
            PLAYER_SPACESHIP.update(3)
        if keys[pygame.K_UP] and player_spaceship is not None:
            if able_to_shoot:
                bullet = Bullet(PLAYER_BULLET, 'player_spaceship',
                       player_spaceship.rect.x + int(40 * DEVIDED_WIDTH), player_spaceship.rect.y)
                shot_sound.play()
                bullet_flies, able_to_shoot = True, False
                evasion = True if random.randrange(100) < 40 else False

        if someone_is_attacking:
            someone_is_getting_back_local = False
            all_dead = True
            if main_attacking_spaceship.mode == 'getting_back':
                all_dead = False
                someone_is_getting_back_local = True
            if main_attacking_spaceship.mode != 'dead':
                all_dead = False
            for ship in other_attacking_spaceships:
                if ship.mode == 'getting_back':
                    someone_is_getting_back_local = True
                if ship.mode != 'dead':
                    all_dead = False
            if someone_is_getting_back_local:

                someone_is_attacking = False
                someone_is_getting_back = True
                main_attacking_spaceship.destination = main_attacking_spaceship.take_off_position_x + \
                                                       moved - main_attacking_spaceship.moved - direction
                for ship in other_attacking_spaceships:
                    ship.destination = ship.take_off_position_x + moved - ship.moved - direction
            elif all_dead:
                someone_is_attacking = False
                pygame.time.set_timer(attack, random.randrange(8000, 12000), 1)

        if someone_is_getting_back:
            all_dead = True
            someone_is_getting_back_local = False
            if main_attacking_spaceship.mode == 'getting_back':
                all_dead = False
                someone_is_getting_back_local = True
            for ship in other_attacking_spaceships:
                if ship.mode == 'getting_back':
                    all_dead = False
                    someone_is_getting_back_local = True
            if not someone_is_getting_back_local or all_dead:
                someone_is_getting_back = False
                pygame.time.set_timer(attack, random.randrange(8000, 12000), 1)

        spacehips_before_update = len(RIVAL_SPACESHIPS)
        health_before_update = health
        if ((bullet_flies and bullet.rect.x in range(left + moved, right + int(60 * DEVIDED_WIDTH) + moved)) and
                (bullet.rect.x - moved + direction) % int(90 * DEVIDED_WIDTH) not in mod_nums and \
                (bullet.rect.x - moved + direction + int(6 * DEVIDED_WIDTH)) % int(90 * DEVIDED_WIDTH) not in mod_nums \
                and evasion) or someone_is_getting_back:
            moved -= direction
            RIVAL_SPACESHIPS.update(0, player_spaceship)
        else:
            RIVAL_SPACESHIPS.update(direction, player_spaceship)

        for bullet_ in RIVAL_BULLETS.sprites():
            if player_spaceship is not None:
                if pygame.sprite.collide_mask(player_spaceship, bullet_):
                    health -= 1
                    bullet_.kill()
                    break

        if health_before_update != health:
            if health == 0:
                defeat_animation()
                break
            else:
                HEALTH_POINTS.remove(HEALTH_POINTS.sprites()[-1])
                AnimatedSprite(explosion, 8, 6, player_spaceship.rect.x, player_spaceship.rect.y)
                player_spaceship = None
                explosion_sound.play()
                PLAYER_SPACESHIP.empty()
                pygame.time.set_timer(death_cooldown, 4500, 1)

        if len(PLAYER_BULLET) == 0 and bullet_flies:
            bullet_flies, able_to_shoot = False, True
        RIVAL_BULLETS.update()
        PLAYER_BULLET.update()
        EXPLOSIONS.update()

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(scoreboard, (int(1500 * DEVIDED_WIDTH), int(50 * DEVIDED_WIDTH)))
        PLAYER_SPACESHIP.draw(SCREEN)
        RIVAL_SPACESHIPS.draw(SCREEN)
        RIVAL_BULLETS.draw(SCREEN)
        PLAYER_BULLET.draw(SCREEN)
        HEALTH_POINTS.draw(SCREEN)
        EXPLOSIONS.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)

    PLAYER_BULLET.empty()
    RIVAL_BULLETS.empty()
    RIVAL_SPACESHIPS.empty()
    PLAYER_SPACESHIP.empty()
    EXPLOSIONS.empty()
    HEALTH_POINTS.empty()


def new_level_animation():
    pass


def victory_animation():
    pass


def defeat_animation():
    pass


EXIT_BUTTON = MainScreenButton('Выход', None,
                               int(55 * DEVIDED_WIDTH),
                               int(150 * DEVIDED_WIDTH),
                               int(800 * DEVIDED_WIDTH), 'main_screen_button')

START_GAME_BUTTON = MainScreenButton('Играть', None, int(55 * DEVIDED_WIDTH),
                                     int(150 * DEVIDED_WIDTH),
                                     int(500 * DEVIDED_WIDTH), 'main_screen_button')

CURSOR = Cursor(CURSOR_SPRITE, pygame.mouse.get_pos())

if __name__ == '__main__':
    start_animation()