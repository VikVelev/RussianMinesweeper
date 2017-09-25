import pygame
import numpy as np
import engine as en
#Main contains only main loop and event listeners, 
#engine contains functions and variables needed for those functions

en.initiateBinaryMatrix()
en.generateMines()
en.renderBase(False)

pygame.display.update();

#public static void Main()
while en.running:
    #---------------------------------
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            coords = en.clickCollision(mousePos)

            x = coords[0]
            y = coords[1]           
            
            en.renderBase(False)                                
            
            print(en.baseMatrix[x,y])

            en.renderBase(en.searchForMines(x,y))

        if event.type == pygame.QUIT:
            en.running = False

    pygame.display.flip()
    en.clock.tick(60)