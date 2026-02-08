import pygame
import os
from typing import Literal

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

GAME_FONT = pygame.font.SysFont(None, 24)
GREEN = "#8fc294"
CREAM = "#fcfcf7"


STARTING_BACK_RANK = ["R", "N", "B", "Q", "K", "B", "N", "R"]
FILES = "ABCDEFGH"


promotion_piece: Piece | None = None
promotion_side: str | None = None
promotion_square: str | None = None
promotion_options = ["Q", "R", "B", "N"]


def index_from_notation(square:str):
    file = FILES.index(square[0])
    rank = int(square[1]) - 1
    return file, rank

def notation_from_index(file:int, rank:int):
    if 0 <= file < 8 and 0 <= rank < 8:
        return f"{FILES[file]}{rank + 1}"
    return None


def ray_moves(piece, directions, board):
    file, rank = index_from_notation(piece.location)
    moves = []
    # follows a direction until it reaches the edge of the board while appending them to a list
    for df, dr in directions:
        f, r = file + df, rank + dr
        while 0 <= f < 8 and 0 <= r < 8:
            square = notation_from_index(f, r)
            if board.squares[square].piece:
                moves.append(square)
                break
            moves.append(square)
            f += df
            r += dr

    return [m for m in moves if m]



def rook_moves(piece:Piece, board:Board) -> list[str]:
    rook_dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    return ray_moves(piece, rook_dirs, board)

def bishop_moves(piece:Piece, board:Board) -> list[str]:
    bishop_dirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
    return ray_moves(piece, bishop_dirs, board)

def knight_moves(piece:Piece, board:Board) -> list[str]:
    knight_offsets = [
    (2,1),(1,2),(-1,2),(-2,1),
    (-2,-1),(-1,-2),(1,-2),(2,-1)]
    file, rank = index_from_notation(piece.location)
    moves = []
    for f,r in knight_offsets:
        notation = notation_from_index(f+file, r+rank)
        moves.append(notation)
    return [m for m in moves if m]

def king_moves(piece:Piece, board:Board) -> list[str]:
    king_offsets = [(1,1), (1,0), (1,-1),
                    (0,1),        (0,-1),
                    (-1,1), (-1,0), (-1,-1)]
    file, rank = index_from_notation(piece.location)
    moves = []
    for f,r in king_offsets:
        notation = notation_from_index(f+file, r+rank)
        moves.append(notation)
    
    
    rank += 1 # index at 0 to index at 1
    enemy = "B" if piece.side == "W" else "W"
    if not piece.moved:
        
        # kingside 
        rook_square = f"H{rank}"
        checks = ["F", "G"]
        blocked = False
        for check in checks:
            if board[f"{check}{rank}"].piece or board.is_square_attacked(f"{check}{rank}", enemy):
                blocked = True
        if board[rook_square].piece and not board[rook_square].piece.moved and not blocked:
            moves.append(f"G{rank}")

        # queenside 
        rook_square = f"A{rank}"
        checks = ["B", "C", "D"]
        blocked = False
        for check in checks:
            if board[f"{check}{rank}"].piece or board.is_square_attacked(f"{check}{rank}", enemy):
                blocked = True
        if board[rook_square].piece and not board[rook_square].piece.moved and not blocked:
            moves.append(f"C{rank}")

    
    return [m for m in moves if m]

def pawn_moves(piece: Piece, board: Board) -> list[str]:

    file, rank = index_from_notation(piece.location)

    direction = 1 if piece.side == "W" else -1

    moves = []

    # forward
    forward = notation_from_index(file, rank + direction)

    if forward and not board[forward].piece:

        moves.append(forward)

        if not piece.moved:

            forward2 = notation_from_index(file, rank + direction * 2)

            if forward2 and not board[forward2].piece:
                moves.append(forward2)

    # captures
    for df in (-1, 1):

        target_sq = notation_from_index(file + df, rank + direction)

        if target_sq:

            target = board[target_sq].piece

            if target and target.side != piece.side:
                moves.append(target_sq)

    return moves



MOVE_GENERATORS = {
    "R": rook_moves,
    "B": bishop_moves,
    "N": knight_moves,
    "Q": lambda p, b: rook_moves(p, b) + bishop_moves(p, b),
    "K": king_moves,
    "P": pawn_moves,
}

class Piece():
    """
    Docstring for Piece
    
    """
    def __init__(self, side:Literal["B", "W"], piece_type:Literal["K", "Q", "R", "B", "N", "P"], location:str):
        self.side = side
        self.type = piece_type
        self.notation = f"{self.side}{self.type}"
        self.passantable = False
        self.moved = False
        
        raw_surf = pygame.image.load(os.path.join("sprites", f"{self.notation}.png")).convert_alpha()
        piece_size = int(HEIGHT / 8 * 0.85)
        self.sprite_surf = pygame.transform.smoothscale(raw_surf, (piece_size, piece_size))
        
        
        
        self.location = location
    def __str__(self) -> str:
        return self.notation 
    def draw(self):
        square = B[self.location]
        rect = self.sprite_surf.get_rect(center=square.coordinate, )
        screen.blit(self.sprite_surf, rect)
        
    def moves(self):
        return MOVE_GENERATORS[self.type](self, B)


