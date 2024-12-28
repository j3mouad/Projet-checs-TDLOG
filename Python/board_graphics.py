
import pygame
import sys
from copy import deepcopy
import time
from random import shuffle
from utils import *
import os
new_dir = ('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
os.chdir(new_dir)
import numpy as np
import copy
from AI import AI
from chess import chessGame
class Board_chess() :
    def __init__(self, board, screen, square_size, piece_size) :
        self.game = chessGame()
        self.screen = screen
    

    def draw_move_back_button(self):
        # Define button properties

        button_width = 60
        button_height = 50
        button_x = screen_width + 150
        button_y = 300
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Draw button with hover effect
        pygame.draw.rect(self.screen, black if not button_rect.collidepoint(mouse_pos) else button_hover_color, button_rect)

        # Render text on button
        font = pygame.font.Font(None, 24)  # Choose font size and style
        text = font.render("Back", True, white)  # Render text with white color
        text_rect = text.get_rect(center=button_rect.center)  # Center text on button
        self.screen.blit(text, text_rect)

        # Handle click on button
        if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            # Prevent multiple triggers with cooldown and only trigger on mouse button down
            self.handle_back_button_click()

    def handle_back_button_click(self):
        # Logic for what happens when the button is clicked
        time = pygame.time.get_ticks()
        if ((time - self.last_time_back_clicked) <= self.cooldown):
            return
        if (self.len_list_of_boards == 0):
            return
        self.last_time_back_clicked = time
        self.len_list_of_boards-=1
        l=self.len_list_of_boards
        self.white_time, self.black_time = self.list_of_times[l - 1]
        self.chess_board = deepcopy(self.list_of_boards[l - 1])
        self.last_move=self.list_of_last_moves[l-1]
        self.castle = deepcopy(self.list_of_castles[l-1])
        self.rook_moved = deepcopy(self.list_of_rooks[l-1])
        self.white_king_check, self.black_king_check = self.list_of_king_check[l-1]
        self.white_king_moved, self.black_king_moved = self.list_of_king_moves[l-1]
        self.pion_passant = self.list_of_passant[l-1]

        self.selected_piece=[]
        self.draw_board()
        self.draw_pieces()
        self.turn = 'black' if self.turn == 'white' else 'white'
        pygame.display.flip()
        pygame.time.delay(100)


    def update_list_of_boards(self) : 
        l = self.len_list_of_boards
        # Ensure the list_of_boards contains independent deep copies of the board (3D list)
        if not np.array_equal(self.list_of_boards[l-1], self.chess_board):
            self.list_of_boards[l] = deepcopy(self.chess_board)
            self.list_of_times[l] = [self.white_time, self.black_time]
            self.list_of_last_moves[l] = deepcopy(self.last_move)
            self.list_of_castles[l] = deepcopy(self.castle)
            self.list_of_rooks[l] = deepcopy(self.rook_moved)
            self.list_of_king_check[l] = [self.white_king_check, self.black_king_check]
            self.list_of_king_moves[l] = [self.white_king_moved, self.black_king_moved]
            self.list_of_passant[l] = self.pion_passant
            self.len_list_of_boards += 1
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    
    def draw_move(self) : 
        if (self.game.last_move and self.game.last_move != self.game.last_move_draw) :
            self.game.last_move_draw = self.game.last_move
            x,y = self.last_move[0]
            mx,my = self.last_move[1]
            dx = (mx-x)/40
            dy = (my-y)/40
            piece = self.chess_board[my][mx]
            print(piece)
            if (piece != '--') :
                resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                for i in range(40):
                    self.draw_board()
                    self.draw_pieces(mx,my)
                    col = y + i * dy
                    row = x + i * dx
                    self.screen.blit(resized_piece, pygame.Rect(row * square_size, col * square_size, square_size, square_size))
                    pygame.time.delay(1)

                    
                    pygame.display.flip()
    def draw_pieces(self,mx=-1,my=-1):
        font = pygame.font.Font(None, 12)        
        for row in range(8):
            for col in range(8):
                text = font.render(self.chess_board_squares[col][row], True, (0, 0, 255)) 
                screen.blit(text, (row*square_size, col*square_size))
                piece = self.chess_board[row][col]
                if piece != '--' :
                        if (mx==col and my==row) :
                            continue 
                        resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                        self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
                        

    def draw_add_time_button(self):
        self.button_rect = pygame.Rect(screen_width + 20, 200, 250, 80)
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.button_rect)
        else:
            pygame.draw.rect(self.screen, black, self.button_rect)

        font = pygame.font.Font(None, 36)
        button_text = font.render('+ 5 seconds', True, white)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, text_rect)
   
    def handle_add_time_button(self):
        current_time = time.time()  # Get the current time
        
        if pygame.mouse.get_pressed()[0]: 
            # Check if the left mouse button is pressed
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                if (self.number_of_time_same_piece_clicked==0) :
                    self.number_of_time_same_piece_clicked=1
                    return 
                # Check if enough time has passed since the last click
                if current_time - self.last_click_time >= self.cooldown:
                    # Play click sound
                    click_sound_add_time_button.play()

                    if  self.turn== 'white':
                        self.black_time += 5  # Add 5 seconds to black's time
                    else:
                        self.white_time += 5  # Add 5 seconds to white's time

                    self.last_click_time = current_time  # Update the last click time fix this code so it gets to add time in the left mouse click

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)
        if (self.white_time<=5):
            white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, red)
        if (self.black_time<=5):
            black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, red)

        if (self.player=='white') :
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if (self.player=='black'):
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))
    def draw_king_in_check(self) :
        if (self.turn=='white') :
            self.white_king_position = self.find_king_position( 'white')
            x_king, y_king = self.white_king_position
            b = False
            for key in self.black_moves :
                if  (x_king,y_king) in self.black_moves[key] :
                    b = True
                    break
            self.white_king_check = b
            if self.white_king_check:
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
        else :
            self.black_king_position = self.find_king_position('black')
            x_king, y_king = self.black_king_position
            b = False
            for key in self.white_moves :
                if (x_king,y_king) in self.white_moves[key] :
                    b = True
                    break
            self.black_king_check = b
            if self.black_king_check:
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
    def draw_selected_piece(self) : 
        if self.selected_piece:
            x, y = self.selected_piece
            if self.turn[0] == self.chess_board[y][x][0]:  # Ensure selected piece belongs to current player
                pygame.draw.rect(self.screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                for mx, my in self.possible_moves:
                    pygame.draw.rect(self.screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def draw_last_move(self) :
        if len(self.last_move) > 1:
            x, y = self.last_move[0]
            mx, my = self.last_move[1]
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def run(self) :
        self.white_king_position = self.find_king_position( 'white')
        self.black_king_position = self.find_king_position('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Check if left click
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    """"  if (self.turn=='black') :
                            self.all_moves()
                            start,end = AI(self)
                            s(start,' this is start and end ',end)
                            self.last_move = [start,end]

                            self.move_piece(start,end[0],end[1])
                            if (start[0]==7 and start[1]==7) :
                                print('rook moved')
                            self.all_moves()
                            self.turn = 'white'"""
                    # Ensure within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if self.selected_piece and (x_square, y_square) in self.possible_moves:
                            self.all_moves()
                            self.is_king_in_check()
                            self.move_piece(self.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            self.last_move = [[self.selected_piece[0], self.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.x_king, self.y_king = -1, -1  # Reset king position
                            for i in range(8):
                                for j in range(8):
                                    check_pos = self.check(i, j)
                                   #"" if check_pos != [-1, -1]:  # Update if a check is found
                                    self.x_king, self.y_king = check_pos
                                    if (self.x_king !=-1) : 
                                        break 
                                if self.x_king != -1:
                                    break
                            self.change_player()
                            self.selected_piece, self.possible_moves = None, []
                        elif self.chess_board[y_square][x_square][0]==self.turn[0]:
                            self.selected_piece = (x_square, y_square)
                            self.castling()
                            self.all_moves()
                            if (self.turn=='white') : 
                                self.possible_moves = deepcopy(self.white_moves[(x_square, y_square)])  # Only get valid moves
                            else :
                                self.possible_moves = deepcopy(self.black_moves[(x_square, y_square)])  # Only get valid moves
        pygame.display.flip()
    def find_king_position(self, color):
        """Returns the position of the king for a given color."""
        for x in range(8):
            for y in range(8):
                piece = self.chess_board[y][x]
                if piece == f'{color[0]}K':  # White king or black king
                    return (x, y)
        return None


