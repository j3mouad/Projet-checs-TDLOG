from Button import Button
import pygame
import sys
from config import *

def Promotion_screen(color) :
    pygame.init()
    promotion_screen = pygame.display.set_mode((screen_width*2, screen_height))
    pygame.display.set_caption("Choose a Piece")
    # Create buttons
    buttons = [
        Button("Queen", 50, 50, 100, 100, color+"_queen.png"),
        Button("Bishop", 50, 350, 100, 100,color+"_bishop.png"),
        Button("Knight", 750, 50, 100, 100, color+"_knight.png"),
        Button("Rook", 750, 350, 100, 100, color+"_rook.png"),
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
            button.draw(promotion_screen)

        pygame.display.flip()

    pygame.quit()
