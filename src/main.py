import os
import random
from globals import *

pygame.init()

# ===== pygame variables =====
running = True
clock = pygame.time.Clock()
framerate = 60
ticks = 0


# ===== every tick =====
def everyTick(tick):
    if ticks % tick == 0:
        return True
    return False



# ===== average =====
def average(lst):
    n = 0

    for item in lst:
        n += item

    if len(lst) != 0: n /= len(lst)
    else: return 0

    return n



# ======= clamp =======
def clamp(value, min, max):
    if value < min: value = min
    if value > max: value = max
    return value



# ======= obstacle =======
class Obstacle:
    def __init__(self, pos, color):
        self.pos = pos * tileSize
        self.color = color


    # ===== draw update =====
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, tileSize, tileSize))



# ======= obstacle =======
class Creature:
    def __init__(self, pos, color):
        self.pos = pos * tileSize
        self.color = color
        self.pathInfo = {"pos":None}


    # ===== start pathfinding =====
    def startPathfinding(self, target):
        end = target * tileSize
        start = self.pos
        self.pathInfo = {"pos":end}

        


    # ===== draw update =====
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, tileSize, tileSize))



# ===== defining variables =====
creatures = []
obstacles = []

c = Creature(Vector2(3, 3), (255, 0, 0))
o = Obstacle(Vector2(7, 7), (150, 150, 150))

obstacles.append(o)
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
    
    c.drawUpdate()
    o.drawUpdate()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1