import pygame
import math
import random
from globals import *
from vector2 import Vector2
from util import clamp

class Creature:
        def __init__(self, pos, health, hunger, reproduction, traits):
                self.pos = pos * tileSize

                self.health = health
                self.hunger = hunger
                self.reproduction = reproduction
                self.traits = {
                        "sight": traits['sight'],
                        "speed": traits['speed'],
                        "reprRate": self.reproduction['rate']
                }

                self.dir = Vector2(0, 1)
                self.curFood = None
                self.hungryLimit = self.hunger['max'] * 0.8

                self.moveTicks = 0
                self.requiredMoveTicks = 30
                self.showBars = True


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


        def TargetFood(self, food):
                if food == None:
                        self.curFood = None
                        return

                directionAbs = abs(food.pos - self.pos)
                distance = math.sqrt(directionAbs.x**2 + directionAbs.y**2)

                # targets the food if it is:
                # - in sight (distance > sight)
                # - the creature is hungry (hunger < hungry limit)
                if ((distance < self.traits['sight'] * tileSize) and
                    self.hunger['amount'] < self.hungryLimit):
                        self.curFood = food
                        return True

                return False

        def EatFood(self):
                self.health['amount'] += self.curFood.heal
                self.hunger['amount'] += self.curFood.hunger
                GameMan.RemoveFood(self.curFood)
                self.curFood = None
                        
        def MoveToFood(self, food):
                if food not in GameMan.food:
                        self.TargetFood(None)
                        return

                # move left
                if (self.pos.x > food.pos.x):
                        if self.dir != Vector2(-1, 0):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move right
                elif (self.pos.x < food.pos.x):
                        if self.dir != Vector2(1, 0):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move up
                elif (self.pos.y > food.pos.y):
                        if self.dir != Vector2(0, -1):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                # move down
                elif (self.pos.y < food.pos.y):
                        if self.dir != Vector2(0, 1):
                                self.Rotate(1)
                        else:
                                self.Move(1)

                else:
                        self.EatFood()


        def MoveRandomly(self):
                n = random.randint(0, 4)
                rotateAmount = random.choice([-1, 1])

                if n == 1:
                        self.Rotate(rotateAmount)
                else:
                        self.Move(1)


        def Die(self):
                GameMan.RemoveCreature(self)

        def OnTimerUpdate(self, tick):
                if ticks % tick != 0:
                        return

                if self.hunger['amount'] <= 0:
                        self.health['amount'] -= self.hunger['loss'] * 3


        def Update(self):
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


                self.moveTicks += self.traits['speed']

                if self.moveTicks > self.requiredMoveTicks:
                        if self.curFood != None:
                                self.MoveToFood(self.curFood)
                        else:
                                self.MoveRandomly()

                        self.moveTicks = 0

                self.pos.x = clamp(self.pos.x, 0, screenSize.x - tileSize)
                self.pos.y = clamp(self.pos.y, 0, screenSize.y - tileSize)


        def Draw(self):
                pygame.draw.rect(
                        screen, colors['male'], 
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

                if self.showBars:
                        pygame.draw.rect(
                                screen, (0, 255, 0), 
                                ()
                        )