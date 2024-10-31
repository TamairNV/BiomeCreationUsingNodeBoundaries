
import pygame

from pygameInput import Input
import CustomDataStructures as dataS

pygame.init()


class Screen:

    def __init__(self, height, width, name):
        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.events = pygame.event.get()
        Input.startListening()
        self.position = dataS.Vector2(0, 0)
        self.frameRate = 1200

class Grid():
    def __init__(self,grid_size):
        self.grid_x = grid_size[0]
        self.grid_y = grid_size[1]
        self.grid = [["" for _ in range(self.grid_y)] for _ in range(self.grid_x)]

    def getGridX(self):
        return self.grid_x

    def getGridY(self):
        return self.grid_y
class PygameGrid(Grid):
    def __init__(self, grid_size,cell_size,screen_x,screen_y,name,line_thickness):
        super().__init__(grid_size)
        self.__screen = Screen(screen_y,screen_x,name)
        self.__cell_size = cell_size
        self.__screen_x = screen_x
        self.__screen_y = screen_y
        self.__line_thickness = line_thickness

        x_fit = self.grid_x*self.getCellSize() <= self.getScreenWidth()
        y_fit = self.grid_y*self.getCellSize() <= self.getScreenHeight()
        if not x_fit or not y_fit: raise ValueError("The grid doesnt fit in the screen")
        self.grid_rect_lines = []
    def getScreenHeight(self):
        return self.__screen_y

    def getLineThickness(self):
        return self.__line_thickness

    def getColour(self,node_name):
        return self.__colour_dict[node_name]

    def getScreenWidth(self):
        return self.__screen_x

    def getScreen(self):
        return self.__screen
    def getCellSize(self):
        return self.__cell_size


    def createGridLines(self):
        for x_line in range(self.getGridX()+1):
            line = pygame.Rect(self.getCellSize() * x_line,0,self.getLineThickness(),self.getCellSize() * self.getGridY())
            self.grid_rect_lines.append(line)
        for y_line in range(self.getGridY()+1):
            line =  pygame.Rect(0,self.getCellSize() * y_line,self.getCellSize() * self.getGridX(),self.getLineThickness())
            self.grid_rect_lines.append(line)
    def drawGrid(self):
        for line in self.grid_rect_lines:
            pygame.draw.rect(self.getScreen().screen,(0,0,0),line)

    def paintCell(self,grid_pos,colour):
        rect = pygame.Rect(grid_pos[0]* self.getCellSize(),grid_pos[1]* self.getCellSize(),self.getCellSize(),self.getCellSize())
        pygame.draw.rect(self.getScreen().screen,colour,rect)



''' Example
colours = {"Person" : (0,0,255),
           "Wall" : (0,0,0),
           "Target" : (255,0,0)}
grid = PygameGrid((25,40),15,600,750,"test",2,colours)
grid.createGridLines()



running = True
screen = grid.getScreen().screen
while running:

    screen.fill((200, 150, 200))


    grid.getScreen().events = pygame.event.get()

    for event in grid.getScreen().events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    grid.paintCell((2,3),(255,0,0))

    grid.drawGrid()
    pygame.display.flip()


'''

