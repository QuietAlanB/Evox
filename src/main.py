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
continueT = False
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

    # ===== food/creature collision =====
    for f in food:
        for c in creatures:
            if f.onConsume(c):
                try:
                    food.remove(f)
                except:
                    pass
                c.health += f.heal
        
        
    # ===== food update =====
    for f in food:
        f.update()


    # ===== creature update =====
    for c in creatures:
        m = c.move(random.randint(-1, 1), random.randint(-1, 1))
        if not (m.x > 880 or m.x < 0 or m.y > 880 or m.y < 0):
            c.pos = m

        # === some creature health bounds ===
        if c.health <= 0:
            creatures.remove(c)
        if c.health > c.maxHealth:
            c.health = c.maxHealth

        c.color = ((c.health / 100) * 255, 0, 0)
        c.update()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1