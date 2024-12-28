import pygame

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 150, 255)

# Set initial screen size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Resize Screen Example')

# Define Button Class
class ResizeButton:
    def __init__(self, x, y, width, height, color, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
    
    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw text in the center of the button
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self, mouse_x, mouse_y):
        """Check if the mouse is hovering over the button."""
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
    
    def handle_click(self, mouse_x, mouse_y):
        """If the button is clicked, resize the window."""
        global screen_width, screen_height
        if self.is_hovered(mouse_x, mouse_y):
            # Example resizing logic: Increase screen size by 100x100 pixels each click
            screen_width += 100
            screen_height += 100
            pygame.display.set_mode((screen_width, screen_height))  # Resize the screen
            return True
        return False

# Create a resize button
resize_button = ResizeButton(50, 50, 200, 50, BUTTON_COLOR, "Resize Screen")

# Main loop
if __name__ == '__main__':
    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if resize_button.handle_click(mouse_x, mouse_y):
                    print(f"Resized screen to {screen_width}x{screen_height}")
        
        # Draw the button
        resize_button.draw(screen)

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
