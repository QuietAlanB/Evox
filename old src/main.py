from ctypes import c_uint32
import os
import pygame
import random
from vector2 import Vector2
from classes import *
from globals import *

pygame.init()

# ===== pygame variables =====
running = True
clock = pygame.time.Clock()
framerate = 60
ticks = 0


# ===== functions =====
def everyTick(tick):
    if ticks == tick:
        return True
    return False

# ===== defining some variables =====
creatures = []
food = []


# ===== creatures and stuff =====
for i in range(50):
    c = Creature(
                Vector2(random.randint(0, 900), random.randint(0, 900)), 3, 180, (255, 0, 0), Vector2(1, 0), 
                {"amount": 0, "max": 120, "gain": 1}, 
                {"amount": 100, "max": 100, "regen": 0.1}, 
                {"amount":100, "max":100, "loss":1}, 
                {"amount":0, "max":100}, 
                {"speed":1, "sight": 50, "reprRate":1}
                )

    f = Food(Vector2(random.randint(0, 900), random.randint(0, 900)), (0, 255, 0), 5, 10)
    
    '''
    c = Creature(
                Vector2(450, 450), 3, 0, (255, 0, 0), Vector2(1, 0), 
                {"amount": 100, "max": 100, "regen": 0.1}, 
                {"amount":100, "max":100, "loss":1}, 
                {"amount":0, "max":100}, 
                {"speed":1, "sight": 100, "reprRate":1}
                )

    f = Food(Vector2(400, 450), (0, 255, 0), 5, 10)
    '''

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
        c.moveToFood()

        if c.foodInfo['food'] not in food: c.searchFood(None)
        if c.dead:
            creatures.remove(c)
            continue

        # === creature-food updates ===
        for f in food:
            c.searchFood(f)

            if f.onConsume(c):
                c.eatFood(f)
                food.remove(f)

        c.moveUpdate()
        c.drawUpdate()

    # ===== food updates =====
    for f in food:
        f.drawUpdate()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1