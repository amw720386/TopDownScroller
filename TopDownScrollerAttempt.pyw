import pygame
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Top Down Scroller')


class CollidingObject:
    def collide(self, colliders, player=''):
        for collider in colliders:
            if collider.hitbox:
                if self.x == collider.origx + collider.sizex and self.y + self.sizex >= collider.origy and self.y <= collider.origy + collider.sizey:
                    self.x = self.prevx
                    self.y = self.prevy
                if self.x + self.sizex == collider.origx and self.y + self.sizex >= collider.origy and self.y <= collider.origy + collider.sizey:
                    self.x = self.prevx
                    self.y = self.prevy
                if self.y == collider.origy + collider.sizey and self.x + self.sizey >= collider.origx and self.x <= collider.origx + collider.sizex:
                    self.x = self.prevx
                    self.y = self.prevy
                if self.y + self.sizey == collider.origy and self.x + self.sizey >= collider.origx and self.x <= collider.origx + collider.sizex:
                    self.x = self.prevx
                    self.y = self.prevy
                if player:
                    self.collide([player])


class Player(CollidingObject):
    def __init__(self, x, y, color, sizex, sizey):
        self.rect = pygame.Rect(
            (screen_width/2), (screen_height/2), sizex, sizey)
        self.origx = x
        self.origy = y
        self.sizex = sizex
        self.sizey = sizey
        self.x = x
        self.y = y
        self.prevx = self.x
        self.prevy = self.y
        self.color = color
        self.dashing = False
        self.dashtick = 0
        self.dashlength = 300
        self.hitbox = True

    def draw(self, screen):
        self.origx = self.x
        self.origy = self.y
        pygame.draw.rect(screen, self.color, self.rect)

    def tick(self, keys, objects):
        self.dash(keys, objects)

    def dash(self, keys, objects):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.dashing:
            for tick in range(0, int(self.dashlength/5)):
                self.collide(objects)
                if self.prevx < self.x:
                    self.x += 5
                    self.prevx += 5
                if self.prevx > self.x:
                    self.x -= 5
                    self.prevx -= 5
                if self.prevy < self.y:
                    self.y += 5
                    self.prevy += 5
                if self.prevy > self.y:
                    self.y -= 5
                    self.prevy -= 5

            self.dashing = True
            self.dashtick = 0

        if self.dashing:
            self.dashtick += 1
        if self.dashtick > 120 and self.dashing:
            self.dashing = False


class ScrollableObject:
    def __init__(self, x, y, hitbox, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.origx = x
        self.origy = y
        self.x = x
        self.y = y
        self.hitbox = hitbox

    def scroll(self):
        self.x = self.origx - player.x + int(screen_width/2)
        self.y = self.origy - player.y + int(screen_height/2)


class Wall(ScrollableObject):
    def __init__(self, x, y, hitbox, sizex, sizey):
        super().__init__(x, y, hitbox, sizex, sizey)
        self.rect = pygame.Rect(self.x, self.y, sizex, sizey)

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
        pygame.draw.rect(screen, WHITE, self.rect)


class Enemy(ScrollableObject, CollidingObject):
    def __init__(self, x, y, hitbox, sizex, sizey, speed, hitpoints):
        super().__init__(x, y, hitbox, sizex, sizey)
        self.origx = x
        self.origy = y
        self.speed = speed
        self.hitpoints = hitpoints
        self.triggered = False
        self.prevx = x
        self.prevy = y

    def tick(self, player, colliders):
        self.prevx = self.origx
        self.prevy = self.origy
        if abs(player.x - self.origx) < 400 and abs(player.y - self.origy) < 400:
            self.triggered = True
        if self.triggered:
            self.pathfind(player)
            self.collide(colliders, player)

    def pathfind(self, player):
        self.origx += 5
        self.origy += 5

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
        pygame.draw.rect(screen, RED, self.rect)


player = Player(int((screen_width/2)), int((screen_height/2)), WHITE, 50, 50)
objects = [Wall(100, 100, True, 100, 100), Wall(
    800, 500, True, 150, 50), Enemy(-500, -500, False, 50, 50, 25, 1)]

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        player.x -= 5
    if keys[pygame.K_l]:
        player.x += 5
    if keys[pygame.K_i]:
        player.y -= 5
    if keys[pygame.K_k]:
        player.y += 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.tick(keys, objects)

    player.collide(objects)

    for object in objects:
        object.scroll()
        if type(object).__name__ == 'Enemy':
            object.tick(player, objects)

    player.prevx = player.x
    player.prevy = player.y

    screen.fill(BLACK)

    for object in objects:
        object.draw(screen)

    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)
