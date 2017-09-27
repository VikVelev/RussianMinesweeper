import pygame
import numpy as np
import random
from pygame.locals import *

#game matrix 
columns = rows = 20
baseMatrix = np.empty((columns, rows), dtype=object) #filled with objects containing each rectangle
binaryMatrix = np.empty((columns, rows), dtype=object) #filled with 1s and 0s showing if a tile is clicked or clickable.
coatMatrix = np.empty((columns, rows), dtype=object) #filled with how many mines are actually nearby and should be the heighest layer
textMatrix = np.empty((columns,rows), dtype=object) #filled with representations of the coatMatrix in text
flagMatrix = np.empty((columns, rows), dtype=object) #filled with flagged shit

#textMatrix
#____________
#coatMatrix
#____________
#baseMatrix
#____________
#binaryMatrix

#future referrence for the non-binary, binaryMatrix: 
#-1 means starting point
#0 means non-clicked tile, 
#1 means clicked
#2 means traversed
#3 means a bomb

#position of the tiles and tiles dimensions (Square)
startPos = 10 #the starting position for X for each column
posX = posY = 10 #the 10 is irrelevant here, just to have them initialized
mineCount = ((random.randint(10,20))/100)*(columns*rows)
tileX = tileY = 50
distanceBetween = tileX #the number is the distance between each tile

#initializing
pygame.init()
screen = pygame.display.set_mode((rows*distanceBetween, columns*distanceBetween))

running = True
clock = pygame.time.Clock()

basicFont = pygame.font.SysFont(None,tileX);

#RGBcolors of the tiles
tileColor = (8, 64, 128)
tileNearColor = (255, 255, 255)
clickedColor = (255, 255, 255)
bombColor = (196, 15, 15)
textColor = (15, 196, 15)
flagColor = (255,255,100)

counter = basicFont.render("",True,(255,255,255))

def initiateMatrices():
    for x in range(0, rows):
        for y in range (0, columns):
            binaryMatrix[x,y] = 0
            coatMatrix[x,y] = 0
            flagMatrix[x,y] = 0

def getBinaryMatrix():
    return binaryMatrix

def renderBase(boolBombs): #it reads the binary matrix and renders it.
    for y in range(0, rows):
        posX = startPos
        for x in range(0, columns):
            posX = x*distanceBetween
            posY = y*distanceBetween
            
            baseMatrix[x,y] = pygame.Rect(posX, posY, tileX, tileY)
            
            if binaryMatrix[x,y] == 1:

                pygame.draw.rect(screen, clickedColor, baseMatrix[x,y])

                if flagMatrix[x,y] == 1:
                    pygame.draw.rect(screen, flagColor, baseMatrix[x,y])

            elif binaryMatrix[x,y] == 2: pygame.draw.rect(screen, tileNearColor, baseMatrix[x,y])
            elif binaryMatrix[x,y] == 3 and boolBombs: pygame.draw.rect(screen, bombColor, baseMatrix[x,y])        
            else:
                if flagMatrix[x,y] == 1:
                    pygame.draw.rect(screen, flagColor, baseMatrix[x,y])
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
    return clickedMatrixCoords;

def generateMines():
    mineCount_tmp = 0

    while mineCount_tmp < mineCount:
        mineX = random.randint(0, columns-1)
        mineY = random.randint(0, rows-1)

        if binaryMatrix[mineX,mineY] == 3 or binaryMatrix[mineX,mineY] == -1:
            continue
        else:
            binaryMatrix[mineX, mineY] = 3
            mineCount_tmp += 1
    for x in range(0,rows):
        for y in range(0,columns):
            countMines(x,y)

def isMine(tileX,tileY):
    if not tileX == None and not tileY == None:
        if binaryMatrix[tileX,tileY] == 3:
            return True

def countMines(tileX,tileY):
    mines = 0    
    if not tileX == None and not tileY == None:
        for i in range(-1,2):
            for j in range(-1,2):
                x = tileX + i
                y = tileY + j
                if x < rows and y < columns and x >= 0 and y >= 0:
                    if binaryMatrix[x,y] == 3:
                        mines += 1
        coatMatrix[tileX,tileY] = mines
        return mines

def expandTile(tileX,tileY,l_non0):
    layersOfNon0 = l_non0          
    for i in range(-1,2):
        for j in range(-1,2):
            x = tileX + i
            y = tileY + j
            if x < rows >= 0 and y < columns and x >= 0 and y >= 0:
                if not binaryMatrix[x,y] == 3 and not binaryMatrix[x,y] == 2: 
                    binaryMatrix[x,y] = 2
                    if not coatMatrix[x,y] == 0:
                        layersOfNon0 += 1
                    else:
                        expandTile(x,y,layersOfNon0)

def renderText(boolBombs):
    for x in range(0,rows):
        for y in range(0,columns):
            baseMatrix[x,y].center = (baseMatrix[x,y].x + 2 / 7  * tileX, baseMatrix[x,y].y + 2 / 9 * tileY)

            if not binaryMatrix[x,y] == 3 and not coatMatrix[x,y] == 0 and not flagMatrix[x,y] == 1:
                if binaryMatrix[x,y] == 2 or binaryMatrix[x,y] == 1:
                    textMatrix[x,y] = basicFont.render(str(countMines(x,y)), True, textColor)
                    screen.blit(textMatrix[x,y], baseMatrix[x,y].center)            

            elif binaryMatrix[x,y] == 3 and boolBombs:
                textMatrix[x,y] = basicFont.render("M", True, (0,0,0)) #M stands for Mine
                screen.blit(textMatrix[x,y], baseMatrix[x,y].center)

# def renderCounter(seconds):
#     global counter
#     counter.fill(tileColor)    
#     counter = basicFont.render(str(seconds),True,(255,255,255))  
#     screen.blit(counter,(0,0))

def anythingLeft():
    anything = False
    for x in range(0,rows):
        for y in range(0,columns):
            if binaryMatrix[x,y] == 0:
                anything = True
    return anything
