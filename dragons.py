import random
from collections import deque

from settings import *


class Head(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.image = pygame.image.load(image('head.png'))

    def move(self, direction, speed):
        self.x += direction[0] * speed
        self.y += direction[1] * speed

        if self.x < 0:
            self.x = WINDOW_WIDTH - self.size
        if self.x > WINDOW_WIDTH - self.size:
            self.x = 0
        if self.y < 0:
            self.y = WINDOW_HEIGHT - self.size
        if self.y > WINDOW_HEIGHT - self.size:
            self.y = 0

        self.rect.topleft = self.x, self.y


class Body(pygame.sprite.Sprite):
    def __init__(self, head):
        super().__init__()
        self.size = head.size
        self.rect = pygame.Rect(head.x, head.y, self.size, self.size)

    def move(self, x, y):
        self.rect.topleft = x, y


class Dragon(pygame.sprite.Sprite):
    DIRECTIONS = {'left': (-1, 0),
                  'right': (1, 0),
                  'up': (0, -1),
                  'down': (0, 1)}

    def __init__(self, keys=None):
        super().__init__()
        keys = keys if keys else {'left': pygame.K_LEFT,
                                  'right': pygame.K_RIGHT,
                                  'up': pygame.K_UP,
                                  'down': pygame.K_DOWN}
        self.speed = 5
        self.color = tuple(random.randint(0, 255) for _ in range(3))
        self.keys = keys
        self.size = 32
        self.head = Head(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), self.size)
        self.body = deque([Body(self.head),
                           Body(self.head),
                           Body(self.head),
                           Body(self.head),
                           Body(self.head)])
        self.direction = random.choice(list(self.DIRECTIONS.values()))
        self.length = len(self.body)

    def move(self):
        self.head.move(self.direction, self.speed)
        self.body.appendleft(self.body.pop())
        self.body[0].move(self.head.x, self.head.y)

    def update(self):
        self.move()

    def input(self, key):
        for direction, value in self.keys.items():
            if key == value and self.direction != (-self.DIRECTIONS[direction][0], -self.DIRECTIONS[direction][1]):
                self.direction = self.DIRECTIONS[direction]

    def eat(self):
        self.length += 5
        for _ in range(5):
            self.body.append(Body(self.head))

    def get_hit(self):
        self.length -= 1
        for _ in range(5):
            self.body.pop()

    def draw(self, window):
        for body in self.body:
            pygame.draw.rect(window, self.color, body.rect)
        window.blit(self.head.image, self.head.rect)
