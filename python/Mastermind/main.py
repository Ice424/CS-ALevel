import pygame
import random

# pygame setup
pygame.init()
WIDTH, HEIGHT = 480, 854

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
GAME_FONT = pygame.font.SysFont(None, 24)



COLOURS = ["red", "green", "blue", "yellow", "orange", "purple"]

PADDING = 20
ROWS = 12
COLUMNS = 5

BOARD_WIDTH, BOARD_HEIGHT = WIDTH-(WIDTH/ COLUMNS), HEIGHT

answer = []
for i in range(COLUMNS):
    answer.append(random.randint(0, len(COLOURS)-1))
print(answer)
guesses = 0

class ball():
    def __init__(self, colour, x, y):
        self.colour = 0
        self.x = x + 1
        self.y = y + 1
        self.state = "hidden"

    def draw(self):
        actual_x = (BOARD_WIDTH / COLUMNS) * self.y - 0.5 * (BOARD_WIDTH / COLUMNS)
        actual_y = (BOARD_HEIGHT / ROWS) * self.x - 0.5 * (BOARD_HEIGHT / ROWS)

        if self.state == "revealed":
            pygame.draw.circle(SCREEN, COLOURS[self.colour], (actual_x, actual_y), 20)
            #pygame.draw.circle(SCREEN, "white", (actual_x, actual_y), 20, width=4)
        elif self.state == "guess":
            pygame.draw.circle(SCREEN, COLOURS[self.colour], (actual_x, actual_y), 20, width=4)
        else:
            pygame.draw.circle(SCREEN, "white", (actual_x, actual_y), 20, width=4)

class selector():
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def draw(self):
        actual_x = (BOARD_WIDTH / COLUMNS) * (self.y+1) - 0.5 * (BOARD_WIDTH / COLUMNS)
        actual_y = (BOARD_HEIGHT / ROWS) * (self.x+1) - 0.5 * (BOARD_HEIGHT / ROWS)

        pygame.draw.line(
            SCREEN,
            "white",
            (actual_x - 30, actual_y + 30),
            (actual_x + 30, actual_y + 30),
            width=5
        )

class pin():
    def __init__(self,x,correct=0,misplaced=0):
        self.x = x
        self.correct = correct
        self.misplaced = misplaced

    def draw(self):
        actual_x = (BOARD_WIDTH / COLUMNS) * (COLUMNS+1) - 0.5 * (BOARD_WIDTH / COLUMNS)
        actual_y = (BOARD_HEIGHT / ROWS) * (self.x+1) - 0.5 * (BOARD_HEIGHT / ROWS)
        
        

        SCREEN.blit(GAME_FONT.render(f"{self.correct} Correct", True, "white"), (actual_x - 50, actual_y - 20))
        SCREEN.blit(GAME_FONT.render(f"{self.misplaced} Misplaced", True, "white"), (actual_x - 50, actual_y))

def submit_guess(row):
    guess = []
    global running
    global guesses
    guesses += 1
    complete = True
    for i in range(COLUMNS):
        if board[row][i].state != "guess":
            complete = False
            return
    if complete:
        for i in range(COLUMNS):
            guess.append(board[row][i].colour)
            board[row][i].state = "revealed"
    answer_copy = answer.copy()
    guess_copy = guess.copy()

    correct = 0
    misplaced = 0

    # First pass: correct position + colour
    for i in range(COLUMNS - 1, -1, -1):
        if guess_copy[i] == answer_copy[i]:
            correct += 1
            del guess_copy[i]
            del answer_copy[i]

    # Second pass: correct colour, wrong position
    for colour in guess_copy:
        if colour in answer_copy:
            misplaced += 1
            answer_copy.remove(colour)

    pins.append(pin(row, correct, misplaced))
    print(guess)
    cursor.x += 1
    cursor.y = 0
    
    if correct == COLUMNS:
        for i in range(COLUMNS):
            for j in range(ROWS):
                board[j][i].colour = answer[i]
                board[j][i].state = "revealed"
                board[j][i].draw()
                pins[-1].draw()
        pygame.display.flip()
        pygame.time.delay(5000)

        running = False
    if guesses == ROWS:
        pygame.time.delay(5000)
        for i in range(COLUMNS):
            for j in range(ROWS):
                board[j][i].colour = answer[i]
                board[j][i].state = "revealed"
                board[j][i].draw()
                pins[-1].draw()
        pygame.display.flip()
        pygame.time.delay(5000)
        
        running = False


        

board = []
pins = []
cursor = selector(0, 0)
count = 0

for i in range(ROWS):
    board.append([])
    for j in range(COLUMNS):
        board[i].append(ball("black", i, j))
        count += 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if cursor.y < COLUMNS-1:
                    cursor.y += 1
            if event.key == pygame.K_LEFT:
                if cursor.y > 0:
                    cursor.y -= 1
            if event.key == pygame.K_DOWN:
                if board[cursor.x][cursor.y].state != "guess":
                    board[cursor.x][cursor.y].state = "guess"
                else:
                    board[cursor.x][cursor.y].colour -= 1
                    board[cursor.x][cursor.y].colour %= len(COLOURS)
            if event.key == pygame.K_UP:
                if board[cursor.x][cursor.y].state != "guess":
                    board[cursor.x][cursor.y].state = "guess"
                else:
                    board[cursor.x][cursor.y].colour += 1
                    board[cursor.x][cursor.y].colour %= len(COLOURS)

            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                submit_guess(cursor.x)
                    
                
    SCREEN.fill("black")

    #board[cursor.x][cursor.y].state = "guess"
    
    for row in board:
        for ball in row:
            ball.draw()
    for current_pin in pins:
        current_pin.draw()
    cursor.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
