from abc import ABC, abstractmethod

from dragons import Dragon
from items import Food
from settings import *


class Display(ABC):
    def __init__(self):
        self.window = WINDOW
        self.running = False
        self.clock = pygame.time.Clock()
        self.next_display = None

    @abstractmethod
    def _update(self): ...

    def update(self):
        self._update()
        pygame.display.flip()
        self.clock.tick(120)

    @abstractmethod
    def input(self, key): ...

    def run(self):
        self.running = True
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.next_display = MainMenu
                    self.input(event.key)
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        return self.next_display() if self.next_display else None

    def checkout(self, display):
        self.running = False
        self.next_display = display


class MainMenu(Display):
    def __init__(self):
        super().__init__()
        self.buttons = ["Single Play", "Multi Play", "Quit"]
        self.links = {
            "Single Play": SinglePlay,
            "Multi Play": MultiPlay,
            "Quit": None
        }
        self.selected = 0
        self.image = pygame.image.load(image("bg.jpeg"))

    def _update(self):
        self.window.blit(self.image, (0, 0))
        for i, button in enumerate(self.buttons):
            color = (255, 255, 255) if i == self.selected else (128, 128, 0)
            text = pygame.font.Font(None, 36).render(button, True, color)
            self.window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 100 + 50 * i))

    def input(self, key):
        if key == pygame.K_UP:
            self.selected -= 1
            self.selected %= len(self.buttons)
        if key == pygame.K_DOWN:
            self.selected += 1
            self.selected %= len(self.buttons)
        if key == pygame.K_RETURN:
            self.checkout(self.links[self.buttons[self.selected]])


class SinglePlay(Display):
    def __init__(self):
        super().__init__()
        self.dragon = Dragon()
        self.food = Food()

    def input(self, key):
        self.dragon.input(key)

    def _update(self):
        self.dragon.update()
        if self.food.rect.colliderect(self.dragon.head.rect):
            self.dragon.eat()
            self.food = Food()

        self.window.fill((0, 0, 0))
        self.dragon.draw(self.window)
        self.food.draw(self.window)


class MultiPlay(Display):
    def __init__(self):
        super().__init__()
        self.dragons = [Dragon({'up': pygame.K_UP,
                                'down': pygame.K_DOWN,
                                'left': pygame.K_LEFT,
                                'right': pygame.K_RIGHT}),
                        Dragon({'up': pygame.K_w,
                                'down': pygame.K_s,
                                'left': pygame.K_a,
                                'right': pygame.K_d})]
        self.food = Food()

    def input(self, key):
        for dragon in self.dragons:
            dragon.input(key)

    def _update(self):
        for dragon in self.dragons:
            dragon.update()
            if self.food.rect.colliderect(dragon.head.rect):
                dragon.eat()
                self.food = Food()

            other_dragons = [other for other in self.dragons if other != dragon]
            if dragon.body[-1].rect.collidelist([other_dragon.head.rect for other_dragon in other_dragons]) != -1:
                dragon.get_hit()

            if len(dragon.body) < 3:
                self.checkout(MainMenu)

        self.window.fill((0, 0, 0))
        for dragon in self.dragons:
            dragon.draw(self.window)
        self.food.draw(self.window)
