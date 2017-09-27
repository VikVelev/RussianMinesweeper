import pygame
import numpy as np
import engine as en

#Main contains only main loop and event listeners, 
#engine contains functions and variables needed for those functions
gameover = False
startPoint = True
refreshRate = 100
timer = 60*refreshRate

en.initiateMatrices()
en.renderBase(False)

pygame.display.update();

#public static void Main()
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

                    if not x == None and not y == None:
                        if en.countMines(x,y) == 0:
                            en.expandTile(x,y,0)

                    if en.isMine(x,y): #if a mine is clicked, oh well.
                        en.renderBase(True)
                        en.renderText(True)
                        gameover = True
                        print("Game Over")
                    else:
                        en.flagMatrix[x,y] = 0
                        en.renderBase(False)
                        en.renderText(False)            
                                            
        if event.type == pygame.QUIT:
            en.running = False

    pygame.display.flip()
    en.clock.tick(refreshRate)
    timer -= 1
    print(timer/refreshRate)