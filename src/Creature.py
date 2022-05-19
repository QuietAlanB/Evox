import pygame
import math
import random
from globals import *
import globals
from vector2 import Vector2
from util import clamp

class Creature:
        def __init__(self, pos, gender, age, health, hunger, reproduction, traits):
                self.pos = pos * tileSize

                self.gender = gender

                if self.gender != "male" or "female":
                        self.gender = random.choice(["male", "female"])

                self.age = age
                self.health = health
                self.hunger = hunger
                self.reproduction = reproduction
                self.traits = {
                        "sight": traits['sight'],
                        "speed": traits['speed'],
                        "reprRate": self.reproduction['rate'],
                        "threatResponse": traits['threatResponse']
                }

                self.dir = Vector2(0, 1)
                self.curFood = None
                self.curMate = None
                self.hungryLimit = self.hunger['max'] * 0.8
                self.mateLimit = self.reproduction['max'] * 0.5

                self.moveTicks = 0
                self.requiredMoveTicks = 30
                self.showBars = {
                        "health": True,
                        "hunger": True,
                        "reproduction": True,
                        "age": True
                }


        def Move(self, amount):
                amount *= tileSize
                self.pos += self.dir * amount

        def Rotate(self, amount):
                if amount < 0: 
                        amount = -(abs(amount) % 4)
                else: 
                        amount %= 4
                
                if amount == 4 or amount == -4 or amount == 0: 
                        self.dir = self.dir
                elif amount == 2 or amount == -2: 
                        self.dir = Vector2(-self.dir.x, -self.dir.y)
                elif amount == 1 or amount == -3: 
                        self.dir = Vector2(self.dir.y, -self.dir.x)
                elif amount == -1 or amount == 3: 
                        self.dir = Vector2(-self.dir.y, self.dir.x)

        def MoveToPos(self, pos):
                # move left
                if (self.pos.x > pos.x):
                        if self.dir != Vector2(-1, 0):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move right
                elif (self.pos.x < pos.x):
                        if self.dir != Vector2(1, 0):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move up
                elif (self.pos.y > pos.y):
                        if self.dir != Vector2(0, -1):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move down
                elif (self.pos.y < pos.y):
                        if self.dir != Vector2(0, 1):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                else:
                        return False

                return True

        
        def InSight(self, pos):
                directionAbs = abs(pos - self.pos)
                distance = math.sqrt(directionAbs.x**2 + directionAbs.y**2)

                if distance < self.traits['sight'] * tileSize:
                        return True
                return False


        def TargetFood(self, food):
                if food == None:
                        self.curFood = None
                        return

                # targets the food if it is:
                # - in sight (distance > sight)
                # - the creature is hungry (hunger < hungry limit)
                if ( ( self.InSight(food.pos) ) and
                self.hunger['amount'] < self.hungryLimit):
                        self.curFood = food
                        return True

                return False

        def EatFood(self):
                self.health['amount'] += self.curFood.heal
                self.hunger['amount'] += self.curFood.hunger
                gameMan.RemoveFood(self.curFood)
                self.curFood = None
        
        def MoveToFood(self, food):
                if food not in gameMan.food:
                        self.TargetFood(None)
                        return

                movedToFood = self.MoveToPos(food.pos)

                if not movedToFood:
                        self.EatFood()


        def MoveRandomly(self):
                n = random.randint(0, 3)
                rotateAmount = random.choice([-1, 1])

                if n == 0:
                        self.Rotate(rotateAmount)
                else:
                        self.Move(1)


        def TargetMate(self, mate):
                # targets the mate if:
                # - not targetting food
                # - not in panic mode (still need to add)
                # - this creature's and mate's reproductive urge is high
                # - age is different
                # - the creature and the mate doesnt already have a mate
                # - mate is in sight
                if (self.curFood == None and
                self.InSight(mate.pos) and
                self.reproduction['amount'] > self.mateLimit and
                mate.reproduction['amount'] > mate.mateLimit and
                self.gender != mate.gender and
                self.curMate == None and
                mate.curMate == None):
                        self.curMate = mate
                        mate.curMate = self
                        return True
                return False

        def MoveToMate(self, mate):
                movedToMate = self.MoveToPos(mate.pos)

                if not movedToMate:
                        self.Mate()
                
        def Mate(self):
                for i in range(random.randint(0, 4)):
                        gender = random.choice(["male", "female"])
                        health = {
                                "amount":self.health['amount'],
                                "max":self.health['max'],
                                "regen": self.health['regen']
                        }
                        hunger = {
                                "amount":self.health['amount'],
                                "max":self.hunger['max'],
                                "loss": self.hunger['loss']
                        }
                        reproduction = {
                                "amount":0,
                                "max":self.reproduction['max'],
                                "rate": self.reproduction['rate']
                        }


                        traits = {
                                "speed":self.traits['speed'],
                                "sight":self.traits['sight']
                        }

                        n = random.randint(1, 5)
                        traitMutationAmount = random.choice(
                                [0.8, 0.9, 1.0, 1.1, 1.2]
                        )
                        selectedTrait = random.choice(
                                ["speed", "sight"]
                        )

                        if n == 1:
                                traits[selectedTrait] *= traitMutationAmount


                        c = Creature(self.pos / tileSize, gender,
                        {"amount":0, "max":self.age['max']},
                        health,
                        hunger,
                        reproduction,
                        traits
                        )

                        gameMan.AddCreature(c)

                self.curMate.reproduction['amount'] = 0
                self.reproduction['amount'] = 0

                self.curMate.curMate = None
                self.curMate = None


        def Die(self):
                gameMan.RemoveCreature(self)

        
        # THIS IS TO BE RUN EVERY SECOND, THOUGH IT IS CONFIGURABLE
        def OnTimerUpdate(self, tick):
                if globals.ticks % tick != 0:
                        return

                self.hunger['amount'] -= self.hunger['loss']
                self.reproduction['amount'] += self.reproduction['rate']
                self.age['amount'] += 1

                if self.hunger['amount'] <= 0:
                        self.health['amount'] -= self.hunger['loss'] * 3


        def Update(self):
                for food in gameMan.food:
                        foodTargetted = self.TargetFood(food)

                        if foodTargetted:
                                break


                for creature in gameMan.creatures:
                        mateFound = self.TargetMate(creature)

                        if mateFound:
                                break


                self.health['amount'] = clamp(
                        self.health['amount'],
                        0, self.health['max']
                        )
                self.hunger['amount'] = clamp(
                        self.hunger['amount'],
                        0, self.hunger['max']
                        )
                self.reproduction['amount'] = clamp(
                        self.reproduction['amount'],
                        0, self.reproduction['max']
                        )

                if self.health['amount'] <= 0:
                        self.Die()
                if self.age['amount'] > self.age['max']:
                        self.Die()


                self.moveTicks += self.traits['speed']

                if self.moveTicks > self.requiredMoveTicks:
                        if self.curFood != None:
                                self.MoveToFood(self.curFood)
                        elif self.curMate != None:
                                self.MoveToMate(self.curMate)
                        else:
                                self.MoveRandomly()

                        self.moveTicks = 0

                self.pos.x = clamp(self.pos.x, 0, screenSize.x - tileSize)
                self.pos.y = clamp(self.pos.y, 0, screenSize.y - tileSize)


        def Draw(self):
                pygame.draw.rect(
                        screen, colors[self.gender], 
                        (self.pos.x, self.pos.y, tileSize, tileSize)
                )

                width = tileSize / 4
                addedPosY = self.pos.y + tileSize - width
                addedPosX = self.pos.x + tileSize - width

                # facing upwards
                if self.dir == Vector2(0, -1):
                        pygame.draw.rect(
                                screen, (255, 255, 255),
                                (self.pos.x, self.pos.y, tileSize, width)
                        )

                # facing downwards
                if self.dir == Vector2(0, 1):
                        pygame.draw.rect(
                                screen, (255, 255, 255),
                                (self.pos.x, addedPosY, tileSize, width)
                        )

                # facing left
                if self.dir == Vector2(-1, 0):
                        pygame.draw.rect(
                                screen, (255, 255, 255),
                                (self.pos.x, self.pos.y, width, tileSize)
                        )

                # facing right
                if self.dir == Vector2(1, 0):
                        pygame.draw.rect(
                                screen, (255, 255, 255),
                                (addedPosX, self.pos.y , width, tileSize)
                        )

                yOffset = self.pos.y - width
                health = self.health['amount'] / 5
                hunger = self.hunger['amount'] / 5
                reproduction = self.reproduction['amount'] / 5  

                inverseAge = self.age['max'] - self.age['amount']
                ageColor = inverseAge * (255 / self.age['max'])

                if self.age['amount'] > self.age['max']:
                        ageColor = 0

                if self.showBars['health']:
                        pygame.draw.rect(
                                screen, (0, 255, 0), 
                                (self.pos.x, yOffset, health, width)
                        )

                        yOffset -= width

                if self.showBars['hunger']:
                        pygame.draw.rect(
                                screen, (255, 128, 0), 
                                (self.pos.x, yOffset, hunger, width)
                        )

                        yOffset -= width

                if self.showBars['reproduction']:
                        pygame.draw.rect(
                                screen, (255, 0, 200), 
                                (self.pos.x, yOffset, reproduction, width)
                        )

                        yOffset -= width

                if self.showBars['age']:
                        pygame.draw.rect(
                                screen, (ageColor, ageColor, ageColor), 
                                (self.pos.x, yOffset, tileSize, width)
                        )