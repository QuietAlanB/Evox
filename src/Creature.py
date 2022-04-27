import pygame
from globals import *
from vector2 import Vector2

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

                self.moveTicks = 0
                self.requiredMoveTicks = 30


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
                self.curFood = food

        def EatFood(self):
                self.health['amount'] += self.curFood.heal
                self.hunger['amount'] += self.curFood.hunger
                self.curFood.Eat()
                self.curFood = None
                        
        def MoveToFood(self, food):
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


        def Update(self):
                self.moveTicks += self.traits['speed']

                if self.moveTicks > self.requiredMoveTicks:
                        if self.curFood != None:
                                self.MoveToFood(self.curFood)
                        else:
                                self.Move(1)

                        self.moveTicks = 0


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