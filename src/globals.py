import pygame
from GameManager import GameManager
from vector2 import Vector2

screenSize = Vector2(900, 900)
screen = pygame.display.set_mode((screenSize.x, screenSize.y))
tileSize = 20
gameMan = GameManager()
ticks = 0
colors = {
        "male": (75, 75, 255),
        "female": (255, 25, 200)
}