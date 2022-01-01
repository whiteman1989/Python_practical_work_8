import pygame

class HealthBar(object):
    def __init__(self, height: int, width: int) -> None:
        super().__init__()
        self.height = height
        self.width = width
    
    def draw(self, x: int, y: int, health: int, win) -> None:
            pygame.draw.rect(win, (255, 0, 0), (x, y - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (x, y - 20, 50 - (5 * (10 - health)), 10))
