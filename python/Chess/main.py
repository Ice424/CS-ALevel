import pygame

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
GREEN = "#8fc294"
CREAM = "#fcfcf7"

class Piece():
    """
    Docstring for Piece
    
    """
    def __init__(self, side):
        self.side = side


def draw_board():
    borad_corner = (WIDTH/2)-(HEIGHT/2)
    square_length = HEIGHT / 8
    colour = [GREEN, CREAM]
    colour_index = 0
    
    pygame.draw.rect(screen, "purple", (borad_corner, 0, HEIGHT, HEIGHT))
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, colour[colour_index], (borad_corner + (square_length*i), (square_length*j), square_length,square_length))
            colour_index = 1 - colour_index
        colour_index = 1 - colour_index

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray20")

    # RENDER YOUR GAME HERE
    draw_board()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()