class Square:
    def __init__(self, file, rank, coordinate):
        self.file: str = file  
        self.rank: str = rank
        self.coordinate: tuple[int, int] = coordinate  
        self.piece: None | Piece = None 


class Board():
    def __init__(self) -> None:
        self.squares: dict[str, Square]= {}
        self.pieces: list[Piece] = []
        self.board_corner = (WIDTH/2)-(HEIGHT/2)
        self.square_length = HEIGHT / 8
        
        self.turn = "W"
        self.check: None | Literal["W", "B"] = None
    
        for file_index, file in enumerate(FILES):
            for rank in range(1, 9):
                x = self.board_corner + file_index * self.square_length + self.square_length / 2
                y = (8 - rank) * self.square_length + self.square_length / 2
                

                self.squares[f"{file}{rank}"] = Square(file, rank, (x, y))

        self.setup_starting_position()
    
    def __getitem__(self, key: str | tuple[int, int]) -> Square:
        if isinstance(key, tuple):
            file, rank = key
            tempkey = notation_from_index(file, rank)
            if tempkey is None:
                raise KeyError("Square out of bounds")
            key = tempkey
        return self.squares[key]
    
    def _add_piece(self, side, piece_type, location):
        piece = Piece(side, piece_type, location)
        self.pieces.append(piece)
        self.squares[location].piece = piece

    
    def setup_starting_position(self):
        for file in FILES:
            self._add_piece("W", "P", f"{file}2")
            self._add_piece("B", "P", f"{file}7")

        for i, piece_type in enumerate(STARTING_BACK_RANK):
            file = FILES[i]
            self._add_piece("W", piece_type, f"{file}1")
            self._add_piece("B", piece_type, f"{file}8")
    
    
    def draw(self):
        colour = [GREEN, CREAM]
        colour_index = 0
        for file_index, file in enumerate(FILES):
            for rank in range(0, 8):
                pygame.draw.rect(screen, colour[colour_index], (self.board_corner + (self.square_length*file_index), (self.square_length*rank), self.square_length,self.square_length))
                
                colour_index = 1 - colour_index
                screen.blit(GAME_FONT.render(f"{file}{8 - rank}", True, colour[colour_index]), ((self.board_corner  + (self.square_length*file_index)), (self.square_length*rank)), )
                
            colour_index = 1 - colour_index
        for piece in self.pieces:
            piece.draw()
    
    def moves(self, piece: Piece):
        
        moves = []
        captures = []

        for move in piece.moves():

            target = self[move].piece

            if not target:
                moves.append(move)

            elif target.side != piece.side:
                captures.append(move)

        legal = []

        for move in moves + captures:

            original_location = piece.location
            captured_piece = self[move].piece

            # simulate move
            self[original_location].piece = None
            self[move].piece = piece
            piece.location = move

            if captured_piece:
                self.pieces.remove(captured_piece)

            if not self.check_check(piece.side):
                legal.append(move)

            # restore
            piece.location = original_location
            self[original_location].piece = piece
            self[move].piece = captured_piece

            if captured_piece:
                self.pieces.append(captured_piece)

        return (
            [m for m in legal if m in moves],
            [m for m in legal if m in captures]
        )


    
    def move(self, start: Piece, end: str):
        
        start_not = start.location

        # clear en passant flags
        for piece in self.pieces:
            if piece.type == "P":
                piece.passantable = False

        # detect en passant eligibility
        if start.type == "P" and abs(int(start.location[1]) - int(end[1])) == 2:
            start.passantable = True

        # castling
        if start.type == "K" and abs(index_from_notation(start.location)[0] - index_from_notation(end)[0]) == 2:

            if end[0] == "C":
                rook = self[f"A{start.location[1]}"].piece
                rook_target = f"D{start.location[1]}"
            else:
                rook = self[f"H{start.location[1]}"].piece
                rook_target = f"F{start.location[1]}"

            self.squares[rook.location].piece = None
            rook.location = rook_target
            self.squares[rook_target].piece = rook
            rook.moved = True

        # capture
        if self.squares[end].piece:
            self.pieces.remove(self.squares[end].piece)

        # move piece
        self.squares[start_not].piece = None
        self.squares[end].piece = start

        start.location = end
        start.moved = True

        global promotion_piece, promotion_side, promotion_square

        # promotion detection
        if start.type == "P":
            rank = end[1]

            if (start.side == "W" and rank == "8") or (start.side == "B" and rank == "1"):

                promotion_piece = start
                promotion_side = start.side
                promotion_square = end

                return 
        
        # switch turn
        self.turn = "B" if self.turn == "W" else "W"

        # update check status
        if self.check_check(self.turn):
            self.check = self.turn
        else:
            self.check = None

    
    
    def is_square_attacked(self, square: str, by_side: str) -> bool:
        for piece in self.pieces:
            if piece.side == by_side:
                if square in piece.moves():
                    return True
        return False

    def check_check(self, side):
        king = None

        for piece in self.pieces:
            if piece.side == side and piece.type == "K":
                king = piece
                break

        if not king:
            return False

        enemy = "B" if side == "W" else "W"

        return self.is_square_attacked(king.location, enemy)
    
    def is_checkmate(self, side):
        if not self.check_check(side):
            return False
        
        for pice in self.pieces:
            if pice.side == side:
                moves, captures = self.moves(pice)
                if moves or captures:
                    return False
        return True
    

                
            

               
