# Example file showing a basic pygame "game loop"
import pygame
import random

# pygame setup
WIDTH, HIGHT = 1000, 1000
pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
clock = pygame.time.Clock()
running = True
seed = "hello"
random.seed(seed)

maze = []
print(random.random())

for i in range(100):
    maze.append([])
    for j in range(100):
        maze[i].append("#")

print(maze)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    for 
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()