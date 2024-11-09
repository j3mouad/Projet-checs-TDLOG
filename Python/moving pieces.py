import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Highlight color for possible moves
YELLOW = (255, 255, 0)  # Highlight color for last move

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Move Generator")

# Font setup
font = pygame.font.Font(None, 74)

# Chess board setup with initial positions
board = [
    ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
]

turn = 'white'  # Track whose turn it is
last_move = None  # Track the last move for highlighting

# Piece movement rules (improved with turn-based logic)
def is_valid_move(board, piece, start, end):
    x, y = start
    mx, my = end
    target_piece = board[my][mx]

    if (piece.isupper() and turn != 'white') or (piece.islower() and turn != 'black'):
        return False  # Only allow moves for the correct player's turn

    # Check if the move is to an occupied square by the same color
    if target_piece is not None and target_piece.isupper() == piece.isupper():
        return False

    # Pawn movement (simplified)
    direction = -1 if piece.isupper() else 1  # Up for white, down for black
    if piece.lower() == 'p':
        if mx == x and board[my][mx] is None:  # Move forward
            if (piece.isupper() and y == 6 and my == y + 2 and board[y + 1][x] is None) or (my == y + direction):
                return True
        elif abs(mx - x) == 1 and my == y + direction and target_piece is not None:  # Capture
            return True

    # Rook movement (horizontal and vertical)
    elif piece.lower() == 'r':
        if x == mx or y == my:
            step_x = 1 if mx > x else -1 if mx < x else 0
            step_y = 1 if my > y else -1 if my < y else 0
            for i in range(1, max(abs(mx - x), abs(my - y))):
                if board[y + i * step_y][x + i * step_x] is not None:
                    return False
            return True

    # Knight movement (L-shape)
    elif piece.lower() == 'n':
        if (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2):
            return True

    # Bishop movement (diagonal)
    elif piece.lower() == 'b':
        if abs(mx - x) == abs(my - y):
            step_x = 1 if mx > x else -1
            step_y = 1 if my > y else -1
            for i in range(1, abs(mx - x)):
                if board[y + i * step_y][x + i * step_x] is not None:
                    return False
            return True

    # Queen movement (rook + bishop)
    elif piece.lower() == 'q':
        if abs(mx - x) == abs(my - y) or x == mx or y == my:
            step_x = 1 if mx > x else -1 if mx < x else 0
            step_y = 1 if my > y else -1 if my < y else 0
            for i in range(1, max(abs(mx - x), abs(my - y))):
                if board[y + i * step_y][x + i * step_x] is not None:
                    return False
            return True

    # King movement (one square in any direction)
    elif piece.lower() == 'k':
        if max(abs(mx - x), abs(my - y)) == 1:
            return True

    return False

def get_possible_moves(piece, x, y):
    moves = []
    for mx in range(8):
        for my in range(8):
            if is_valid_move(board, piece, (x, y), (mx, my)):
                moves.append((mx, my))
    return moves

# Main loop
running = True
selected_piece = None
selected_position = None
possible_moves = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            x = mouse_x // SQUARE_SIZE
            y = mouse_y // SQUARE_SIZE

            if selected_piece is None:
                if board[y][x] is not None:
                    selected_piece = board[y][x]
                    selected_position = (x, y)
                    possible_moves = get_possible_moves(selected_piece, x, y)
            else:
                if (x, y) in possible_moves:
                    board[y][x] = selected_piece
                    board[selected_position[1]][selected_position[0]] = None
                    last_move = (selected_position, (x, y))  # Track the last move
                    turn = 'black' if turn == 'white' else 'white'
                selected_piece = None
                selected_position = None
                possible_moves = []

    # Draw board
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Draw last move highlight
            if last_move:
                start, end = last_move
                if (col, row) == start or (col, row) == end:
                    pygame.draw.rect(screen, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw pieces
            if board[row][col] is not None:
                text_surface = font.render(board[row][col], True, (255, 0, 0) if board[row][col].isupper() else (0, 0, 255))
                screen.blit(text_surface, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE))

    # Highlight possible moves
    for mx, my in possible_moves:
        pygame.draw.rect(screen, GREEN, (mx * SQUARE_SIZE, my * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()

pygame.quit()
