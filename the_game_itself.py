import pygame

pygame.init()
pygame.mouse.set_visible(False)

COLORS = {'intro_part_1': pygame.Color((74, 212, 237)),
          'intro_part_2': pygame.Color((251, 232, 32)),
          'main_screen_button': pygame.Color((251, 232, 32)),
          'main_screen_button_back': pygame.Color((251, 232, 32, 50))
          }


TEXT = ['galaxian', 'тут текст', 'тут тоже', 'и здесь', 'а здесь могла бьiть ваша реклама', '89220368225',
        'Михаил', '50 руб/сутки']
FPS = 60
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
CLOCK = pygame.time.Clock()
CURSOR = pygame.image.load('data/cursor3.png')
CURSOR = CURSOR.convert_alpha()
CURSOR = pygame.transform.smoothscale(CURSOR, (50, 50))


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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if event.pos[0] in range(150, 400) and event.pos[1] in range(765, 850):
                    quit()
            if event.type == pygame.MOUSEMOTION:
                EXIT_BUTTON.check_selected(event.pos[0], event.pos[1])
                START_GAME_BUTTON.check_selected(event.pos[0], event.pos[1])

        EXIT_BUTTON.update(SCREEN)
        START_GAME_BUTTON.update(SCREEN)
        SCREEN.blit(CURSOR, (pygame.mouse.get_pos()[0] - 25, pygame.mouse.get_pos()[1] - 3))
        pygame.display.flip()


def start_animation():
    intro_part_1, intro_part_2 = True, False
    first_intro, text_top_coord = pygame.USEREVENT + 1, 0
    pygame.time.set_timer(first_intro, 4000)

    SCREEN.fill((0, 0, 0))
    font = pygame.font.Font('data/intro_font.ttf', 70)

    string_rendered = font.render('A long time ago in a galaxy far,', True, COLORS['intro_part_1'])
    intro_rect = string_rendered.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 40))
    SCREEN.blit(string_rendered, intro_rect)

    string_rendered = font.render('far away...', True, COLORS['intro_part_1'])
    intro_rect = string_rendered.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 40))
    SCREEN.blit(string_rendered, intro_rect)

    pygame.display.flip()

    while intro_part_1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                intro_part_1 = event.key != pygame.K_ESCAPE and event.key != pygame.K_SPACE
            if event.type == first_intro:
                intro_part_1 = False
                intro_part_2 = True

    pygame.time.set_timer(first_intro, 0)

    background = pygame.transform.scale(pygame.image.load('data/backgrounds/background_start_game.png'), (WIDTH, HEIGHT))

    while intro_part_2:
        text_top_coord += 1
        SCREEN.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                intro_part_2 = event.key != pygame.K_ESCAPE and event.key != pygame.K_SPACE
        for num, text in enumerate(TEXT):
            string_rendered = font.render(text, True, COLORS['intro_part_2'])
            intro_rect = string_rendered.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 490 + num * 70 - text_top_coord))
            SCREEN.blit(string_rendered, intro_rect)
        pygame.display.flip()
        CLOCK.tick(FPS)
    main_screen()


EXIT_BUTTON = MainScreenButton('Выход', None, 55, 150, 800, 'main_screen_button')
START_GAME_BUTTON = MainScreenButton('Играть', None, 55, 150, 500, 'main_screen_button')

start_animation()