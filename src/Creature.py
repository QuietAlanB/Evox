import pygame
from globals import *
from vector2 import Vector2

class Creature:
        def __init__(self, pos, health, hunger, reproduction, traits):
                self.pos = pos * tileSize

                self.health = health
                self.hunger = hunger
                self.reproduction = reproduction
                self.traits = {
                        "sight": traits['sight'],
                        "speed": traits['speed'],
                        "reprRate": self.reproduction['rate']
                }

                self.dir = Vector2(0, 1)

                self.moveTicks = 0
                self.requiredMoveTicks = 30


        def Move(self, amount):
                amount *= tileSize
                self.pos += self.dir * amount

        def Rotate(self, amount):
                if amount < 0: 
                        amount = -(abs(amount) % 4)
                else: 
                        amount %= 4
                
                if amount == 4 or amount == -4 or amount == 0: 
                        self.dir = self.dir
                elif amount == 2 or amount == -2: 
                        self.dir = Vector2(-self.dir.x, -self.dir.y)
                elif amount == 1 or amount == -3: 
                        self.dir = Vector2(self.dir.y, -self.dir.x)
                elif amount == -1 or amount == 3: 
                        self.dir = Vector2(-self.dir.y, self.dir.x)
                        

        def Update(self):
                self.moveTicks += self.speed

                if self.moveTicks > self.requiredMoveTicks:
                        self.Move(1)
                        self.moveTicks = 0


        def Draw(self):
                pygame.draw.rect(
                        screen, colors['male'], 
                        (self.pos.x, self.pos.y, tileSize, tileSize)
                        )