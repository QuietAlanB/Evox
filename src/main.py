from ctypes import c_uint32
import os
import pygame
import random
from vector2 import Vector2
from classes import *
from screen import *

pygame.init()

# ===== pygame variables =====
running = True
clock = pygame.time.Clock()
framerate = 60
ticks = 0


# ===== defining some variables =====
creatures = []
food = []


# ===== creatures and stuff =====
c = Creature(
            Vector2(450, 450), 3, 45, (255, 0, 0), Vector2(1, 0), 
            {"amount": 100, "max": 100, "regen": 0.1}, 
            {"amount":100, "max":100, "loss":1}, 
            {"amount":0, "max":100}, 
            {"speed":5, "sight": 7, "reprRate":1}
            )

f = Food(Vector2(400, 400), (0, 255, 0), 5)

food.append(f)
creatures.append(c)


# ===== main loop =====
while running:
    mousePos = Vector2( pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0] )
    pressed = pygame.key.get_pressed()

    # ===== event loop =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    screen.fill((0, 0, 0))

    # ===== creature updates =====
    for c in creatures:
        for f in food:
            c.targetFood(f)

            if f.onConsume(c):
                food.remove(f)

        c.drawUpdate()

    # ===== food updates =====
    for f in food:
        f.drawUpdate()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1