import pygame
import numpy as np
import random

#game matrix 
columns = rows = 15
baseMatrix = np.empty((columns, rows), dtype=object) #filled with objects containing each rectangle
binaryMatrix = np.empty((columns, rows), dtype=object) #filled with 1s and 0s showing if a tile is clicked or clickable.
coatMatrix = np.empty((columns, rows), dtype=object) #filled with 1s and 0s showing if a tile is clicked or clickable.

#future referrence for the non-binary, binaryMatrix: 
#0 means normal tile, 
#1 means clicked and empty
#2 means bombs near this one
#3 means a bomb

#position of the tiles and tiles dimensions (Square)
startPos = 10 #the starting position for X for each column
posX = posY = 10 #the 10 is irrelevant here, just to have them initialized
mineCount = ((random.randint(5,20))/100)*(columns*rows)
tileX = tileY = 50
distanceBetween = tileX #the number is the distance between each tile

#initializing
pygame.init()
screen = pygame.display.set_mode((rows*distanceBetween, columns*distanceBetween))
running = True
clock = pygame.time.Clock()

#RGBcolors of the tiles
tileColor = (8, 64, 128)
tileNearColor = (255, 255, 255)
clickedColor = (255, 255, 255)
bombColor = (196, 15, 15)

def initiateBinaryMatrix():
    for x in range(0, rows):
        for y in range (0, columns):
            binaryMatrix[x,y] = 0

def getBinaryMatrix():
    return binaryMatrix

def renderBase(boolBombs): #it reads the binary matrix and renders it.
    for y in range(0, rows):
        posX = startPos
        for x in range(0, columns):
            posX = x*distanceBetween
            posY = y*distanceBetween
            
            baseMatrix[x,y] = pygame.Rect(posX, posY, tileX, tileY)

            if coatMatrix[x,y] == 1:
                pygame.draw.rect(screen, clickedColor, baseMatrix[x,y])
            elif binaryMatrix[x,y] == 2:
                pygame.draw.rect(screen, tileNearColor, baseMatrix[x,y])
            elif binaryMatrix[x,y] == 3 and boolBombs:
                pygame.draw.rect(screen, bombColor, baseMatrix[x,y])                
            else:
                pygame.draw.rect(screen, tileColor, baseMatrix[x,y])

def clickCollision(mousePos):
    clickedMatrixCoords = (None, None)
    temporaryMatrix = np.empty((columns, rows), dtype=object)

    for i in range(0, rows):
        for j in range (0, columns):
            temporaryMatrix[i,j] = baseMatrix[i,j].collidepoint(mousePos) #returns 1 or 0 depending on if its clicked
            if temporaryMatrix[i,j] == 1:
                clickedMatrixCoords = (i,j)                
                if not binaryMatrix[i,j] == 3 and not binaryMatrix[i,j] == 2:
                    binaryMatrix[i,j] = temporaryMatrix[i,j]
                    coatMatrix[i,j] = temporaryMatrix[i,j]
    return clickedMatrixCoords;

def generateMines():
    mineCount_tmp = 0

    while mineCount_tmp < mineCount:
        mineX = random.randint(0, columns-1)
        mineY = random.randint(0, rows-1)

        if binaryMatrix[mineX,mineY] == 3:
            continue
        else:
            binaryMatrix[mineX, mineY] = 3
            mineCount_tmp += 1

def searchForMines(tileX,tileY):
    if binaryMatrix[tileX,tileY] == 1: #actually should be 0 but check main why it isn't
        wayOut = True
        enoughMines = 5
        minesFound = 0
        while wayOut:
            print("Not implemented. Inf loop")
            wayOut = False            
            if minesFound == enoughMines:
                wayOut = False
            #think of an algorithm to expand and check for bombs here.
    if binaryMatrix[tileX,tileY] == 3:
        #the one you clicked is a mine
        return True
    if binaryMatrix[tileX,tileY] == 2:
        print("already clicked")

def countMines(tileX,tileY):
    mines = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if binaryMatrix[tileX+i,tileY+j] == 3:
                mines += 1
    print(mines)
    return mines

def expandTile(tileX,tileY):
    for i in range(-1,2):
        for j in range(-1,2):
            x = tileX + i
            y = tileY + j
            if x < rows and y < columns and x >= 0 and y >= 0:
                if not binaryMatrix[x,y] == 3 and not binaryMatrix[x,y] == 2:
                    binaryMatrix[x,y] = 2                
                    expandTile(x,y)
