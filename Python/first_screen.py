import pygame
from Button import Button  # Assuming the Button class is in a separate module
from config import *
from random import shuffle
def choose_game(board):
    window = pygame.display.set_mode((screen_width + added_screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Let's play Chess!")

    # Load the background image
    background_image = pygame.image.load("background_image.jpg")  # Update with your image path
    background_image = pygame.transform.scale(background_image, (screen_width + added_screen_width, screen_height))

    font = pygame.font.Font(None, 28)
    text = font.render("Choose color and time", True, black)

    button_width = 250
    button_height = 50
    button_margin = 20
    button_x = 50
    button_y = 100

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
    Button("White pieces / AI_hard", button_x, button_y + 6 * button_height + 3 * button_margin, button_width, button_height)
]


    first_choosing = True
    second_choosing = True
    white_time = 0
    black_time = 0

    while first_choosing or second_choosing:
        mouse_pos = pygame.mouse.get_pos()
        # Draw the background image
        window.blit(background_image, (0, 0))
        window.blit(text, (50, 50))

        for button in buttons:
            button.draw(window)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(event):
                    first_choosing = False
                    board.game.flipped = True
                    board.game.player = True
                    board.game.black = True
                    board.game.flip_board()
                elif buttons[1].is_clicked(event):
                    first_choosing = False
                    board.game.player = True
                    board.game.white = True
                elif buttons[8].is_clicked(event):
                    first_choosing = False
                    board.game.player = True
                    board.game.black = True
                    board.game.hard = True
                    board.game.flipped = True
                    board.game.flip_board()
                elif buttons[9].is_clicked(event):
                    first_choosing = False
                    board.game.player = True
                    board.game.white = True
                    board.game.hard = True

                elif buttons[2].is_clicked(event):
                    first_choosing = False
                    board.game.one_v_one = True
                elif buttons[3].is_clicked(event):
                    shuffle(board.game.chess_board[0])
                    shuffle(board.game.chess_board[7])
                elif buttons[4].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(600, 600)
                    white_time = 600
                    black_time = 600
                elif buttons[5].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(3600, 3600)
                    white_time = 3600
                    black_time = 3600
                elif buttons[6].is_clicked(event):
                    second_choosing = False
                    board.game.time_reg(60, 60)
                    white_time = 60
                    black_time = 60
                elif buttons[7].is_clicked(event):
                    first_choosing = False
                    board.game.chess_board[0][0] = 'bW'
                    board.game.chess_board[0][2] = 'bF'
                    board.game.chess_board[0][7] = 'bW'
                    board.game.chess_board[0][5] = 'bF'
                    board.game.chess_board[7][0] = 'wW'
                    board.game.chess_board[7][2] = 'wF'
                    board.game.chess_board[7][7] = 'wW'
                    board.game.chess_board[7][5] = 'wF' 
                    board.game.chess_board[0][1] = 'bC'
                    board.game.chess_board[0][6] = 'bC'
                    board.game.chess_board[7][1] = 'wC'
                    board.game.chess_board[7][6] = 'wC'
                    board.game.chess_board[0][3] = 'bM'
                    board.game.chess_board[7][3] = 'wM'


                    

    board.game.list_of_boards[0] = [board.game.chess_board]
    board.game.len_list_of_boards += 1
    return white_time, black_time
