import pygame

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Highlight color for possible moves

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Move Generator")

# Font setup
font = pygame.font.Font(None, 74)

# Chess board setup with initial positions
# Represent pieces with their initials
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
]

# Piece movement rules
def is_valid_move(board, piece, start, end):
    x, y = start
    mx, my = end
    target_piece = board[my][mx]

    # Check if the move is to an occupied square
    if target_piece is not None and target_piece[0] == piece[0]:
        return False

    if piece[1].lower() == 'p':  # Pawn
        direction = -1 if piece.isupper() else 1  # Up for white, down for black
        if mx == x and target_piece is None:  # Move forward
            if (piece.isupper() and y == 6 and my == y + 2 and target_piece is None) or (my == y + direction):
                return True
        elif abs(mx - x) == 1 and my == y + direction and target_piece is not None:  # Capture
            return True

    elif piece.lower() == 'r':  # Rook
        if x == mx:  # Same column
            step = 1 if my > y else -1
            for i in range(y + step, my, step):
                if board[i][x] is not None:
                    return False
            return True
        elif y == my:  # Same row
            step = 1 if mx > x else -1
            for i in range(x + step, mx, step):
                if board[y][i] is not None:
                    return False
            return True

    elif piece.lower() == 'n':  # Knight
        if (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2):
            return True

    elif piece.lower() == 'b':  # Bishop
        if abs(mx - x) == abs(my - y):  # Diagonal move
            step_x = 1 if mx > x else -1
            step_y = 1 if my > y else -1
            for i in range(1, abs(mx - x)):
                if board[y + i * step_y][x + i * step_x] is not None:
                    return False
            return True

    elif piece.lower() == 'q':  # Queen
        if abs(mx - x) == abs(my - y) or x == mx or y == my:  # Rook + Bishop
            step_x = 1 if mx > x else -1
            step_y = 1 if my > y else -1
            if abs(mx - x) == abs(my - y):
                for i in range(1, abs(mx - x)):
                    if board[y + i * step_y][x + i * step_x] is not None:
                        return False
            else:
                if x == mx:
                    step = 1 if my > y else -1
                    for i in range(y + step, my, step):
                        if board[i][x] is not None:
                            return False
                else:
                    step = 1 if mx > x else -1
                    for i in range(x + step, mx, step):
                        if board[y][i] is not None:
                            return False
            return True

    elif piece.lower() == 'k':  # King
        if max(abs(mx - x), abs(my - y)) == 1:  # One square in any direction
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
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            x = mouse_x // SQUARE_SIZE
            y = mouse_y // SQUARE_SIZE
            
            # If a piece is selected
            if selected_piece is None:
                # Select a piece if it's not empty
                if board[y][x] is not None:
                    selected_piece = board[y][x]
                    selected_position = (x, y)
                    possible_moves = get_possible_moves(selected_piece, x, y)
            else:
                # Move the piece if the move is valid
                if (x, y) in possible_moves:
                    board[y][x] = selected_piece  # Move piece
                    board[selected_position[1]][selected_position[0]] = None  # Remove from original position
                # Reset selection
                selected_piece = None
                selected_position = None
                possible_moves = []

    # Drawing the board
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Draw the pieces using letters
            if board[row][col] is not None:
                text_surface = font.render(board[row][col], True, (255, 0, 0) if board[row][col].isupper() else (0, 0, 255))
                screen.blit(text_surface, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE))

    # Highlight possible moves
    for mx, my in possible_moves:
        pygame.draw.rect(screen, GREEN, (mx * SQUARE_SIZE, my * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Refresh the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
