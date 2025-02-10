"""This file is only used for writing constants we need after that."""

import pygame
import os

pygame.init()

# Screen dimensions (not constants)
screen_width = 1600
screen_height = 800

square_size = screen_height // 8

# Colors

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BROWN = (118, 150, 86)
LIGHT_BROWN = (238, 238, 210)
HIGHLIGHT_COLOR = (200, 200, 0)
BLACK = (0, 0, 0)
HOVER_COLOR = (204, 255, 250)

# Button colors
BUTTON_COLOR = (100, 200, 100)  # Green
BUTTON_HOVER_COLOR = (150, 250, 150)

# Helper function to safely load assets
def load_sound(path):
    """Load a sound file safely."""
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        print(f"Warning: Sound file not found: {path}")
        return None

def load_image(path):
    """Load an image file safely."""
    if os.path.exists(path):
        return pygame.image.load(path)
    else:
        print(f"Warning: Image file not found: {path}")
        return None

# Load sound effects
CLICK_SOUND_ADD_TIME_BUTTON = load_sound("./python/sounds/chess_add_time_sound.wav")
CLICK_SOUND_CHESS = load_sound("./python/sounds/chess_move_sound.mp3")
CHECK_SOUND = load_sound("./python/sounds/move-check.mp3")

# Load pieces images
PIECES_IMAGES = {
    'bR': load_image('./python/images/black_rook.png'),
    'bN': load_image('./python/images/black_knight.png'),
    'bB': load_image('./python/images/black_bishop.png'),
    'bQ': load_image('./python/images/black_queen.png'),
    'bK': load_image('./python/images/black_king.png'),
    'bP': load_image('./python/images/black_pawn.png'),
    'wR': load_image('./python/images/white_rook.png'),
    'wN': load_image('./python/images/white_knight.png'),
    'wB': load_image('./python/images/white_bishop.png'),
    'wQ': load_image('./python/images/white_queen.png'),
    'wK': load_image('./python/images/white_king.png'),
    'wP': load_image('./python/images/white_pawn.png'),
    'wW': load_image('./python/images/white_wazir.png'),
    'bW': load_image('./python/images/black_wazir.png'),
    'wF': load_image('./python/images/white_ferz.png'),
    'bF': load_image('./python/images/black_ferz.png'),
    'wC': load_image('./python/images/white_camel.png'),
    'bC': load_image('./python/images/black_camel.png'),
    'wM': load_image('./python/images/white_malika.png'),
    'bM': load_image('./python/images/black_malika.png')
}
