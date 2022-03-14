import random
import pygame
from screen import *
from pygame import gfxdraw
import math


# ======= functions =======
def rotatePoint(point, center, angle):
    s = math.sin(angle)
    c = math.cos(angle)

    # ===== front point =====
    point -= center

    xNew = point.x * c - point.y * s
    yNew = point.x * s + point.y * c

    point = Vector2(xNew, yNew) + center
    return point


# ======= clamp =======
def clamp(value, start, end):
    if value > end: value = end
    if value < start: value = start
    return value



class Food:
    def __init__(self, pos, color, size, hunger, heal = 0):
        self.pos = pos
        self.color = color
        self.radius = size
        self.hunger = hunger
        self.heal = heal

    # ===== on consume =====
    def onConsume(self, creature):
        frontDist = ((self.pos.x - creature.front.x) ** 2 + (self.pos.y - creature.front.y) ** 2)
        topDist = ((self.pos.x - creature.top.x) ** 2 + (self.pos.y - creature.top.y) ** 2)
        bottomDist = ((self.pos.x - creature.bottom.x) ** 2 + (self.pos.y - creature.bottom.y) ** 2)
        radSqr = self.radius ** 2

        # === if its lower ===
        if (frontDist <= radSqr or
            topDist <= radSqr or
            bottomDist <= radSqr): 
            return True

        return False


    # ===== draw update =====
    def drawUpdate(self):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)




