import os
import random
import pygame
from Creature import Creature
from Food import Food
from vector2 import Vector2
from globals import *
import globals

running = True
framerate = 60
clock = pygame.time.Clock()

for i in range(12):
        c = Creature(Vector2(random.randint(0, 44), random.randint(0, 45)),
                random.choice(['male', 'female']),
                {"amount":0, "max":gameMan.maxAge},
                {"amount":100, "max":100, "regen":0.5},
                {"amount":100, "max":100, "loss":1},
                {"amount":0, "max":100, "rate":1},
                {"speed":3, "sight":7, "threatResponse":random.randint(0, 1)}
                )

        gameMan.AddCreature(c)


for i in range(150):
        f = Food(Vector2(random.randint(0, 44), random.randint(0, 44)), 20, 5)
        gameMan.AddFood(f)

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        screen.fill((0, 0, 0))

        gameMan.OnTimerUpdate(framerate)
        gameMan.Update()
        gameMan.Draw()

        globals.ticks += 1

        pygame.display.update()
        clock.tick(framerate)