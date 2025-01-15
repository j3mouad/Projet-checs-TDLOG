# config.py
"""This file is only used for writing constants we need after that."""
import pygame
pygame.init()
# Screen dimensions
screen_width = 1000
screen_height = 500

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
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")
click_sound_chess = pygame.mixer.Sound("chess_move_soundf.mp3")
check_sound = pygame.mixer.Sound("move-check.mp3")
# Load sound effects


#laod pieces images
pieces_images = {
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
    'wP': pygame.image.load('white_pawn.png'),
    'wW':pygame.image.load('white_wazir.png'),
    'bW':pygame.image.load('black_wazir.png'),
    'wF':pygame.image.load('white_ferz.png'),
    'bF':pygame.image.load('black_ferz.png'),
    'wC':pygame.image.load('white_camel.png'),
    'bC':pygame.image.load('black_camel.png'),
    'wM':pygame.image.load('white_malika.png'),
    'bM':pygame.image.load('black_malika.png')

}