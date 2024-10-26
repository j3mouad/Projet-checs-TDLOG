import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
screen_width = (500)
screen_height = (500)
screen = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)

# Taille de la case
square_size = screen_width // 8

# Charger les images des pièces (les fichiers doivent être présents dans le même répertoire)
pieces = {
    'bR': pygame.image.load('black_rook.png'),
    'bN': pygame.image.load('black_knight.png'),
    'bB': pygame.image.load('black_bishop.png'),
    'bQ': pygame.image.load('black_queen.png'),
    'bK': pygame.image.load('black_king.png'),
    'bP': pygame.image.load('black_pawn.png'),
    'wR': pygame.image.load('white_rook.png'),
    'wN': pygame.image.load('white_knight.png'),
    'wB': pygame.image.load('white_bishop.png'),
    'wQ': pygame.image.load('white_queen.png'),
    'wK': pygame.image.load('white_king.png'),
    'wP': pygame.image.load('white_pawn.png')
}

# Fonction pour dessiner l'échiquier
def draw_board():
    for row in range(8):
        for col in range(8):
            color = light_brown if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Fonction pour placer les pièces sur l'échiquier
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':  # S'il y a une pièce à cette position
                # Redimensionner l'image de la pièce pour qu'elle corresponde à la taille des cases
                resized_piece = pygame.transform.scale(pieces[piece], (square_size, square_size))
                screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Disposition initiale des pièces sur l'échiquier
chess_board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Boucle principale
running = True
while running:
    draw_board()  # Dessiner l'échiquier
    draw_pieces(chess_board)  # Dessiner les pièces sur l'échiquier

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
