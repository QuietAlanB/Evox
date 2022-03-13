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


# ===== some function =====
def everyTick(tick):
    if ticks % tick == 0:
        return True
    return False


def average(lst):
    n = 0

    for item in lst:
        n += item

    if len(lst) != 0: n /= len(lst)
    else: n = 0

    return n


# ===== defining variables =====
creatures = []
food = []
lineGraphPopulation = []
lineGraphReprRate = []
reprRateAvg = []
viewingLineGraph = False
extinct = False


# === creature spawning ===
for i in range(10):
    c = Creature(Vector2(random.randrange(0, 890, 10), random.randrange(0, 890, 10)), random.randint(0, 1), 0, 140, 100, 100, 0.1, 100, 100, 1, 0, 100, 1.25, 3, 9, random.randint(0, 1), Vector2(0, 10), 0)
    creatures.append(c)

for i in range(0):
    f = Food(Vector2(random.randrange(0, 900, 10), random.randrange(0, 900, 10)), (0, 255, 0), 1, 5)
    food.append(f)

# ===== main loop =====
while running:
    mousePos = Vector2( pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0] )
    pressed = pygame.key.get_pressed()

    # ===== event loop =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            viewingLineGraph = not viewingLineGraph

   
    screen.fill((0, 0, 0))

    generations = []

    for f in food:
        if not viewingLineGraph:
            f.drawUpdate()

    reprRateAvg = []

    for c in creatures:
        generations.append(c.generation)

        if c.dead:
            creatures.remove(c)
            continue


        # === mate target ===
        if (c.reproductiveUrge > (c.maxReproductiveUrge / 4)) and ((100 - c.reproductiveUrge) < c.hunger) and (c.mateInfo['mate'] == None) and (c.age > c.maxAge / 3) and not c.lowHunger:
            for c2 in creatures:
                c.targetMate(c2)


        # === mate ===
        if c.mateInfo['mate'] != None:
            children = c.mateWith(c.mateInfo['mate'])

            if children != []:
                for child in children:
                    creatures.append(child)
                
                continue


        # === food/creature update ===
        for f in food:
            if c.inSight(f.pos) and c.foodInfo['food'] == None and not c.wellFed:
                c.targetFood(f)

            if f.onConsume(c):
                c.eatFood(f)
                food.remove(f)
                    

        # === if food gets eaten ===
        if c.foodInfo['food'] not in food:
            c.targetFood(None)

        # === stats update ===
        if everyTick(framerate):
            c.statsUpdate()

        if not viewingLineGraph:
            c.drawUpdate()

        c.moveUpdate()
        reprRateAvg.append(c.traits['reprRate'])

    # ===== every second updates =====
    if everyTick(framerate):
        lineGraphPopulation.append(len(creatures))
        lineGraphReprRate.append(average(reprRateAvg))

        for i in range(4):
            if len(food) < 300:
                f = Food(Vector2(random.randrange(0, 900, 10), random.randrange(0, 900, 10)), (0, 255, 0), 0.5, random.randint(5, 20))
                food.append(f)

    # ===== extinct =====
    if len(creatures) == 0: extinct = True

    # ===== line graphs =====
    if viewingLineGraph:
        for x in range(9000):
            try: pygame.draw.circle(screen, (255, 255, 255), (x, screenSize.y / 2 - lineGraphPopulation[x]), 1)
            except IndexError: pass
            
            try: pygame.draw.circle(screen, (0, 230, 255), (x, screenSize.y / 2 - lineGraphReprRate[x]), 1)
            except IndexError: pass

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1