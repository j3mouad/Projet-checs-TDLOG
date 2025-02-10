import pygame
from button import Button
from config import *
from fisher import shuffle_fischer_row

def choose_game(board):
    """
    Displays a screen where the user can select game options for a chess game.
    
    Parameters:
        board (object): An instance of the board containing game settings and state.

    Returns:
        tuple: Contains two integers representing the chosen time for white and black players in seconds.
    """
    
    global screen_width, screen_height
    
    # Set up the window
    window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Let's play Chess!")

    # Load the background image
    background_image = pygame.image.load("./python/images/background_image.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Font for text
    font = pygame.font.Font(None, int(screen_width / 25))
    text = font.render("Choose color and time", True, BLACK)

    # Button sizes and positions
    button_width = screen_width // 4
    button_height = screen_height // 12
    button_margin = screen_height // 30
    button_x = screen_width // 10
    button_y = screen_height // 6
    size = screen_width / 50

    # Button definitions
    buttons = [
        Button("Black pieces / AI", button_x, button_y, button_width, button_height),
        Button("White pieces / AI", button_x, button_y + button_height + button_margin, button_width, button_height),
        Button("1 VS 1", button_x + button_width + 20, button_y + button_height + button_margin, button_width, button_height),
        Button("Fisher", button_x, button_y + 4 * button_height, button_width, button_height),
        Button("Rapid", button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
        Button("Classic", button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
        Button("Blitz", button_x + button_width + 40, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
        Button("Ferry", button_x + button_width + 40 + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
        Button("Black pieces / AI_hard", button_x, button_y + 5 * button_height + 2 * button_margin, button_width, button_height),
        Button("White pieces / AI_hard", button_x, button_y + 6 * button_height + 3 * button_margin, button_width, button_height),
        Button("King of the Hill", button_x + button_width + 40, button_y + 4 * button_height, button_width, button_height)
    ]

    # Game state variables
    first_choosing = True
    second_choosing = True
    white_time = black_time = 0

    # Event loop
    while first_choosing or second_choosing:
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw background and buttons
        window.blit(background_image, (0, 0))
        window.blit(text, (50, 50))

        for button in buttons:
            button.draw(window, size=int(screen_width / 50))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                button_width = screen_width // 4
                button_height = screen_height // 12
                button_margin = screen_height // 30
                button_x = screen_width // 10
                button_y = screen_height // 6
                buttons = [
                    Button("Black pieces / AI", button_x, button_y, button_width, button_height),
                    Button("White pieces / AI", button_x, button_y + button_height + button_margin, button_width, button_height),
                    Button("1 VS 1", button_x + button_width + 20, button_y + button_height + button_margin, button_width, button_height),
                    Button("Fisher", button_x, button_y + 4 * button_height, button_width, button_height),
                    Button("Rapid", button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
                    Button("Classic", button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
                    Button("Blitz", button_x + button_width + 40, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
                    Button("Ferry", button_x + button_width + 40 + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height),
                    Button("Black pieces / AI_hard", button_x, button_y + 5 * button_height + 2 * button_margin, button_width, button_height),
                    Button("White pieces / AI_hard", button_x, button_y + 6 * button_height + 3 * button_margin, button_width, button_height),
                    Button("King of the Hill", button_x + button_width + 40, button_y + 4 * button_height, button_width, button_height)
                ]
                print(f"Window resized to {event.w}x{event.h}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(event):
                    first_choosing = False
                    board.game.flipped, board.game.player, board.game.black = True, True, True
                    board.game.flip_board()
                elif buttons[1].is_clicked(event):
                    first_choosing = False
                    board.game.player, board.game.white = True, True
                elif buttons[8].is_clicked(event):
                    first_choosing = False
                    board.game.player, board.game.black, board.game.hard = True, True, True
                    board.game.flipped = True
                    board.game.flip_board()
                elif buttons[9].is_clicked(event):
                    first_choosing = False
                    board.game.player, board.game.white, board.game.hard = True, True, True
                elif buttons[2].is_clicked(event):
                    first_choosing = False
                    board.game.one_v_one = True
                elif buttons[3].is_clicked(event):
                    first_choosing = False
                    fischer_row = shuffle_fischer_row()
                    board.game.fisher = True
                    board.game.chess_board[7] = (['w' + fischer_row[i] for i in range(8)])
                    board.game.chess_board[0] = ['b' + fischer_row[i] for i in range(8)]
                elif buttons[4].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(600, 600)
                    white_time, black_time = 600, 600
                elif buttons[5].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(3600, 3600)
                    white_time, black_time = 3600, 3600
                elif buttons[6].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(60, 60)
                    white_time, black_time = 60, 60
                elif buttons[7].is_clicked(event):
                    first_choosing = False
                    board.game.setup_ferry_mode()
                elif buttons[10].is_clicked(event):
                    first_choosing = False
                    board.game.one_v_one, board.game.king_of_the_hill = True, True

    # Update board state
    board.game.list_of_boards[0] = [board.game.chess_board]
    board.game.len_list_of_boards += 1

    return white_time, black_time, screen_width, screen_height
