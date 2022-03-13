import pygame
from screen import *
from pygame import gfxdraw
import math

def rotatePoint(point, center, angle):
    s = math.sin(angle)
    c = math.cos(angle)

    # ===== front point =====
    point -= center

    xNew = point.x * c - point.y * s
    yNew = point.x * s + point.y * c

    point = Vector2(xNew, yNew) + center
    return point



class Creature:
    def __init__(self, pos, size, angle, color, dir):
        self.pos = pos
        self.initialPos = pos
        self.color = color
        self.size = size
        self.dir = dir
        self.angle = angle
        self.rotation = self.angle * (math.pi / 180)
        self.center = self.pos

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



    # ======= draw update =======
    def drawUpdate(self):
        self.center = self.pos

        points = [ (self.front.x, self.front.y),
                   (self.top.x, self.top.y),
                   (self.bottom.x, self.bottom.y) ]

        gfxdraw.aapolygon(screen, points, self.color)
        gfxdraw.filled_polygon(screen, points, self.color)