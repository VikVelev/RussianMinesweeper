import pygame
import numpy as np
import random

#game matrix 
columns = rows = 10
baseMatrix = np.empty((columns, rows), dtype=object) #filled with objects containing each rectangle
binaryMatrix = np.empty((columns, rows), dtype=object) #filled with 1s and 0s showing if a tile is clicked or clickable.
#future referrence for the non-binary, binaryMatrix: 
#0 means normal tile, 
#1 means clicked and empty
#2 means bombs near this one
#3 means a bomb

#position of the tiles and tiles dimensions (Square)
startPos = 10 #the starting position for X for each column
posX = posY = 10 #the 10 is irrelevant here, just to have them initialized
mineCount = (10*(random.randint(2,6))/100)*(columns*rows)
tileX = tileY = 40
distanceBetween = tileX + 3 #the number is the distance between each tile

#initializing
pygame.init()
screen = pygame.display.set_mode((rows*distanceBetween, columns*distanceBetween))
running = True
clock = pygame.time.Clock()

#RGBcolors of the tiles
tileColor = (8, 64, 128)
tileNearColor = (8, 64, 196)
clickedColor = (255, 255, 255)
bombColor = (196, 15, 15)

def initiateBinaryMatrix():
    for x in range(0, rows):
        for y in range (0, columns):
            binaryMatrix[x,y] = 0

def getBinaryMatrix():
    return binaryMatrix

def renderBase(): #it reads the binary matrix and renders it.
    for y in range(0, rows):
        posX = startPos
        for x in range(0, columns):
            posX = x*distanceBetween
            posY = y*distanceBetween
            
            baseMatrix[x,y] = pygame.Rect(posX, posY, tileX, tileY)
            
            if binaryMatrix[x,y] == 1:
                pygame.draw.rect(screen, clickedColor, baseMatrix[x,y])
            elif binaryMatrix[x,y] == 3:
                pygame.draw.rect(screen, bombColor, baseMatrix[x,y])
            else:
                pygame.draw.rect(screen, tileColor, baseMatrix[x,y])

def clickCollision(mousePos):
    clickedMatrixCoords = (None, None)
    temporaryMatrix = np.empty((columns, rows), dtype=object)

    for i in range(0, rows):
        for j in range (0, columns):
            if not binaryMatrix[i,j] == 1:
                temporaryMatrix[i,j] = baseMatrix[i,j].collidepoint(mousePos) #returns 1 or 0 depending on if its clicked
                if temporaryMatrix[i,j] == 1:
                    clickedMatrixCoords = (i,j);
                    binaryMatrix[i,j] = temporaryMatrix[i,j]
    return clickedMatrixCoords;

def generateMines():
    print(mineCount)
    mineCount_tmp = 0

    while mineCount_tmp < mineCount:
        mineX = random.randint(0, columns-1)
        mineY = random.randint(0, rows-1)

        if binaryMatrix[mineX,mineY] == 3:
            continue
        else:
            binaryMatrix[mineX, mineY] = 3
            mineCount_tmp += 1