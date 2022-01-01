import pygame

class Bird(object):
    def __init__(self, x, y, end) -> None:
        self.x = x
        self.y = y
        self.width = 30
        self.height = 23
        self.path = [x, end]
        self.walk_count = 0
        self.vel = 3
        self.visible = True

    flight_right = [pygame.image.load('sprites/bird/BFR1.png'), pygame.image.load('sprites/bird/BFR2.png')]
    flight_left = [pygame.image.load('sprites/bird/BFL1.png'), pygame.image.load('sprites/bird/BFL2.png')]

    def draw(self, win) -> None:
        if self.visible:
            self.move()
            if self.walk_count + 1 >= 10:
                self.walk_count = 0
            
            if self.vel > 0:
                win.blit(self.flight_right[self.walk_count//5], (self.x,self.y))
                self.walk_count += 1
            else:
                win.blit(self.flight_left[self.walk_count//5], (self.x,self.y))
                self.walk_count += 1

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0