

import pygame







from BiomeCreation import *

def main():


    grid = biomeGrid((70,70),10,700,750,"test",2)
    grid.createGridLines()


    running = True
    screen = grid.getScreen().screen
    parentNode.expand_all_node(75) 
    parentNode.expand_all_node(25)
    parentNode.expand_all_node(75)
    parentNode.normal_node_pos(grid)
    while running:

        screen.fill((200, 150, 200))


        grid.getScreen().events = pygame.event.get()

        for event in grid.getScreen().events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


        grid.paint_grid()
        grid.paint_nodes()


        grid.drawGrid()
        pygame.display.flip()

if __name__ == "__main__":
    main()