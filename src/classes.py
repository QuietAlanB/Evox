import math
import pygame
from screen import screen
from vector2 import Vector2

pygame.init()

class Consumable:
    def __init__(self, pos, color, heal = 0):
        self.pos = pos
        self.color = color
        self.heal = heal

    def onConsume(self, creature):
        if self.pos == creature.pos:
            return True
        return False

    def update(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, 10, 10))
        

class Creature:
    def __init__(self, pos, color, hunger = 100, maxHunger = 100, hungerRate = 1, speed = 1, reproductiveUrge = 0, reproductiveUrgeRate = 1):
        self.pos = pos
        self.color = color

        # === health ===
        self.hunger = hunger
        self.maxHunger = maxHunger
        self.hungerRate = hungerRate

        # === movement ===
        self.moving = False
        self.speed = speed

        # === reproduction ===
        self.reproductiveUrge = reproductiveUrge
        self.reproductiveUrgeRate = reproductiveUrgeRate
        

    def move(self, x, y):
        self.pos = Vector2(x, y)

    def update(self):
        self.health -= 0.5

        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, 10, 10))