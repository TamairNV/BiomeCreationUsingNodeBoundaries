
import math
from Grid import PygameGrid
import pygame
import random

class biomeGrid(PygameGrid):

    def __init__(self, grid_size, cell_size, screen_x, screen_y, name, line_thickness):
        super().__init__(grid_size, cell_size, screen_x, screen_y, name, line_thickness)
        self.grid = [["White" for _ in range(self.grid_y)] for _ in range(self.grid_x)]
        #parentNode.center_node = node((round(self.getGridX()/2*self.getCellSize()),round(self.getGridY()/2*self.getCellSize())),"Cyan")
        self.parent_nodes = []
        self.colour_dict = {"White" : (255,255,255),
           "Red" : (255,0,0),
           "Blue" : (0,0,255),
                            "Green" : (0,255,0),
                            "Cyan" : (255,0,0),
                            "Black" : (0,0,0)}

        self.spawn_parent_nodes()
        self.wall_nodes = []
        self.make_wall_nodes()
        self.lines_to_draw = []
    def paintCell(self,grid_pos):
        rect = pygame.Rect(grid_pos[0]* self.getCellSize(),grid_pos[1]* self.getCellSize(),self.getCellSize(),self.getCellSize())
        colour = self.colour_dict[self.grid[grid_pos[0]][grid_pos[1]]]
        pygame.draw.rect(self.getScreen().screen,colour,rect)

    def spawn_parent_nodes(self):
        colours = ["Green","Red","Blue","Cyan","Black","Blue","Green","Red","Blue"]
        for i in range(3):
            random_x = random.randint(0,self.getGridX()*self.getCellSize())
            random_y = random.randint(0, self.getGridY() * self.getCellSize())
            parent_node = parentNode((random_x,random_y),colours[i],0.7,self)
            parentNode.parent_nodes.append(parent_node)

    def paint_grid(self):
        for y in range(self.getGridY()):
            for x in range(self.getGridX()):
                self.paintCell((x, y))


        for colour, start_pos, end_pos in self.lines_to_draw:
            pygame.draw.line(self.getScreen().screen, colour, start_pos, end_pos,3)

    def make_wall_nodes(self):
        for pos in self.get_wall_positions():
            wall = node(pos,"Cyan",self)
            self.wall_nodes.append(wall)

    def get_wall_positions(self):
        wall_positions = []
        cell_size = self.getCellSize()
        grid_width = self.getGridX()
        grid_height = self.getGridY()

        # Top and bottom walls
        for x in range(grid_width):
            wall_positions.append((x * cell_size, 0))
            wall_positions.append((x * cell_size, (grid_height - 1) * cell_size))

        # Left and right walls
        for y in range(grid_height):
            wall_positions.append((0, y * cell_size))
            wall_positions.append(((grid_width - 1) * cell_size, y * cell_size))

        return wall_positions




    def paint_nodes(self):
        for n in node.nodes:
            n.paint_node()
        for n in parentNode.parent_nodes:
            n.paint_node()



class node():
    nodes = []
    def __init__(self,pos,colour,grid):
        self.x = pos[0]
        self.y = pos[1]
        self.colour = colour
        node.nodes.append(self)
        self.grid = grid

    def paint_node(self):
        rect = pygame.Rect(self.x,self.y,self.grid.getCellSize(),self.grid.getCellSize())
        pygame.draw.rect(self.grid.getScreen().screen,self.colour,rect)





class parentNode(node):
    parent_nodes = []
    center_force = -0.02
    center_node = None
    def __init__(self, pos, colour,force,cellSize):
        super().__init__(pos, colour,cellSize)
        parentNode.parent_nodes.append(self)
        self.__force = force

    def get_force(self):
        return self.__force

    def get_direction(self, point2):

        dx = point2.x - self.x
        dy = point2.y - self.y

        magnitude = math.sqrt(dx ** 2 + dy ** 2)


        if magnitude == 0:
            return 0, 0
        direction = (dx / magnitude, dy / magnitude)

        return direction

    def get_reaction_force(self, node2, force,is_center = False):
        force_direction = self.get_direction(node2)
        distance = math.sqrt((node2.x - self.x) ** 2 + (node2.y - self.y) ** 2)

        # Apply a decay factor to the force based on the distance
        if distance != 0:
            decayed_force = -force
        else:
            decayed_force = -force

        x_force = force_direction[0] * decayed_force
        y_force = force_direction[1] * decayed_force
        return x_force,y_force

    def spread(self):
        total_force = [0,0]
        for node_ in parentNode.parent_nodes:
            if node_ != self:
                force = self.get_reaction_force(node_,self.get_force())
                total_force[0] += force[0]
                total_force[1] += force[1]
        self.x += total_force[0]
        self.y += total_force[1]

        total_force = [0, 0]
        for node_ in node.nodes:
            force = self.get_reaction_force(node_,parentNode.center_force)
            total_force[0] += force[0]
            total_force[1] += force[1]

        self.x += total_force[0]
        self.y += total_force[1]


    def expand_parent_nodes(self):
        distances = [200,160,130]
        direction_vectors = []
        for i in range(3):
            dir_vector = (random.uniform(-1, 1),random.uniform(-1, 1))
            direction_vectors.append(dir_vector)

        for i in range(3):
            x_pos = self.x + direction_vectors[i][0] * distances[i]
            y_pos = self.y + direction_vectors[i][1] * distances[i]
            parentNode((x_pos,y_pos),self.colour,0.13,self.grid)

            self.grid.lines_to_draw.append((self.colour, (x_pos, y_pos), (self.x, self.y)))


    @staticmethod
    def expand_all_node(iter_amount):
        for i in range(iter_amount):
            for node_ in parentNode.parent_nodes:
                node_.spread()
        length = len(parentNode.parent_nodes)
        for i in range(length):
            parentNode.parent_nodes[i].expand_parent_nodes()



    @staticmethod
    def normal_node_pos(grid):
        node_size = grid.getCellSize()
        for node_ in node.nodes:
            new_x = (node_.x//node_size) * node_size
            new_y = (node_.y//node_size) * node_size
            node_.x = new_x
            node_.y = new_y






