"""
Frog & Lily-pad puzzle simulation (Pygame)

Controls:
 - SPACE : perform one random legal move (step)
 - S : step one move (same as SPACE)
 - A : toggle autorun (continuous random moves)
 - R : reset to initial configuration
 - MOUSE : click a frog then click a valid target to perform that move (manual)
 - +/- : increase/decrease autorun speed
 - ESC or window close : quit

Notes:
 - Default uses M=1000 pads. For easier visual debugging change M to a smaller value (e.g. 60).
 - The positions are drawn around a circle; occupied pads are filled circles.
"""

import pygame, sys, math, random, time

# ---------- Configuration ----------
M = 1000 # total number of pads (set to 60 when testing visually)
initial_n = 300 # initial number of occupied pads (set <= M)
WIDTH, HEIGHT = 1200, 900
BG_COLOR = (245, 245, 245)
PAD_COLOR = (200, 200, 200)
OCC_COLOR = (30, 120, 200)
SELECT_COLOR = (200, 50, 50)
TEXT_COLOR = (20, 20, 20)
PAD_RADIUS = 3 # will be scaled for big/small M
RING_RADIUS = min(WIDTH, HEIGHT) * 0.38
FPS = 60
# -----------------------------------

# adjust radii for huge M so pads fit
if M <= 100:
    PAD_RADIUS = 6
elif M <= 500:
    PAD_RADIUS = 4
else:
    PAD_RADIUS = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog & Lily-pad puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

