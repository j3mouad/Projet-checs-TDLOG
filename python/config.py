import pygame
import os

pygame.init()

# Function to safely load sounds
def load_sound(path):
    if not os.path.exists(path):
        print(f"Warning: Sound file {path} not found. Using default sound.")
        return None  
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return None

# Function to safely load images
def load_image(path, size):
    if not os.path.exists(path):
        print(f"Warning: Image file {path} not found. Using a placeholder.")
        return pygame.Surface((size, size))  
    try:
        return pygame.image.load(path)  # Fixed incorrect recursive call
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return pygame.Surface((size, size))  

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
HOVER_COLOR = (204, 255, 250)

# Button colors
button_color = (100, 200, 100)  # green
button_hover_color = (150, 250, 150)

# Load sound effects
click_sound_add_time_button = load_sound("./sounds/chess_add_time_sound.wav")
click_sound_chess = load_sound("./sounds/chess_move_soundf.mp3")
check_sound = load_sound("./sounds/move-check.mp3")

# Load pieces images
pieces_images = {
    'bR': load_image('./images/black_rook.png', square_size),
    'bN': load_image('./images/black_knight.png', square_size),
    'bB': load_image('./images/black_bishop.png', square_size),
    'bQ': load_image('./images/black_queen.png', square_size),
    'bK': load_image('./images/black_king.png', square_size),
    'bP': load_image('./images/black_pawn.png', square_size),
    'wR': load_image('./images/white_rook.png', square_size),
    'wN': load_image('./images/white_knight.png', square_size),
    'wB': load_image('./images/white_bishop.png', square_size),
    'wQ': load_image('./images/white_queen.png', square_size),
    'wK': load_image('./images/white_king.png', square_size),
    'wP': load_image('./images/white_pawn.png', square_size),
    'wW': load_image('./images/white_wazir.png', square_size),
    'bW': load_image('./images/black_wazir.png', square_size),
    'wF': load_image('./images/white_ferz.png', square_size),
    'bF': load_image('./images/black_ferz.png', square_size),
    'wC': load_image('./images/white_camel.png', square_size),
    'bC': load_image('./images/black_camel.png', square_size),
    'wM': load_image('./images/white_malika.png', square_size),
    'bM': load_image('./images/black_malika.png', square_size)
}
