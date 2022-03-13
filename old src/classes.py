import math
import pygame
from screen import screen
from vector2 import Vector2
import random

pygame.init()

class Food:
    def __init__(self, pos, color, heal = 0, hunger = 0):
        self.pos = pos
        self.color = color
        self.heal = heal
        self.hunger = hunger

    # ===== when a creature is on the food's position =====
    def onConsume(self, creature):
        if self.pos == creature.pos:
            return True
        return False

    # ===== draw update =====
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, 10, 10))
        

class Creature:
    def __init__(self, pos, gender, age, maxAge,
                health, maxHealth, healthRegen, 
                hunger, maxHunger, hungerLoss, 
                reprUrge, maxReprUrge, reprRate, 
                speed, sight, threatResponse, direction, generation):
        self.pos = pos
        self.color = (0, 0, 0)

        # === basic stats ===
        # 0 = male / 1 = female
        self.gender = gender
        self.age = age
        self.maxAge = maxAge

        if self.gender == 0: self.color = (0, 125, 255)
        if self.gender == 1: self.color = (255, 0, 0)

        # === health ===
        self.health = health
        self.maxHealth = maxHealth
        self.healthRegen = healthRegen

        # === hunger ===
        self.hunger = hunger
        self.maxHunger = maxHunger
        self.hungerLoss = hungerLoss
        self.totalFood = 0

        # === reproduction ===
        self.reproductiveUrge = reprUrge
        self.maxReproductiveUrge = maxReprUrge
        self.reproductiveUrgeRate = reprRate

        # === movement ===
        self.maxSpeed = 30
        self.moveTicks = 0
        self.initialSpeed = speed
        self.speed = speed
        self.sight = sight

        # 0 = calm / 1 = panic
        self.threatResponse = threatResponse

        self.maxTurn = 20
        self.turnTicks = 0
        self.turnFreq = 0.5

        self.lowHunger = False
        self.wellFed = True

        # === other ===
        self.dead = False
        self.foodInfo = {"movingTowards": False, "food": None}
        self.mateInfo = {"movingTowards": False, "mate": None}
        self.traits = {"speed":self.speed, "sight":self.sight, "reprRate":self.reproductiveUrgeRate, "threatResponse":self.threatResponse}
        self.dir = direction
        self.generation = generation
        self.showBars = {"health": True, "hunger": True, "repr": True, "age": True}
        


    # ===== move =====
    def move(self, x, y):
        self.pos += Vector2(x, y)



    # ===== turn =====
    def turn(self, amount):
        if amount < 0: 
            amount = abs(amount) % 4
            amount = -amount

        else: 
            amount %= 4
        
        # == 360 / 0 ==
        if amount == 4 or amount == -4 or amount == 0: self.dir = self.dir
        # == 180 ==
        elif amount == 2 or amount == -2: self.dir = Vector2(-self.dir.x, -self.dir.y)
        # == 90 / -270 ==
        elif amount == 1 or amount == -3: self.dir = Vector2(self.dir.y, -self.dir.x)
        # == -90 / 270 ==
        elif amount == -1 or amount == 3: self.dir = Vector2(-self.dir.y, self.dir.x)



    # ===== on sight =====
    def inSight(self, pos):
        if (abs(self.pos - pos).x <= self.sight * 10 and abs(self.pos - pos).y <= self.sight * 10):
            return True

        return False

    

    # ===== target food =====
    def targetFood(self, food):
        if food == None:
            self.foodInfo['movingTowards'] = False
            self.foodInfo['food'] = None
            return

        self.foodInfo['movingTowards'] = True
        self.foodInfo['food'] = food



    # ===== eat food =====
    def eatFood(self, food):
        self.hunger += food.hunger
        self.totalFood += 1
        self.foodInfo['movingTowards'] = False
        self.foodInfo['food'] = None

        if self.hunger > self.maxHunger: self.hunger = self.maxHunger



    # ===== target mate =====
    def targetMate(self, mate):
        if (self.gender != mate.gender and 
        self.inSight(mate.pos) and 
        (mate.reproductiveUrge > (mate.maxReproductiveUrge / 4)) and 
        ((100 - mate.reproductiveUrge) < mate.hunger) and 
        (mate.mateInfo['mate'] == None) and 
        (mate.age > mate.maxAge / 3) and 
        not mate.lowHunger):

            self.mateInfo['movingTowards'] = True
            self.mateInfo['mate'] = mate

            mate.mateInfo['mate'] = self
            mate.mateInfo['movingTowards'] = True



    # ===== mate =====
    def mateWith(self, mate):
        lastMate = None

        if abs(self.pos.x - mate.pos.x) <= 10 and abs(self.pos.y - mate.pos.y) <= 10 and self.gender != mate.gender:
            lastMate = self.mateInfo['mate']

            self.mateInfo['mate'].mateInfo['movingTowards'] = False
            self.mateInfo['mate'].mateInfo['mate'] = None
            self.mateInfo['movingTowards'] = False
            self.mateInfo['mate'] = None

            childrenAmount = random.randint(1, 3)
            children = []

            # === make children ===
            for i in range(childrenAmount):
                traits = [random.choice([self.traits, mate.traits])]
                traits = traits[0]

                traits = [traits['speed'], traits['sight'], traits['reprRate'], traits['threatResponse']]

                # === mutation and stuff ===
                mutationChance = 4
                mutationList = [0] * mutationChance
                mutationList[mutationChance - 1] = 1

                mutation = random.choice(mutationList)

                # === mutation ===
                if mutation == 1:
                    n = random.randint(0, len(traits) - 1)
                    multiplyAmount = random.choice([1.2, 1.1, 0.9, 0.8])
                    traits[n] *= multiplyAmount

                    if n == 3:
                        if multiplyAmount < 0:
                            traits[n] = 0
                        elif multiplyAmount > 0:
                            traits[n] = 1

                # === creature spawning ===
                c = Creature(mate.pos, random.choice([0, 1]), 0, random.randint(110, 140), 
                            80, self.maxHealth, self.healthRegen, 
                            60, self.maxHunger, self.hungerLoss, 
                            0, self.maxReproductiveUrge, traits[2],
                            traits[0], traits[1], traits[3], random.choice([Vector2(10, 0), Vector2(0, -10), Vector2(0, -10), Vector2(-10, 0)]),
                            max([self.generation, mate.generation]) + 1)

                children.append(c)

            # === reset stuff ===
            self.reproductiveUrge = 0
            lastMate.reproductiveUrge = 0

            return children

        else:
            return []

                

    # ===== move update =====
    def moveUpdate(self):
        # === low hunger ===
        if self.lowHunger:
            if self.threatResponse == 1:
                self.speed = self.initialSpeed * 3.5
        else:
            self.speed = self.initialSpeed


        # === not moving towards any food ===
        if not self.foodInfo['movingTowards'] and not self.mateInfo['movingTowards']:
            self.moveTicks += self.speed
            self.turnTicks += self.turnFreq

            # === turn randomly ===
            if self.turnTicks > self.maxTurn:
                self.turn(random.choice([1, 0, -1]))
                self.turnTicks = 0

            # === move forward ===
            if self.moveTicks > self.maxSpeed:
                self.pos += self.dir
                self.moveTicks = 0


        # === moving towards mate ===
        if self.mateInfo['movingTowards'] and not self.foodInfo['movingTowards']:
            # === right ===
            if self.mateInfo['mate'].pos.x > self.pos.x:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(10, 0): self.turn(1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === down ===
            elif self.mateInfo['mate'].pos.y > self.pos.y:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(0, 10): self.turn(-1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === left ===
            elif self.mateInfo['mate'].pos.x < self.pos.x:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(-10, 0): self.turn(-1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === up ===
            elif self.mateInfo['mate'].pos.y < self.pos.y:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(0, -10): self.turn(1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            self.moveTicks += self.speed



        # === moving towards food ===
        elif not self.mateInfo['movingTowards'] and self.foodInfo['movingTowards']:
            # === right ===
            if self.foodInfo['food'].pos.x > self.pos.x:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(10, 0): self.turn(1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === down ===
            elif self.foodInfo['food'].pos.y > self.pos.y:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(0, 10): self.turn(-1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === left ===
            elif self.foodInfo['food'].pos.x < self.pos.x:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(-10, 0): self.turn(-1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            # === up ===
            elif self.foodInfo['food'].pos.y < self.pos.y:
                if self.moveTicks > self.maxSpeed:
                    if self.dir != Vector2(0, -10): self.turn(1)
                    else: self.pos += self.dir
                    self.moveTicks = 0

            self.moveTicks += self.speed


        # === dont allow food and mate ===
        else:
            if self.hunger < (100 - self.reproductiveUrge): self.mateInfo['movingTowards'] = False
            else: self.foodInfo['movingTowards'] = False


        # === dont allow outside of map ===
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x > 890: self.pos.x = 890
        if self.pos.y < 0: self.pos.y = 0
        if self.pos.y > 890: self.pos.y = 890



    # ===== stats update (these need to happen every second) =====
    def statsUpdate(self):
        self.health += self.healthRegen
        self.hunger -= self.hungerLoss
        self.reproductiveUrge += self.reproductiveUrgeRate
        self.age += 1

        # === set low hunger ===
        if self.hunger < (self.maxHunger / 10): self.lowHunger = True
        else: self.lowHunger = False

        if self.hunger > (self.maxHunger / 1.25): self.wellFed = True
        else: self.wellFed = False

        # === max clamping ===
        if self.hunger > self.maxHunger:
            self.hunger = self.maxHunger

        if self.health > self.maxHealth:
            self.health = self.maxHealth

        if self.reproductiveUrge > self.maxReproductiveUrge:
            self.reproductiveUrge = self.maxReproductiveUrge

        # === damage if panicked ===
        if self.lowHunger:
            if self.threatResponse == 0: self.health -= 1
            elif self.threatResponse == 1: self.health -= 6

        if self.health < 0: self.dead = True
        if self.age > self.maxAge: self.dead = True



    # ===== draw update =====
    def drawUpdate(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, 10, 10))

        if self.dir == Vector2(0, -10): pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y, 10, 2))
        if self.dir == Vector2(0, 10): pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y + 8, 10, 2))
        if self.dir == Vector2(-10, 0): pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x, self.pos.y, 2, 10))
        if self.dir == Vector2(10, 0): pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos.x + 8, self.pos.y, 2, 10))

        if self.showBars:
            # health bar
            bgColor = (160, 160, 160)
            yOffset = 2
            barOffset = 5
            offset = yOffset + barOffset

            if self.showBars['health']:
                pygame.draw.rect(screen, bgColor, pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.maxHealth / 5, 5))
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.health / 5, 5))
                offset += barOffset

            if self.showBars['hunger']:
                pygame.draw.rect(screen, bgColor, pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.maxHunger / 5, 5))
                pygame.draw.rect(screen, (255, 217, 0), pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.hunger / 5, 5))
                offset += barOffset

            if self.showBars['repr']:
                pygame.draw.rect(screen, bgColor, pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.maxReproductiveUrge / 5, 5))
                pygame.draw.rect(screen, (229, 0, 255), pygame.Rect(self.pos.x - 5, self.pos.y - offset, self.reproductiveUrge / 5, 5))
                offset += barOffset

            if self.showBars['age']:
                ageColor = (255 * ((self.maxAge - self.age) / self.maxAge))

                if ageColor < 0: ageColor = 0
                if ageColor > 255: ageColor = 255

                pygame.draw.rect(screen, (ageColor, ageColor, ageColor), pygame.Rect(self.pos.x - 5, self.pos.y - offset, 20, 5))
                offset += barOffset