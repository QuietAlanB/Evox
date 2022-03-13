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

t = Creature(Vector2(450, 450), 3, 45, (255, 0, 0), Vector2(1, 0))

# ===== main loop =====
while running:
    mousePos = Vector2( pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0] )
    pressed = pygame.key.get_pressed()

    # ===== event loop =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    screen.fill((0, 0, 0))

    t.move(2)

    t.drawUpdate()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1