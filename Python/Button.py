import pygame
import sys
from config import *

# Initialize Pygame
pygame.init()

class Button:
    def __init__(self, text, x, y, width, height, image_path=None,color = grey):
        """Initialize the Button with text, position, size, optional image, and color."""

        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = HOVER_COLOR
        if (image_path is not None) :
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width - 10, height - 10))  # Scale image to fit button
        else :
            self.image = None

    def draw(self, screen,size = 20,color = black):
        """Draw the button on the screen with optional text and image."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Draw the image
        if (self.image is not None) :
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect)

        # Optional: Draw the text (comment this if you want just the image)
        FONT0 = pygame.font.Font(None, size)  # `None` uses the default system font
        text_surface = FONT0.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Check if the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
squares = [[None for _ in range(8)] for _ in range(8)]
def draw(squares,x_square_size,y_square_size):
    for row in range(8):
                for col in range(8):
                    color = light_brown if (row + col) % 2 == 0 else brown
                    square = Button("",col*x_square_size,row*y_square_size,square_size,square_size,image_path = None,color = color)
                    squares[col][row] = square