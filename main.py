import pygame
import numpy as np
import engine as en

#Main contains only main loop and event listeners, 
#engine contains functions and variables needed for those functions
gameover = False

en.initiateMatrices()
en.generateMines()
en.renderBase(False)


pygame.display.update();

#public static void Main()
while en.running:
    #---------------------------------
    for event in pygame.event.get():
        if not gameover:
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                coords = en.clickCollision(mousePos)

                x = coords[0]
                y = coords[1]           
                                
                print(en.baseMatrix[x,y])

                en.expandTile(x,y)
                en.renderBase(False)
                
                print(en.coatMatrix)
                                                            
                if en.searchForMines(x,y):
                    en.renderBase(True)
                    gameover = True
                    print("Game Over")

                text = en.basicFont.render(str(en.countMines(x,y)), True , (255,0,0))
                en.screen.blit(text,text.get_rect())
                           
        if event.type == pygame.QUIT:
            en.running = False

    pygame.display.flip()
    en.clock.tick(60)