center = (WIDTH // 2, HEIGHT // 2 - 30)

def pad_position(i):
    """Compute x,y position for pad index i."""
    angle = (2 * math.pi * i) / M - math.pi/2 # start at top
    x = center[0] + RING_RADIUS * math.cos(angle)
    y = center[1] + RING_RADIUS * math.sin(angle)
    return int(x), int(y)

# Precompute positions for speed
POS = [pad_position(i) for i in range(M)]

# ---------- Game state ----------
def make_initial_state():
    # 1 for occupied, 0 for empty
    occ = [0] * M
    for i in range(initial_n):
        occ[i % M] = 1
    return occ

state = make_initial_state()
moves_done = 0
autorun = False
autorun_delay = 0.02 # seconds between auto moves
last_auto_time = 0

selected_pad = None # index selected by user (for manual move)

# ---------- Helpers for rules ----------
def mod(i):
    return i % M

def is_swim_move(occ, k, dest):
    # swim by 4
    return (mod(k + 4) == dest or mod(k - 4) == dest) and occ[dest] == 0

def is_jump_move(occ, k, dest):
    # jump by 3; both jumped-over pads must be occupied, dest empty
    # compute direction
    if mod(k + 3) == dest:
        mid1 = mod(k + 1)
        mid2 = mod(k + 2)
        return occ[dest] == 0 and occ[mid1] == 1 and occ[mid2] == 1
    if mod(k - 3) == dest:
        mid1 = mod(k - 1)
        mid2 = mod(k - 2)
        return occ[dest] == 0 and occ[mid1] == 1 and occ[mid2] == 1
    return False

def legal_moves(occ):
    """Return list of legal moves as tuples (k, dest, type) type 'swim' or 'jump'"""
    moves = []
    for k in range(M):
        if occ[k] == 1:
            # swim candidates:
            for d in (4, -4):
                dest = mod(k + d)
                if occ[dest] == 0:
                    moves.append((k, dest, 'swim'))
            # jump candidates:
            for d in (3, -3):
                dest = mod(k + d)
                # check two jumped-over pads are occupied
                if occ[dest] == 0:
                    # get jumped indices
                    if d > 0:
                        mid1, mid2 = mod(k+1), mod(k+2)
                    else:
                        mid1, mid2 = mod(k-1), mod(k-2)
                    if occ[mid1] == 1 and occ[mid2] == 1:
                        moves.append((k, dest, 'jump'))
    return moves

def apply_move(occ, move):
    """Apply a move in place. move = (k, dest, type). Return number of removed frogs (0 or 2)."""
    k, dest, typ = move
    occ[k] = 0
    occ[dest] = 1
    removed = 0
    if typ == 'jump':
        # remove the two jumped-over frogs
        if (dest - k) % M in (3,):
            mid1, mid2 = mod(k+1), mod(k+2)
        elif (k - dest) % M in (3,):
            mid1, mid2 = mod(k-1), mod(k-2)
        else:
            # due to wrap, compute by difference normalized to [-M/2, M/2]
            diff = (dest - k + M) % M
            if diff == 3:
                mid1, mid2 = mod(k+1), mod(k+2)
            elif diff == M-3:
                mid1, mid2 = mod(k-1), mod(k-2)
            else:
                # shouldn't happen
                mid1 = mid2 = None
        if mid1 is not None:
            if occ[mid1] == 1: occ[mid1] = 0; removed += 1
            if occ[mid2] == 1: occ[mid2] = 0; removed += 1
    return removed

# ---------- Drawing ----------
def draw(occ, highlight_move=None):
    screen.fill(BG_COLOR)
    # draw pads (only outline or small circle)
    # draw lines maybe connecting first few for clarity? skip for speed
    for i, pos in enumerate(POS):
        # small grey dot for pad background
        pygame.draw.circle(screen, PAD_COLOR, pos, PAD_RADIUS)
    # draw occupied pads
    for i, pos in enumerate(POS):
        if occ[i]:
            pygame.draw.circle(screen, OCC_COLOR, pos, PAD_RADIUS+1)
    # highlight selected pad
    if selected_pad is not None:
        pygame.draw.circle(screen, SELECT_COLOR, POS[selected_pad], PAD_RADIUS+3, 2)
    # highlight a potential move
    if highlight_move:
        k, dest, typ = highlight_move
        pygame.draw.circle(screen, (0,200,0), POS[dest], PAD_RADIUS+4, 2)
        pygame.draw.line(screen, (0,150,0), POS[k], POS[dest], 1)

    # info text
    frogs_left = sum(state)
    lines = [
        f"Pads M = {M} Initial occupied n = {initial_n}",
        f"Frogs remaining: {frogs_left}",
        f"Moves done: {moves_done}",
        f"Legal moves available: {len(legal_moves(state))}",
        "Controls: SPACE/S - step, A - toggle autorun, R - reset, +/- speed, Click frog then click dest to manually move"
    ]
    y = HEIGHT - 120
    for line in lines:
        surf = font.render(line, True, TEXT_COLOR)
        screen.blit(surf, (20, y))
        y += 22

    pygame.display.flip()

# ---------- Main loop ----------
def random_step():
    global moves_done
    moves = legal_moves(state)
    if not moves:
        return False
    mv = random.choice(moves)
    apply_move(state, mv)
    moves_done += 1
    return True

running = True
draw(state)
while running:
    now = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_s:
                random_step()
            elif event.key == pygame.K_r:
                state = make_initial_state()
                moves_done = 0
                selected_pad = None
            elif event.key == pygame.K_a:
                autorun = not autorun
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                autorun_delay = max(0.001, autorun_delay * 0.7)
            elif event.key == pygame.K_MINUS:
                autorun_delay = autorun_delay * 1.3
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # find nearest pad within some radius
            closest = None
            bestd = 9999
            for i, pos in enumerate(POS):
                d = (pos[0] - mx)**2 + (pos[1] - my)**2
                if d < bestd:
                    bestd = d; closest = i
            # threshold for clicking on pad:
            if bestd <= (20 if M < 300 else 12)**2:
                if selected_pad is None:
                    # only select an occupied pad
                    if state[closest] == 1:
                        selected_pad = closest
                else:
                    # attempt to move selected_pad -> closest if legal
                    k = selected_pad
                    dest = closest
                    if is_swim_move(state, k, dest):
                        apply_move(state, (k, dest, 'swim'))
                        moves_done += 1
                        selected_pad = None
                    elif is_jump_move(state, k, dest):
                        apply_move(state, (k, dest, 'jump'))
                        moves_done += 1
                        selected_pad = None
                    else:
                        # if clicked another occupied pad, switch selection
                        if state[closest] == 1:
                            selected_pad = closest
                        else:
                            # clear selection
                            selected_pad = None

    # autorun
    if autorun:
        if now - last_auto_time >= autorun_delay:
            cont = random_step()
            last_auto_time = now
            if not cont:
                autorun = False

    # draw current state
    draw(state)

    clock.tick(FPS)

pygame.quit()
sys.exit()