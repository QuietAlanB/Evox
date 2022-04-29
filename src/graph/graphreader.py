import pygame

file = open("src/graph/graphData.txt", "r", -1, "utf-8")

lines = file.readlines()
data = []

for line in lines:
        line = line.split(" ")

        data.append([int(line[0]), int(line[1])])

screenSize = (900, 900)
running = True
screen = pygame.display.set_mode(screenSize)
zeroHeight = 500
scaleAmount = 5

for i in range(1, len(data)):
        pointOne = (data[i - 1][0], zeroHeight - data[i - 1][1] * scaleAmount)
        pointTwo = (data[i][0], zeroHeight - data[i][1] * scaleAmount)

        pygame.draw.line(screen, (255, 255, 255), pointOne, pointTwo)

pygame.draw.line(screen, (255, 0, 0), (0, zeroHeight), (screenSize[0], zeroHeight))

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        pygame.display.update()