class Creature:
    def __init__(self, pos, size, angle, color, dir, health, hunger, reproduction, traits):
        self.pos = pos
        self.initialPos = pos
        self.color = color
        self.size = size
        self.dir = dir
        self.angle = angle
        self.rotation = self.angle * (math.pi / 180)
        self.center = self.pos

        # ==== info ====
        self.health = health
        self.hunger = hunger
        self.reproduction = reproduction
        self.traits = traits
        self.foodInfo = {"food": None}
        self.mateInfo = {"mate": None}

        # ==== point positions ====
        self.front = Vector2(self.pos.x + self.dir.x * self.size, self.pos.y + self.dir.y * self.size)
        self.top = Vector2(self.pos.x - self.size, self.pos.y + self.size)
        self.bottom = Vector2(self.pos.x - self.size, self.pos.y - self.size)

        # ==== point rotations ====
        # note: i cant use self.turn() because it adjusts the angle in the function
        self.front = rotatePoint(self.front, self.center, self.angle)
        self.top = rotatePoint(self.top, self.center, self.angle)
        self.bottom = rotatePoint(self.bottom, self.center, self.angle)

        # ==== point scaling ====
        self.scale(self.size)

        # ==== other ====
        self.turnInfo = {"turning": False, "angle": 0, "amount":1}



    # ======= scale =======
    def scale(self, scaleFactor):
        self.size += scaleFactor

        # ==== adjust point positions ====
        self.front = Vector2(self.pos.x + self.dir.x * self.size, self.pos.y + self.dir.y * self.size)
        self.top = Vector2(self.pos.x - self.size, self.pos.y + self.size)
        self.bottom = Vector2(self.pos.x - self.size, self.pos.y - self.size)

        # ==== adjust point rotations ====
        self.front = rotatePoint(self.front, self.center, self.rotation)
        self.top = rotatePoint(self.top, self.center, self.rotation)
        self.bottom = rotatePoint(self.bottom, self.center, self.rotation)



    # ======= turn =======
    def turn(self, angle):
        self.angle += angle
        angle = angle * (math.pi / 180)
        self.rotation += angle

        # ==== point rotations ====
        self.front = rotatePoint(self.front, self.center, angle)
        self.top = rotatePoint(self.top, self.center, angle)
        self.bottom = rotatePoint(self.bottom, self.center, angle)



    # ======= move =======
    def move(self, amount):
        self.pos.x += amount * math.cos(self.angle * (math.pi / 180))
        self.pos.y += amount * math.sin(self.angle * (math.pi / 180))

        # ==== adjust point positions ====
        self.front = Vector2(self.pos.x + self.dir.x * self.size, self.pos.y + self.dir.y * self.size)
        self.top = Vector2(self.pos.x - self.size, self.pos.y + self.size)
        self.bottom = Vector2(self.pos.x - self.size, self.pos.y - self.size)

        # ==== adjust point rotations ====
        self.front = rotatePoint(self.front, self.center, self.rotation)
        self.top = rotatePoint(self.top, self.center, self.rotation)
        self.bottom = rotatePoint(self.bottom, self.center, self.rotation)



    # ======= move pos =======
    def movePos(self, point):
        self.pos = point

        # ==== adjust point positions ====
        self.front = Vector2(self.pos.x + self.dir.x * self.size, self.pos.y + self.dir.y * self.size)
        self.top = Vector2(self.pos.x - self.size, self.pos.y + self.size)
        self.bottom = Vector2(self.pos.x - self.size, self.pos.y - self.size)

        # ==== adjust point rotations ====
        self.front = rotatePoint(self.front, self.center, self.rotation)
        self.top = rotatePoint(self.top, self.center, self.rotation)
        self.bottom = rotatePoint(self.bottom, self.center, self.rotation)



    # ======= target food =======
    def searchFood(self, food):
        if food == None: self.foodInfo['food'] = None
        elif abs(self.pos - food.pos) < Vector2(self.traits['sight'], self.traits['sight']): 
            self.foodInfo['food'] = food
            self.turnInfo['turning'] = False

    

    # ======= move to food =======
    def moveToFood(self):
        if self.foodInfo['food'] == None: return

        creatureDir = (self.front - self.pos).normalized()
        foodDir = (self.foodInfo['food'].pos - self.pos).normalized()

        lookAmount = creatureDir.dot(foodDir)
        lookThreshold = 0.95

        distance = abs(self.front - self.pos)
        
        if not lookAmount > lookThreshold: 
            self.turn(1)

        if lookAmount > lookThreshold: pass



    # ======= eat food =======
    def eatFood(self, food):
        self.hunger['amount'] += food.hunger
        self.foodInfo['food'] = None



    # ======= stats update =======
    def statsUpdate(self):
        self.health['amount'] += self.health['regen']
        self.hunger['amount'] -= self.hunger['loss']
        self.reproduction['amount'] += self.traits['reprRate']

        self.health['amount'] = clamp(self.health['amount'], 0, 100)
        self.hunger['amount'] = clamp(self.hunger['amount'], 0, 100)
        self.reproduction['amount'] = clamp(self.reproduction['amount'], 0, 100)





    # ======= move update =======
    def moveUpdate(self):
        self.move(self.traits['speed'])


        # ===== no food so it moves randomly =====
        if self.foodInfo['food'] == None:
            
            # === start turning randomly ===
            if not self.turnInfo['turning']:
                self.turnInfo['angle'] = random.randrange(-110, 110, self.traits['speed'])
                self.turnInfo['amount'] = random.choice([1 * self.traits['speed'], -1 * self.traits['speed']])
                self.turnInfo['turning'] = True

            # === in the process of turning ===
            if self.turnInfo['turning']:
                if self.angle % 360 != self.turnInfo['angle'] % 360: self.turn(self.turnInfo['amount'])
                else: self.turnInfo['turning'] = False

        else:
            self.moveToFood()



    # ======= draw update =======
    def drawUpdate(self):
        self.center = self.pos

        # === dont allow outside map ===
        self.pos.x = clamp(self.pos.x, 0, 900)
        self.pos.y = clamp(self.pos.y, 0, 900)

        points = [ (self.front.x, self.front.y),
                   (self.top.x, self.top.y),
                   (self.bottom.x, self.bottom.y) ]

        gfxdraw.aapolygon(screen, points, self.color)
        gfxdraw.filled_polygon(screen, points, self.color)