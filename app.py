#!/usr/bin/python3

"""
Python Chess Client
"""

import chess
from chess import uci
import pygame

class Piece():
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_shade = pygame.Surface((w + 3, h + 3)).convert()
    button_shade.fill(pygame.Color(105, 105, 105))
    SCREEN.blit(button_shade, (x, y))
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(SCREEN, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(SCREEN, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("Ubuntu",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    SCREEN.blit(textSurf, textRect)


def updateBoard():
    for square in chess.SQUARES:
        piece = str(BOARD.piece_at(square))
        x_cord = chess.file_index(square)
        y_cord = 7 - chess.rank_index(square)
        piece_dict = { 'P':LIGHT_PAWN.image, 'p':DARK_PAWN.image, 'B':L_BISHOP.image, 
            'b':D_BISHOP.image, 'R':L_ROOK.image,'r':D_ROOK.image,'N':L_KNIGHT.image, 
            'n':D_KNIGHT.image,'Q':L_QUEEN.image,'q':D_QUEEN.image, 'K':L_KING.image, 
            'k':D_KING.image
        }
        if piece != "None":
            SCREEN.blit(piece_dict[piece], (x_cord  * 64, y_cord * 64))

def resetBoard():
    global move_array
    BOARD.reset()
    move_array = []

def toBeginning():
    global move_array
    global TMP
    while len(BOARD.move_stack) > 0:
        TMP.append(BOARD.pop())
    move_array = []

def oneBack():
    global move_array
    global TMP
    if len(BOARD.move_stack) > 0:
        TMP.append(BOARD.pop())
    move_array = []

def pushOne():
    if len(TMP) > 0:
        BOARD.push(TMP.pop())

def toEnd():
    while len(TMP) > 0:
        BOARD.push(TMP.pop())

pygame.init()

pygame.display.set_caption('PyChess')
WIDTH, HEIGHT = 512, 570
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARE_LIGHT = pygame.Surface((64, 64)).convert()
SQUARE_LIGHT.fill(pygame.Color("#E9E9E9"))
SQUARE_DARK = pygame.Surface((64, 64)).convert()
SQUARE_DARK.fill(pygame.Color("#6F83B5"))
SQUARE_CLICKED = pygame.Surface((64, 64)).convert()
SQUARE_CLICKED.fill(pygame.Color("#34F02E"))
BACKGROUND = pygame.Surface((WIDTH, 512)).convert()
BACKGROUND.fill(pygame.Color("#D3D3D3"))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_BACK = (255, 222, 173)

LIGHT_PAWN = Piece(64, 6*64, './images/Chess_tile_pl.png')
DARK_PAWN = Piece(64, 6*64, './images/Chess_tile_pd.png')
L_BISHOP = Piece(64, 6*64, './images/Chess_tile_bl.png')
D_BISHOP = Piece(64, 6*64, './images/Chess_tile_bd.png')
L_ROOK = Piece(64, 6*64, './images/Chess_tile_rl.png')
D_ROOK = Piece(64, 6*64, './images/Chess_tile_rd.png')
L_KNIGHT = Piece(64, 6*64, './images/Chess_tile_nl.png')
D_KNIGHT = Piece(64, 6*64, './images/Chess_tile_nd.png')
L_QUEEN = Piece(64, 6*64, './images/Chess_tile_ql.png')
D_QUEEN = Piece(64, 6*64, './images/Chess_tile_qd.png')
L_KING = Piece(64, 6*64, './images/Chess_tile_kl.png')
D_KING = Piece(64, 6*64, './images/Chess_tile_kd.png')

CLOCK = pygame.time.Clock()
BOARD = chess.Board()
move_array = []
TMP = []

def main():
    global move_array
    game = True
    engine = uci.popen_engine('./Engine/stockfish_8_x64')
    engine.uci()

    while game:

        SCREEN.blit(BACKGROUND, (0, 512))
        button("Reset", 50, 520, 100, 30, BUTTON_BACK, BUTTON_BACK, resetBoard)
        button("<<", 200, 520, 50, 30, BUTTON_BACK, BUTTON_BACK, toBeginning)
        button("<", 270, 520, 50, 30, BUTTON_BACK, BUTTON_BACK, oneBack)
        button(">", 340, 520, 50, 30, BUTTON_BACK, BUTTON_BACK, pushOne)
        button(">>", 410, 520, 50, 30, BUTTON_BACK, BUTTON_BACK, toEnd)

        for row in range(8):
            for column in range(8):
                if (row, column) not in move_array:
                    if (row + column) % 2 == 0:
                        SCREEN.blit(SQUARE_DARK, (row * 64, column * 64))
                    else:
                        SCREEN.blit(SQUARE_LIGHT, (row * 64, column * 64))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x_val, y_val = int(pos[0] / 64), 7 - (int(pos[1] / 64))
                if y_val >= 0:
                    move_array.append((x_val, y_val))

        if len(move_array) == 1:
            SCREEN.blit(SQUARE_CLICKED, (move_array[0][0] * 64, (7 - move_array[0][1]) * 64))

        if len(move_array) == 2:
            square_x = chess.square(move_array[0][0], move_array[0][1])
            square_y = chess.square(move_array[1][0], move_array[1][1])

            if (str(BOARD.piece_at(square_x)) == 'P' or str(BOARD.piece_at(square_x)) == 'p') \
            and chess.file_index(square_x) != chess.file_index(square_y) and \
            (chess.rank_index(square_y) == 0 or chess.rank_index(square_y) == 7):
                cur_move = chess.Move(square_x, square_y, promotion=5)
            else:
                cur_move = chess.Move(square_x, square_y)

            if cur_move in BOARD.legal_moves:
                BOARD.push(cur_move)
                engine_position = engine.position(BOARD)
                engine_moves = engine.go()
                BOARD.push(engine_moves[0])
            else:
                move_array = []


        updateBoard()
        pygame.display.flip()
        CLOCK.tick(30)

if __name__ == "__main__": main()
