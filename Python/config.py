# config.py
"""This file is only used for writing constants we need after that."""

# Now the relative paths will be based on this directory

import pygame
pygame.init()
# Screen dimensions
screen_width = 1600
screen_height = 800

square_size = screen_height // 8

# Colors
white = (255, 255, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
orange = (255, 165, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
highlight_color = (200, 200, 0)
black = (0, 0, 0)
HOVER_COLOR = (204,255,250)
# Button colors
button_color = (100, 200, 100)  # green
button_hover_color = (150, 250, 150)

# Load sound effects
click_sound_add_time_button = pygame.mixer.Sound("./sounds/chess_add_time_sound.wav")
click_sound_chess = pygame.mixer.Sound("./sounds/chess_move_soundf.mp3")
check_sound = pygame.mixer.Sound("./sounds/move-check.mp3")

# Load pieces images
pieces_images = {
    'bR': pygame.image.load('./images/black_rook.png'),
    'bN': pygame.image.load('./images/black_knight.png'),
    'bB': pygame.image.load('./images/black_bishop.png'),
    'bQ': pygame.image.load('./images/black_queen.png'),
    'bK': pygame.image.load('./images/black_king.png'),
    'bP': pygame.image.load('./images/black_pawn.png'),
    'wR': pygame.image.load('./images/white_rook.png'),
    'wN': pygame.image.load('./images/white_knight.png'),
    'wB': pygame.image.load('./images/white_bishop.png'),
    'wQ': pygame.image.load('./images/white_queen.png'),
    'wK': pygame.image.load('./images/white_king.png'),
    'wP': pygame.image.load('./images/white_pawn.png'),
    'wW': pygame.image.load('./images/white_wazir.png'),
    'bW': pygame.image.load('./images/black_wazir.png'),
    'wF': pygame.image.load('./images/white_ferz.png'),
    'bF': pygame.image.load('./images/black_ferz.png'),
    'wC': pygame.image.load('./images/white_camel.png'),
    'bC': pygame.image.load('./images/black_camel.png'),
    'wM': pygame.image.load('./images/white_malika.png'),
    'bM': pygame.image.load('./images/black_malika.png')
}
