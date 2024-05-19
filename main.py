import displays
from settings import *


class Game:
    def __init__(self, display):
        pygame.init()
        self.display = display

    def run(self):
        while self.display:
            self.display = self.display.run()


if __name__ == "__main__":
    game = Game(displays.MainMenu())
    game.run()
