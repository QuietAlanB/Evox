import pygame
from globals import *

class Food:
        def __init__(self, pos, hunger, heal):
                self.pos = pos * tileSize
                self.hunger = hunger
                self.heal = heal

        def Update(self):
                pass

        def Draw(self):
                pygame.draw.rect(
                        screen, (0, 225, 0), 
                        (self.pos.x, self.pos.y, tileSize, tileSize)
                        )