import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, owner, x_pos, y_pos, d_w, d_h, h):
        super().__init__(group)
        self.DEVIDED_WIDTH, self.DEVIDED_HEIGHT, self.HEIGHT = d_w, d_h, h
        self.image = pygame.transform.smoothscale(pygame.image.load('data/sprites/bullet.png'),
                                             (int(6 * self.DEVIDED_WIDTH), int(20 * self.DEVIDED_WIDTH)))
        self.image.convert_alpha()
        if owner == 'rival_spaceship':
            self.direction = 12
            self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.direction = -12
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.y < 0 or self.rect.y > self.HEIGHT:
            self.kill()
        else:
            self.rect.y += self.direction