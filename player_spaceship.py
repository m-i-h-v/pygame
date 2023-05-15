import pygame


class PlayerSpaceship(pygame.sprite.Sprite):
    def __init__(self, group, d_w, d_h, w, h):
        super().__init__(group)
        self.DEVIDED_WIDTH, self.DEVIDED_HEIGHT, self.WIDTH, self.HEIGHT = d_w, d_h, w, h
        self.image = pygame.transform.smoothscale(pygame.image.load('data/sprites/spaceships/player_spaceship.png'),
                                             (int(80 * self.DEVIDED_WIDTH), int(80 * self.DEVIDED_WIDTH)))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2 + 300))

    def update(self, direction):
        if self.rect.x + direction in range(self.WIDTH - int(80 * self.DEVIDED_WIDTH)):
            self.rect.x += direction