def notation_from_mouse(pos):
    x, y = pos
    
    if not (B.board_corner <= x <= B.board_corner + B.square_length * 8):
        return None
    
    file_index = int((x - B.board_corner) // B.square_length)
    rank_index = int(y // B.square_length)
    
    if not (0 <= file_index < 8 and 0 <= rank_index < 8):
        return None
    
    file = FILES[file_index]
    rank = 8 - rank_index  
    return f"{file}{rank}"


def draw_promotion_ui():

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,150))
    screen.blit(overlay, (0,0))

    box_size = HEIGHT // 8
    start_x = WIDTH//2 - (box_size*2)
    y = HEIGHT//2 - box_size//2

    rects = []

    for i, piece_type in enumerate(promotion_options):

        rect = pygame.Rect(start_x + i*box_size, y, box_size, box_size)

        pygame.draw.rect(screen, "white", rect)
        pygame.draw.rect(screen, "black", rect, 2)

        notation = f"{promotion_side}{piece_type}"

        img = pygame.image.load(
            os.path.join("sprites", f"{notation}.png")
        ).convert_alpha()

        img = pygame.transform.smoothscale(img, (box_size*0.8, box_size*0.8))

        screen.blit(img, img.get_rect(center=rect.center))

        rects.append((rect, piece_type))

    return rects

def draw_win_ui():

    # dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # determine winner
    if B.turn == "W":
        text = "Black Wins"
    else:
        text = "White Wins"


    # create large font
    win_font = pygame.font.SysFont(None, 72)

    text_surf = win_font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    padding = 20
    box_rect = text_rect.inflate(padding*2, padding*2)

    pygame.draw.rect(screen, (240, 240, 240), box_rect)

    screen.blit(text_surf, text_rect)

    

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def rect_from_notation(square:str) -> pygame.Rect:
    return pygame.Rect(B[square].coordinate[0] - B.square_length//2, B[square].coordinate[1]- B.square_length//2, B.square_length, B.square_length)







B = Board()
selected_piece: None | Piece = None
moves = []
captures = []
checkmate = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if checkmate:
                running=False
                pygame.time.wait(300)
            if promotion_piece:
                rects = draw_promotion_ui()
                for rect, piece_type in rects:
                    if rect.collidepoint(event.pos):
                        # replace pawn
                        B.pieces.remove(promotion_piece)
                        new_piece = Piece(
                            promotion_side,
                            piece_type,
                            promotion_square
                        )
                        new_piece.moved = True
                        B.pieces.append(new_piece)
                        B.squares[promotion_square].piece = new_piece
                        # clear promotion state
                        promotion_piece = None
                        promotion_side = None
                        promotion_square = None
                        # switch turn NOW
                        B.turn = "B" if B.turn == "W" else "W"
            square = notation_from_mouse(event.pos)
            if not square:

                selected_piece = None
                moves, captures = [], []
                continue
            
            if selected_piece:
                if square in moves + captures:
                    B.move(selected_piece, square)
                    selected_piece = None
                    checkmate = B.is_checkmate(B.turn)

                elif B[square].piece and B[square].piece.side == B.turn:
                    selected_piece = B[square].piece
                else:
                    selected_piece = None
            else:
                if B[square].piece and B[square].piece.side == B.turn:
                    selected_piece = B[square].piece


            if selected_piece:
                moves, captures = B.moves(selected_piece)
            else:
                moves, captures = [], []

                            
                    
                    
            
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray20")

    
    B.draw()
    
    
    square = notation_from_mouse(pygame.mouse.get_pos())
    if square:
        square_rect = rect_from_notation(square)
        draw_rect_alpha(screen, (255,255,0, 25) , square_rect)
    if selected_piece:
        square_rect = rect_from_notation(selected_piece.location)
        draw_rect_alpha(screen, (255,255,0, 50) , square_rect)
        for move in moves:
            square_rect = rect_from_notation(move)
            draw_rect_alpha(screen, (0,0,255, 50) , square_rect)
        for move in captures:
            square_rect = rect_from_notation(move)
            draw_rect_alpha(screen, (255,0,0, 50) , square_rect)
        
    if B.check:
        for piece in B.pieces:
            if piece.side == B.check and piece.type == "K":
                king = piece
        square_rect = rect_from_notation(king.location)
        draw_rect_alpha(screen, (255,0,255, 50) , square_rect)
    
    if promotion_piece:
        draw_promotion_ui()
        
    if checkmate:
        B.draw()
        draw_win_ui()
    
        
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    

        

pygame.quit()