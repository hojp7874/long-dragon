import random

from settings import *


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 20
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH - self.size),
                                random.randint(0, WINDOW_HEIGHT - self.size),
                                self.size, self.size)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)

    def draw(self, window):
        window.blit(self.image, self.rect)
