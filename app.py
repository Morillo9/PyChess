#!/usr/bin/python3

"""
Python Chess Client
"""

import chess
import pygame

class Piece():
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

pygame.init()

pygame.display.set_caption('PyChess')
HEIGHT, WIDTH = 512, 512
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARE_LIGHT = pygame.Surface((64, 64))
SQUARE_LIGHT.convert()
SQUARE_LIGHT.fill(pygame.Color("#E9E9E9"))
SQUARE_DARK = pygame.Surface((64, 64)).convert()
SQUARE_DARK.fill(pygame.Color("#6F83B5"))
SQUARE_CLICKED = pygame.Surface((64, 64)).convert()
SQUARE_CLICKED.fill(pygame.Color("#34F02E"))

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

def main():

    move_array = []
    game = True

    while game:
        for x in range(8):
            for y in range(8):
                if (x, y) not in move_array:
                    if (x + y) % 2 == 0:
                        SCREEN.blit(SQUARE_DARK, (x * 64, y * 64))
                    else:
                        SCREEN.blit(SQUARE_LIGHT, (x * 64, y * 64))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x_val, y_val = int(pos[0] / 64), 7 - (int(pos[1] / 64))
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
            else:
                move_array = []

        updateBoard()
        pygame.display.flip()
        CLOCK.tick(30)

if __name__ == "__main__": main()
