import pygame
import chess
import time
from AIchess import AIChess  # Import the AIChess class
pygame.init()

BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

piece_images = {
    'wR': pygame.image.load("pieces/wR.png"),
    'wN': pygame.image.load("pieces/wN.png"),
    'wB': pygame.image.load("pieces/wB.png"),
    'wQ': pygame.image.load("pieces/wQ.png"),
    'wK': pygame.image.load("pieces/wK.png"),
    'wP': pygame.image.load("pieces/wP.png"),
    'bR': pygame.image.load("pieces/bR.png"),
    'bN': pygame.image.load("pieces/bN.png"),
    'bB': pygame.image.load("pieces/bB.png"),
    'bQ': pygame.image.load("pieces/bQ.png"),
    'bK': pygame.image.load("pieces/bK.png"),
    'bP': pygame.image.load("pieces/bP.png"),
}

for key, image in piece_images.items():
    piece_images[key] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Python Chess Game")

def draw_board(screen, board, selected_square, legal_moves):
    possible = []
    if selected_square:
        for move in board.legal_moves:
            if move.to_square == selected_square:
                possible.append(move)
    for square in range(64):
        x = (square % 8) * SQUARE_SIZE
        y = (7 - square // 8) * SQUARE_SIZE
        color = WHITE if (square // 8 + square % 8) % 2 == 0 else BLACK
        pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        if selected_square == square:
            pygame.draw.rect(screen, YELLOW, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        if legal_moves and square in [move.to_square for move in legal_moves]:
            pygame.draw.rect(screen, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        for p in possible:
            if p.from_square == square:
                pygame.draw.rect(screen, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                

        piece = board.piece_at(square)
        if piece:
            piece_str = piece.symbol()
            piece_str = ["b","w"][piece_str.isupper()] + piece_str.upper()
            screen.blit(piece_images[piece_str], (x, y))

def handle_click(board, selected_square, x, y):
    square = (7-y // SQUARE_SIZE) * 8 + (x // SQUARE_SIZE)
    if selected_square is None:
        possible = []
        for move in board.legal_moves:
            if move.to_square == square:
                possible.append(move)
        if len(possible) == 1:
            board.push(possible[0])
        elif len(possible) > 1:
            return square
        elif board.piece_at(square):
            return square
    else:
        move = chess.Move(square, selected_square)
        if move in board.legal_moves:
            board.push(move)
        else:
            move = chess.Move(selected_square, square)
            if move in board.legal_moves:
                board.push(move)
    return None

ai_engine = AIChess()
board = ai_engine.board
selected_square = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            selected_square = handle_click(board, selected_square, x, y)

    legal_moves = list(board.legal_moves) if selected_square is not None else []
    draw_board(screen, board, selected_square, legal_moves)
    
    pygame.display.flip()

    if not board.is_game_over() and board.turn == chess.BLACK:
        best_move = ai_engine.chessAIMove()[0]
        if best_move:
            board.push(chess.Move.from_uci(best_move))
        selected_square = None

pygame.quit()
