import os
import random
import pygame
from GameManager import GameManager
from Creature import Creature
from Food import Food
from vector2 import Vector2
from globals import *

GameMan = GameManager()
running = True
framerate = 60
clock = pygame.time.Clock()

c = Creature(Vector2(2, 2),
             {"amount":100, "max":100, "regen":0.5},
             {"amount":100, "max":100, "loss":1},
             {"amount":0, "max":100, "rate":1},
             {"speed":3, "sight":7}
             )

f = Food(Vector2(10, 10), 20, 5)

GameMan.AddCreature(c)
GameMan.AddFood(f)

c.TargetFood(f)

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        screen.fill((0, 0, 0))

        GameMan.Update()
        GameMan.Draw()

        pygame.display.update()
        clock.tick(framerate)