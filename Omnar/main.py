# Example file showing a basic pygame "game loop"
import pygame
import math
import random

# pygame setup
pygame.init()
HEIGHT = 1080
WIDTH = 720
screen = pygame.display.set_mode((HEIGHT, HEIGHT))
clock = pygame.time.Clock()
running = True
r = 300

pads = []
n = 50
for i in range(400):
    step = 2*math.pi/400
    x = r * math.sin(step*i)
    y = r * math.cos(step*i)
    
    if n >= 0:
        pads.append([x,y,"green"])
    else:
        pads.append([x,y,"white"])
    n = n-1
        
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    
    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, "pink", (HEIGHT/2,HEIGHT/2), r)
    
    for pad in pads:
        pygame.draw.circle(screen, pad[2], (HEIGHT/2 + pad[0],HEIGHT/2+ pad[1]), 2)
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    random.choice([pad for pad in pads if pad[2] == "green"])

    clock.tick(60)  # limits FPS to 60

pygame.quit()