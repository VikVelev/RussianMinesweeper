import pygame
import numpy as np
import engine as en
#Main contains only main loop and event listeners, 
#engine contains functions and variables needed for those functions

en.initiateBinaryMatrix()
en.generateMines()
en.renderBase()

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

            if not x == None and not y == None:
                print(en.baseMatrix[x,y])
                #use the baseMatrix[x,y] for whatever here
            else:
                print("Already clicked once or not clickable.")
            
            en.renderBase()

        if event.type == pygame.QUIT:
            en.running = False

    pygame.display.flip()
    en.clock.tick(60)