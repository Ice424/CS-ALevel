import pygame
import random

# pygame setup
pygame.init()
WIDTH, HEIGHT = 480, 854
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

colours = ["red", "white", "green", "blue", "yellow", "purple"]

PADDING = 20
ROWS = 12
COLUMNS = 5

class ball():
    def __init__(self,colour,x,y):
        self.colour = colour
        self.x = x+1
        self.y = y+1
        self.state = "guess"
    def draw(self):
        actual_y = ((WIDTH)/COLUMNS) * self.y-0.5*(WIDTH)/COLUMNS
        actual_x = ((HEIGHT)/ROWS) * self.x-0.5*(HEIGHT)/ROWS
        if self.state == "revealed":
            pygame.draw.circle(SCREEN, self.colour, (actual_y,actual_x), 20)
            pygame.draw.circle(SCREEN, "white", (actual_y,actual_x), 20, width=4)
        elif self.state == "guess":
            pygame.draw.circle(SCREEN, self.colour, (actual_y,actual_x), 20, width=4)
        else:
            pygame.draw.circle(SCREEN, "white", (actual_y,actual_x), 20, width=4)

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

board = []

count = 0
for i in range(ROWS):
    board.append([])
    for j in range(COLUMNS):
        board[i].append(ball(random.choice(colours), i,j))
        count += 1
#print (board)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill("black")

    # RENDER YOUR GAME HERE
    for row in board:
        for ball in row:
            ball.draw()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()