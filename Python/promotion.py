from button import Button
import pygame
from config import *

def Promotion_screen(game,color) :
    
    """Displays the promotion screen allowing the player to choose a piece for pawn promotion.

    Args:
    game (ChessGame): The current game instance.
    color (str): The color of the player choosing the promotion ('white' or 'black').

    Returns:
    str: The type of piece selected for promotion ('Queen', 'Bishop', 'Knight', or 'Rook').
    """
    pygame.init()
    screen = game.screen
    width, height = screen.get_size()
    promotion_screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Choose a Piece")
    # Create buttons
    text_color = red
    buttons = [
        Button("Queen", 50, 50, 150, 150, color+"_queen.png"),
        Button("Bishop", 50, 350, 150, 150,color+"_bishop.png"),
        Button("Knight", 750, 50, 150, 150, color+"_knight.png"),
        Button("Rook", 750, 350, 150, 150, color+"_rook.png"),
    ]

    # Main loop
    running = True
    while running:
        promotion_screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check button clicks
            for button in buttons:
                if button.is_clicked(event):
                    print(f"You selected {button.text}")
                    return button.text

        # Draw buttons
        for button in buttons:
            button.draw(promotion_screen,color = text_color)

        pygame.display.flip()

    pygame.quit()
