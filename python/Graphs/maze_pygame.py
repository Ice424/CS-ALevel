import pygame
import time
import sys
from collections import deque

"""#################
#C - -#F - - -#4#
##### ####### # #
#- -#- - - -#- -#
# # ### ####### #
#-#3#- -#- - -#-#
# ### ### ### # #
#- - - - -#D#-#-#
### ### # # # # #
#-#- -#-#-#-#-#-#
# ### ### # # # #
#B#- - -#- -#- -#
# # # # #########
#-#2#-#- -#- - -#
# ### # # # ### #
#- - -#A#S -#1 -#
#################"""

grid = """#################
#- - -#A#S -#1 -#
# ### # # # ### #
#-#2#-#- -#- - -#
# # # # #########
#-#- - -#- -#- -#
# ### ### # # # #
#B#- -#-#-#-#-#-#
### ### # # # # #
#- - - - -#D#-#-#
# ### ### ### # #
#-#3#- -#- - -#-#
# # ### ####### #
#- -#- - - -#- -#
##### ####### # #
#C - -#F - - -#4#
#################"""



grid = grid.split("\n")

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300,700))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(pygame.font.get_default_font(), 12)

# setup lists
walls = []
path = []
visited = set()
frontier = deque()
solution = {}   
start_x, start_y = 0,0

# this is the class for the Maze
class Wall(pygame.Surface):               # define a Maze class
    def __init__(self)-> None:
        super().__init__((24,24))
        self.fill("white")

# this is the class for the finish line - green square in the maze
class Green(pygame.Surface):
    def __init__(self)-> None:
            super().__init__((24,24))
            self.fill("green")

class Blue(pygame.Surface):
    def __init__(self)-> None:
            super().__init__((24,24))
            self.fill("blue")
        
# this is the class for the yellow or turtle
class Red(pygame.Surface):
    def __init__(self)-> None:
            super().__init__((24,24))
            self.fill("red")

class Yellow(pygame.Surface):
    def __init__(self)-> None:
            super().__init__((24,24))
            self.fill("yellow")
        
        
class Letter(pygame.Surface):
   def __init__(self, letter)-> None:
           super().__init__((24,24))
           self.fill("pink")
           self.blit(font.render(letter, True, "black"), (6,6))
           
# set up classes
wall = Wall()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()
letter = Letter("a")

def setup_maze(grid, screen:pygame.Surface):                          # define a function called setup_maze
    global start_x, start_y, end_x, end_y      # set up global variables for start and end locations
    for y in range(len(grid)):                 # read in the grid line by line
        for x in range(len(grid[y])):          # read each cell in the line
            character = grid[y][x]             # assign the varaible "character" the the x and y location od the grid
            screen_x = 0 + (x * 24)         # move to the x location on the screen staring at -588
            screen_y = 500 - (y * 24)          # move to the y location of the screen starting at 288

            match character:
                case "#":
                    screen.blit(wall, (screen_x,screen_y)) 
                    walls.append((screen_x, screen_y))    # add coordinate to walls list
                case "F":
                    screen.blit(green, (screen_x,screen_y))
                    end_x, end_y = screen_x,screen_y     # assign end locations variables to end_x and end_y
                    path.append((screen_x, screen_y))
                case "S":
                    start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                    screen.blit(red, (screen_x,screen_y))
                case "1"|"2"|"3"|"4"|"A"|"B"|"C"|"D":
                    screen.blit(Letter(character), (screen_x,screen_y))
                    path.append((screen_x, screen_y))
                case _:
    
                    path.append((screen_x, screen_y)) 

screen.fill("black")
setup_maze(grid, screen)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    x,y = (start_x,start_y)
    frontier.append((x, y))
    solution[x,y] = x,y
    
    if len(frontier) > 0: 
            screen.blit(yellow, (x,y))
            while (x, y) != (start_x, start_y):    # stop loop when current cells == start cell
                screen.blit(yellow, solution[x, y])
                x, y = solution[x, y]    
    
    
    
    x, y = frontier.popleft()     # pop next entry in the frontier queue an assign to x and y location
    if(x - 24, y) in path and (x - 24, y) not in visited:  # check the cell on the left
        cell = (x - 24, y)
        solution[cell] = x, y    # backtracking routine [cell] is the previous cell. x, y is the current cell
        screen.blit(blue, (cell))
        frontier.append(cell)   # add cell to frontier list
        visited.add((x-24, y))  # add cell to visited list
    if (x, y - 24) in path and (x, y - 24) not in visited:  # check the cell down
        cell = (x, y - 24)
        solution[cell] = x, y
        screen.blit(blue, (cell))
        frontier.append(cell)
        visited.add((x, y - 24))
        print(solution)
    if(x + 24, y) in path and (x + 24, y) not in visited:   # check the cell on the  right
        cell = (x + 24, y)
        solution[cell] = x, y
        screen.blit(blue, (cell))
        frontier.append(cell)
        visited.add((x +24, y))
    if(x, y + 24) in path and (x, y + 24) not in visited:  # check the cell up
        cell = (x, y + 24)
        solution[cell] = x, y
        screen.blit(blue, (cell))
        frontier.append(cell)
        visited.add((x, y + 24))
    screen.blit(green, (x,y))
    pygame.display.flip()
    
    
    
    clock.tick(240) # limits FPS to 60

pygame.quit()











    

