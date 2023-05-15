import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group, current_pos, width, height):
        super().__init__(group)
        self.DEVIDED_WIDTH, self.DEVIDED_HEIGHT = width, height
        self.cursor = pygame.image.load('data/sprites/cursor.png')
        self.cursor = self.cursor.convert_alpha()
        self.cursor = pygame.transform.smoothscale(self.cursor, (int(50 * self.DEVIDED_WIDTH), int(50 * self.DEVIDED_WIDTH)))
        self.image = self.cursor
        self.rect = self.image.get_rect()
        self.rect.x = current_pos[0] - int(25 * self.DEVIDED_WIDTH)
        self.rect.y = current_pos[1]

    def update(self, pos):
        self.rect.x = pos[0] - int(25 * self.DEVIDED_WIDTH)
        self.rect.y = pos[1]