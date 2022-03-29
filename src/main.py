import os
import random
from globals import *

pygame.init()

# ======= pygame variables =======
running = True
clock = pygame.time.Clock()
framerate = 60
ticks = 0


# ======= functions =======
def everyTick(tick):
    if ticks % tick == 0:
        return True
    return False



def clamp(value, min, max):
    if value < min: value = min
    if value > max: value = max
    return value



# ======= food =======
class Food:
    def __init__(self, pos, color, health, hunger):
        self.pos = pos * tileSize
        self.color = color
        self.health = health
        self.hunger = hunger
    
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, tileSize, tileSize))



# ======= creature =======
class Creature:
    def __init__(self, pos, color, dir, age, health, hunger, reproduction, traits):
        self.pos = pos * tileSize
        self.color = color
        self.dir = dir * tileSize

        self.foodInfo = {"food":None}

        # ===== stats =====
        # age:    amount / max / gain
        # health: amount / max / regen
        # hunger: amount / max / loss
        # repr:   amount / max
        # traits: speed / sight / reprRate
        self.age = age
        self.health = health
        self.hunger = hunger
        self.reproduction = reproduction
        self.traits = traits
        self.traits['sight'] *= tileSize

        self.dead = False
        self.lowHunger = False

        # ===== moving =====
        self.maxSpeed = framerate
        self.moveTicks = 0



    # ======= movement =======
    def move(self, amount):
        self.pos += self.dir * amount

    def turn(self, amount):
        # ===== negative adjustments =====
        if amount < 0: amount = -(abs(amount) % 4)
        else: amount %= 4
        
        # ===== actual rotations =====
        if amount == 4 or amount == -4 or amount == 0: self.dir = self.dir
        elif amount == 2 or amount == -2: self.dir = Vector2(-self.dir.x, -self.dir.y)
        elif amount == 1 or amount == -3: self.dir = Vector2(self.dir.y, -self.dir.x)
        elif amount == -1 or amount == 3: self.dir = Vector2(-self.dir.y, self.dir.x)



    # ======= some functions for changing variables =======
    def targetFood(self, food):
       self.foodInfo['food'] = food



    # ======= moving to things and similar functions =======
    def moveRandomly(self):
        if random.randint(1, 3) == 1: self.turn( random.choice( [1, -1] ) )
        else: self.move(1)


    def moveToFood(self):
        foodPos = self.foodInfo['food'].pos
        dx = foodPos.x - self.pos.x
        dy = foodPos.y - self.pos.y

        # ===== move on x axis =====
        if dx >= dy:
            if dx > 0:
                if self.dir != Vector2(tileSize, 0): self.turn(1)
                else: self.move(1)

            else:
                if self.dir != Vector2(-tileSize, 0): self.turn(-1)
                else: self.move(1)


        # ===== move on y axis =====
        else:
            if dy > 0:
                if self.dir != Vector2(0, tileSize): self.turn(-1)
                else: self.move(1)

            else:
                if self.dir != Vector2(0, -tileSize): self.turn(1)
                else: self.move(1)



    # ======= move update =======
    def moveUpdate(self):

        if self.moveTicks > self.maxSpeed:
            self.moveTicks = 0

            if self.foodInfo['food'] != None: self.moveToFood()
            else: self.moveRandomly()

        self.moveTicks += self.traits['speed']



    # ======= stats update =======
    # THIS NEEDS TO BE CALLED EVERY SECOND, NOT TICK
    def statsUpdate(self):
        # ===== basic stat gain =====
        self.age['amount'] += self.age['gain']
        if not self.lowHunger: self.health['amount'] += self.health['regen']
        self.hunger['amount'] -= self.hunger['loss']
        self.reproduction['amount'] += self.traits['reprRate']

        # ===== low hunger effects =====
        if self.hunger['amount'] <= self.hunger['max'] / 5: 
            self.lowHunger = True
        else: 
            self.lowHunger = False
        if self.hunger['amount'] < 0: self.health['amount'] -= self.health['max'] / 30

        # ===== death =====
        if self.health['amount'] < 0: self.dead = True
        if self.dead: creatures.remove(self)

        # ===== clamp =====
        self.health['amount'] = clamp(self.health['amount'], 0, self.health['max'])
        self.hunger['amount'] = clamp(self.hunger['amount'], 0, self.hunger['max'])
        self.reproduction['amount'] = clamp(self.reproduction['amount'], 0, self.reproduction['max'])



    # ======= draw update =======
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, tileSize, tileSize))
        if self.dir.x < 0: pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y, tileSize / 5, tileSize))
        if self.dir.x > 0: pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x + tileSize - (tileSize / 5), self.pos.y, tileSize / 5, tileSize))
        if self.dir.y < 0: pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y, tileSize, tileSize / 5))
        if self.dir.y > 0: pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y + tileSize - (tileSize / 5), tileSize, tileSize / 5))



# ===== defining variables =====
creatures = []

for i in range(1):
    c = Creature(Vector2(22, 22), (255, 0, 0), Vector2(-1, 0), 
                {"amount":0, "max":80},
                {"amount":100, "max":100, "regen":0.5},
                {"amount":100, "max":100, "loss":1},
                {"amount":0, "max":100},
                {"speed":5, "sight":5, "reprRate":1})

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
    
    for creature in creatures:
        creature.moveUpdate()
        creature.drawUpdate()

    pygame.display.update()
    clock.tick(framerate)
    ticks += 1