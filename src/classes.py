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
    def __init__(self, pos, color, health = 100):
        self.pos = pos
        self.color = color
        self.health = health
        self.maxHealth = health

    def move(self, x, y):
        mx = self.pos.x + x * 10
        my = self.pos.y + y * 10
        return Vector2(mx, my)

    def update(self):
        self.health -= 0.5

        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, 10, 10))