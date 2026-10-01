import pygame
import time
import sys
from collections import deque

grid = """#################
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

grid = grid.split("\n")

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300,700))
clock = pygame.time.Clock()
running = True

# setup lists
walls = []
path = []
visited = set()
frontier = deque()
solution = {}   


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

            if character == "#":
                screen.blit(wall, (screen_x,screen_y)) 
                walls.append((screen_x, screen_y))    # add coordinate to walls list



            elif character == "F":
                screen.blit(green, (screen_x,screen_y))
                end_x, end_y = screen_x,screen_y     # assign end locations variables to end_x and end_y
                path.append((screen_x, screen_y))

            elif character == "S":
                start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                screen.blit(red, (screen_x,screen_y))
                
            else:
                path.append((screen_x, screen_y)) 

screen.fill("black")
setup_maze(grid, screen)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    
    
    
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()











def search(x,y):
    frontier.append((x, y))
    solution[x,y] = x,y

    while len(frontier) > 0:          # exit while loop when frontier queue equals zero
        #time.sleep(0.2)
        x, y = frontier.popleft()     # pop next entry in the frontier queue an assign to x and y location

        if(x - 24, y) in path and (x - 24, y) not in visited:  # check the cell on the left
            cell = (x - 24, y)
            solution[cell] = x, y    # backtracking routine [cell] is the previous cell. x, y is the current cell
            #blue.goto(cell)        # identify frontier cells
            #blue.stamp()
            frontier.append(cell)   # add cell to frontier list
            visited.add((x-24, y))  # add cell to visited list

        if (x, y - 24) in path and (x, y - 24) not in visited:  # check the cell down
            cell = (x, y - 24)
            solution[cell] = x, y
            letter.goto(cell)
            letter.stamp()
            frontier.append(cell)
            visited.add((x, y - 24))
            print(solution)

        if(x + 24, y) in path and (x + 24, y) not in visited:   # check the cell on the  right
            cell = (x + 24, y)
            solution[cell] = x, y
            letter.goto(cell)
            letter.stamp()
            frontier.append(cell)
            visited.add((x +24, y))

        if(x, y + 24) in path and (x, y + 24) not in visited:  # check the cell up
            cell = (x, y + 24)
            solution[cell] = x, y
            letter.goto(cell)
            letter.stamp()
            frontier.append(cell)
            visited.add((x, y + 24))
        green.goto(x,y)
        green.stamp()


def backRoute(x, y):
    yellow.goto(x, y)
    yellow.stamp()
    while (x, y) != (start_x, start_y):    # stop loop when current cells == start cell
        yellow.goto(solution[x, y])        # move the yellow sprite to the key value of solution ()
        yellow.stamp()
        x, y = solution[x, y]               # "key value" now becomes the new key



                        # solution dictionary


# main program starts here ####
setup_maze(grid)
search(start_x,start_y)
backRoute(end_x, end_y)
wn.exitonclick()
