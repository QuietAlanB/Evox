import pygame
import random
from vector2 import Vector2
from classes import *
from screen import screen

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


# ===== defining variables =====
creatures = []
food = []

# === creature spawning ===
for i in range(100):
    c = Creature(Vector2(random.randrange(0, 900, 10), random.randrange(0, 900, 10)), (255, 0, 0))
    creatures.append(c)

# === food spawning ===
for i in range(1000):
    f = Consumable(Vector2(random.randrange(0, 900, 10), random.randrange(0, 900, 10)), (0, 255, 0), random.randint(50, 100))
    f.color = (0, (f.heal / 100) * 255, 0)

    food.append(f)

# ===== main loop =====
while running:
    mousePos = Vector2( pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0] )
    pressed = pygame.key.get_pressed()

    # ===== event loop =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1