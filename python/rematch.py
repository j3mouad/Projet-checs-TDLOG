import pygame
from config import *
from button import Button

def Rematch_screen(winner):
    if winner is None :
        return
    # Initialize the Pygame screen
    screen = pygame.display.set_mode((screen_width , screen_height))
    pygame.display.set_caption("Rematch?")

    # Set up the winner message
    FONT = pygame.font.Font(None, 48)
    if winner == 1 :
        winner_text = "white Wins!"
    elif winner == -1 : 
        winner_text = "black Wins!"
    else :
        winner_text = "Stale_mate"
    
    winner_surface = FONT.render(winner_text, True, (0, 0, 0))  # Black color for text
    winner_rect = winner_surface.get_rect(center=(screen_width // 2 , screen_height // 4))

    # Create rematch button using the Button class
    rematch_button = Button('Rematch', (screen_width) // 2 - 25, screen_height // 2 - 30, 100, 80)
    quit_button = Button('Quit', (screen_width) // 2 - 25, screen_height // 2 + 100, 100, 80)

    running = True
    while running:
        screen.fill(WHITE)  # Fill the screen with white

        # Display the winner message
        screen.blit(winner_surface, winner_rect)

        # Draw the buttons
        rematch_button.draw(screen,32)
        quit_button.draw(screen,32)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the rematch button was clicked
                if rematch_button.rect.collidepoint(mouse_pos):
                    return True  # Start a new game

                # Check if the quit button was clicked
                if quit_button.rect.collidepoint(mouse_pos):
                    return False  # Exit the game

        pygame.display.flip()  # Update the screen

    pygame.quit()
    return False  # If no button is clicked
