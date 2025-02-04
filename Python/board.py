import pygame
from copy import deepcopy
import time
from random import shuffle
from utils import *
from button import Button
from ai import AI,AI_hard,evaluate
from config import *
from chess_game import find_king_position
# Initialize Pygame
pygame.init()
class Board:
    def __init__(self, game, screen):
        """
        Initializes a chess board with game data, screen size, and other properties.

        This class manages the game board, including rendering, tracking game state, 
        and handling user interactions.

        Parameters:
        game (Game): The game instance containing the game state.
        screen (pygame.Surface): The surface for rendering the game.

        Attributes:
        screen (pygame.Surface): The surface where the game is displayed.
        game (Game): The game instance managing the chess logic.
        cooldown (float): Time delay to prevent rapid piece selection.
        number_of_time_same_piece_clicked (int): Counter for consecutive clicks on the same piece.
        last_click_time (float): Timestamp of the last click event.
        screen_width (int): Width of the game window.
        screen_height (int): Height of the game window.
        x_square_size (int): Width of a single chess square.
        y_square_size (int): Height of a single chess square.
        score (int): The evaluation score of the board position.
        """
        self.screen = screen
        pygame.display.set_caption("Chess")
        self.screen = screen
        self.game = game
        self.cooldown = 0.5
        self.number_of_time_same_piece_clicked = 0
        self.last_click_time = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_square_size = screen_width // 16
        self.y_square_size = screen_height // 8
        self.score = evaluate(self.game, {})


    def draw_board(self):
        """
        Draws the chessboard on the screen.

        The chessboard is an 8x8 grid where each square is drawn as a rectangle.
        The color of each square alternates between light brown and brown, following 
        the standard pattern for a chessboard. The squares are drawn using the 
        `pygame.draw.rect` function.

        This method does not return any value.
        """
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                square = Button("",col*self.x_square_size,row*self.y_square_size,self.x_square_size,self.y_square_size,image_path = None,color = color)
                square.draw(self.screen)
        

    def draw_move(self):
        """
            This method animates the movement of a chess piece from its original 
            position to its new position based on the last move made in the game. 
            The animation is done by interpolating the piece's position in small 
            steps and redrawing the board and pieces at each step.

            Preconditions:
            - `self.game.last_move` is a tuple containing the starting and ending 
              coordinates of the last move.
            - `self.game.last_move_draw` is used to track the last move that was 
              drawn to avoid redrawing the same move.
            - `self.game.chess_board` is a 2D list representing the current state 
              of the chess board.
            - `pieces_images` is a dictionary mapping piece identifiers to their 
              corresponding images.
            - `self.x_square_size` and `self.y_square_size` are the dimensions of 
              each square on the board.
            - `self.screen` is the Pygame display surface.

            Post conditions:
            - The board and pieces are redrawn with the piece moved to its new 
              position.
            - The move animation is displayed on the screen.

            Note:
            - The method uses Pygame for rendering and animating the movement.
            - The animation consists of 5 steps, with a short delay between each 
              step to create a smooth transition.
        """
        if (self.game.last_move and self.game.last_move != self.game.last_move_draw):
            self.game.last_move_draw = self.game.last_move
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            dx = (mx - x) / 5
            dy = (my - y) / 5
            piece = self.game.chess_board[my][mx]
            if (piece != '--'):
                resized_piece = pygame.transform.scale(pieces_images[piece], (self.x_square_size, self.y_square_size))
                for i in range(1,6):
                    self.draw_board()
                    self.draw_pieces(mx, my)
                    col = y + i * dy
                    row = x + i * dx
                    self.screen.blit(resized_piece, pygame.Rect(row * self.x_square_size, col * self.y_square_size, self.x_square_size, self.y_square_size))
                    pygame.time.delay(1)
                    pygame.display.flip()

    def draw_pieces(self, mx=-1, my=-1):
        """
            Parameters:
            mx (int): The x-coordinate of the mouse position. Default is -1.
            my (int): The y-coordinate of the mouse position. Default is -1.

            This function iterates over the chess board and draws each piece on the screen.
            If a piece is located at the mouse position (mx, my), it will not be drawn.
            The pieces are resized to fit the square size of the board.
        """
        font = pygame.font.Font(None, 12)
        for row in range(8):
            for col in range(8):
                text = font.render(self.game.chess_board_squares[col][row], True, (0, 0, 255)) 
                self.screen.blit(text, (row * self.x_square_size, col * self.y_square_size))
                piece = self.game.chess_board[row][col]
                if piece != '--':
                    if (mx == col and my == row):
                        continue 
                    resized_piece = pygame.transform.scale(pieces_images[piece], (self.x_square_size , self.y_square_size ))
                    self.screen.blit(resized_piece, pygame.Rect(col * self.x_square_size, row * self.y_square_size, self.x_square_size, self.y_square_size))
    def draw_add_time_button(self):
        """
        Draws the 'Add Time' button on the screen using the Button class.

        This method uses the Button class to create and manage a button 
        that allows the user to add 5 seconds to the opponent's timer.

        Returns:
            None
        """
        # Create the button instance
        self.add_time_button = Button(
            text="+ 5 seconds",
            x=self.screen_width//2 + self.x_square_size,
            y=self.screen_height//2-self.y_square_size,
            width=3*self.x_square_size,
            height=self.y_square_size,
            color=grey

        )
        self.add_time_button.draw(self.screen,size = int(square_size//3))

        

    def handle_add_time_button(self,event):
        
        """Adds 5 seconds to the current player's time when the 'Add Time' button is clicked, 
        ensuring a cooldown period between clicks.

        Parameters:
        event (pygame.event): The event triggered by the button click.
        """
        current_time = time.time()
        if self.add_time_button.is_clicked(event) and current_time - self.last_click_time >= self.cooldown:
            click_sound_add_time_button.play()
            if self.game.turn == 'white':
                self.game.black_time += 5
            else:
                self.game.white_time += 5

            self.last_click_time = current_time


    def draw_timer(self):
        """
        Draws the timers for both players.

        This method displays the countdown timers for the white and black players, updating 
        them in minutes and seconds format. If a player's time is below 5 seconds, their 
        timer is displayed in red. The timers are drawn on the screen depending on whose 
        turn it is.

        Returns:
            None
        """
        self.screen.fill(white)
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.game.white_time // 60}:{self.game.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.game.black_time // 60}:{self.game.black_time % 60:02}', True, black)
        if self.game.white_time <= 5:
            white_timer_surface = font.render(f'White: {self.game.white_time // 60}:{self.game.white_time % 60:02}', True, red)
        if self.game.black_time <= 5:
            black_timer_surface = font.render(f'Black: {self.game.black_time // 60}:{self.game.black_time % 60:02}', True, red)

        # Clear the right half of the screen for the timer area
        pygame.draw.rect(self.screen, white, (self.screen_width // 2, 0, self.screen_width // 2, self.screen_height))

        # Correct the timer surface positions
        white_timer_position = (self.screen_width // 2 + self.x_square_size // 2, self.screen_height - self.y_square_size)
        black_timer_position = (self.screen_width // 2 + self.x_square_size // 2, self.y_square_size)

        self.screen.blit(white_timer_surface, white_timer_position)
        self.screen.blit(black_timer_surface, black_timer_position)

    def draw_move_back_button(self):
        """
        Draws the 'Back' button on the screen using the Button class.

        This method uses the Button class to create and manage a button 
        that allows the player to undo the last move.

        Returns:
            None
        """
        # Create the button instance
        self.back_button = Button(
            text="Back",
            x=self.screen_width//2 + 2*self.x_square_size,
            y=self.screen_height//2+self.y_square_size,
            width=self.x_square_size ,
            height=int(self.y_square_size),
        )

        # Draw the button
        self.back_button.draw(self.screen, size = int(self.x_square_size)//4)

        # Handle button click
       

    def handle_back_button_click(self, event):
        """
        Handles the logic when the 'Back' button is clicked.

        This method restores the game state to the previous one if available, adhering to a cooldown
        to prevent rapid triggers. It also redraws the game UI to reflect the restored state.

        Returns:
            None
        """
        # Enforce cooldown to prevent rapid triggers

        current_time = pygame.time.get_ticks()
        if (current_time - self.game.last_time_back_clicked) <= self.cooldown:
            return

        # Check if a previous state is available
        if self.game.len_list_of_boards == 0:
            return

        # Update cooldown tracker
        if (self.back_button.is_clicked(event)) :
            self.game.last_time_back_clicked = current_time

            # Revert to the previous state
            self.game.len_list_of_boards -= 1
            previous_index = self.game.len_list_of_boards

            # Restore game attributes
            self.game.white_time, self.game.black_time = self.game.list_of_times[previous_index - 1]
            self.game.chess_board = deepcopy(self.game.list_of_boards[previous_index - 1])
            self.game.last_move = self.game.list_of_last_moves[previous_index - 1]
            self.game.castle = deepcopy(self.game.list_of_castles[previous_index - 1])
            self.game.rook_moved = deepcopy(self.game.list_of_rooks[previous_index - 1])
            self.game.white_king_check, self.game.black_king_check = self.game.list_of_king_check[previous_index - 1]
            self.game.white_king_moved, self.game.black_king_moved = self.game.list_of_king_moves[previous_index - 1]
            self.game.pion_passant = self.game.list_of_passant[previous_index - 1]
            self.game.selected_piece = []

            # Redraw game board and pieces
            
            self.draw_board()
            self.draw_pieces()

            # Toggle the turn
            self.game.turn = 'black' if self.game.turn == 'white' else 'white'

            # Update the display
            pygame.display.flip()

            # Add a short delay for smooth transition
            pygame.time.delay(100)

    def update_timers(self):
        """
        Updates the timers for both players based on the elapsed time since the last update.

        Modifies:
        - self.game.white_time (int): Decreases the white player's time.
        - self.game.black_time (int): Decreases the black player's time.
        - self.game.last_time_update (int): Updates the last time the timer was checked.
        Returns:
            None
        """
        current_time = pygame.time.get_ticks()

        elapsed_time = (current_time - self.game.last_time_update) // 1000
        if elapsed_time > 0:
            if self.game.turn == 'white':
                    self.game.white_time -= elapsed_time
                    self.game.last_time_update = current_time

            else:
                self.game.black_time -= elapsed_time
                self.game.last_time_update = current_time
    def draw_king_in_check(self):
        """
        Draws a red square around the current player's king if it is in check.
        The function checks if the king is threatened by any opponent's piece.
        Returns:
            None
        """
        if (self.game.turn == 'white'):
            self.game.white_king_position = find_king_position(self.game.chess_board,'white')
            x_king, y_king = self.game.white_king_position
            b = False
            # Check if the white king is in check by any black piece
            for key in self.game.black_moves:
                if (x_king, y_king) in self.game.black_moves[key]:
                    b = True
                    break
            self.game.white_king_check = b
            # If white king is in check, draw a red square around its position
            if self.game.white_king_check:
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * self.x_square_size, y_king * self.y_square_size, self.x_square_size, self.y_square_size))
        else:
            self.game.black_king_position = find_king_position(self.game.chess_board,'black')
            x_king, y_king = self.game.black_king_position
            b = False
            # Check if the black king is in check by any white piece
            for key in self.game.white_moves:
                if (x_king, y_king) in self.game.white_moves[key]:
                    b = True
                    break
            self.game.black_king_check = b
            # If black king is in check, draw a red square around its position
            if self.game.black_king_check:
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * self.x_square_size, y_king * self.y_square_size, self.x_square_size, self.y_square_size))

    def draw_selected_piece(self):
        """
        Draws a grey square around the currently selected piece and its possible moves.
        The function ensures that the selected piece belongs to the current player and highlights its valid moves.
        Returns:
            None    
        """
        if self.game.selected_piece:
            x, y = self.game.selected_piece
            # Ensure the selected piece belongs to the current player
            if self.game.turn[0] == self.game.chess_board[y][x][0]:
                # Highlight the selected piece
                pygame.draw.rect(self.screen, grey, pygame.Rect(x * self.x_square_size, y * self.y_square_size, self.x_square_size, self.y_square_size))
                # Highlight all possible valid moves of the selected piece
                for mx, my in self.game.possible_moves:
                    pygame.draw.rect(self.screen, grey, pygame.Rect(mx * self.x_square_size, my * self.y_square_size, self.x_square_size, self.y_square_size))
    def draw_last_move(self):
        """
        Highlights the squares involved in the last move.
        It draws a special color on the starting and ending positions of the last move.
        Returns:
            None
        """
        if len(self.game.last_move) > 1:
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            # Highlight the starting and ending squares of the last move
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(x * self.x_square_size, y * self.y_square_size, self.x_square_size, self.y_square_size))
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(mx * self.x_square_size, my * self.y_square_size, self.x_square_size, self.y_square_size))
    def update_moves(self) :
        """updates all moves"""
        self.game.castling()
        self.game.all_moves()
        self.game.change_player()
        self.game.castling()
        self.game.all_moves()
        self.game.change_player()
    def draw_score(self) :
    
        """Draws the score button on the screen with the current score displayed.

        Creates and draws a button with the current score at a specific position.
        Returns:
            None
        """
        self.score_button = Button(
            text="score : " + str(self.score),
            x=self.screen_width//2 + 4*self.x_square_size,
            y=self.screen_height//2+self.y_square_size,
            width=self.x_square_size ,
            height=int(self.y_square_size),
        )

        # Draw the button
        self.score_button.draw(self.screen, size = int(self.x_square_size)//4)

    def update_score(self) :
        """Updates the score by evaluating the current state of the game.
        Modifies:
        - self.score (int): The current score based on the game state.
        Returns:
            None
        """
        self.score = evaluate(self.game,{})
    def update_screen(self) :
        """Updates the screen to reflect the current game screen.
         Modifies:
        - self.game.screen: Sets the current screen to the updated screen.
        Returns:
            None
        """
        self.game.screen= self.screen
    def handle_reisze(self,event) :
        # Mettre à jour la taille de l'écran
        # Update screen size to the event's size directly
        self.screen_width, self.screen_height = max(event.w, 100), max(event.h, 100)  # Minimum size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.x_square_size = int(self.screen_width / 16)
        self.y_square_size = int(self.screen_height / 8)

    def run(self):
        """
        Main game loop. Handles player input, updates the game state, 
        checks for check conditions, and alternates turns.
        Returns:
            None
        """

        self.game.white_king_position = find_king_position(self.game.chess_board,'white')
        self.game.black_king_position = find_king_position(self.game.chess_board,'black')
        
        for event in pygame.event.get():
            self.handle_add_time_button(event)
            self.handle_back_button_click( event)
            if (self.game.player) :
                if (self.game.white and self.game.turn == 'black') :
                            self.game.all_moves()
                            if (self.game.hard) :
                                start,end = AI_hard(self.game)
                            else :
                                start,end = AI(self.game)
                            x,y = start 
                            mx,my = end 
                            self.game.move_piece(start,end[0],end[1])
                            self.game.last_move = [start,end]
                            self.draw_last_move()
                            self.update_timers()
                            self.game.change_player()
                            self.game.all_moves()
                if (self.game.black and self.game.turn=='white') :
                            self.game.all_moves()
                            if (self.game.hard) :
                                start,end = AI_hard(self.game)
                            else :
                                start,end = AI(self.game)
                            x,y = start 
                            mx,my = end 
                            self.game.move_piece(start,mx,my)
                            self.game.last_move = [start,end]
                            self.draw_last_move()
                            self.update_timers()
                            self.game.change_player()
                            self.game.all_moves()

            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_reisze(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click check
                    x, y = event.pos
                    x_square, y_square = int(x // self.x_square_size), int(y // self.y_square_size)
                    # Ensure the clicked position is within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if (x_square,y_square) == (self.game.selected_piece) :
                            continue
                        if (self.game.selected_piece and (x_square,y_square) not in self.game.possible_moves) :
                            self.game.selected_piece = None
                            self.game.possible_moves = []
                        if self.game.selected_piece and (x_square, y_square) in self.game.possible_moves:
                            #self.game.all_moves()
                            #self.game.is_king_in_check()
                            self.game.move_piece(self.game.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            # Update last move
                            self.game.last_move = [[self.game.selected_piece[0], self.game.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.game.update_list_of_boards()
                            
                            self.game.change_player()
                            self.update_moves()
                            self.game.selected_piece, self.game.possible_moves = None, []  # Reset selected piece and possible moves
                        
                        elif self.game.chess_board[y_square][x_square][0] == self.game.turn[0]:

                            # Select a piece if it belongs to the current player
                            self.game.selected_piece = (x_square, y_square)
                           # self.game.castling()
                           # self.game.all_moves()
                            self.game.is_king_in_check()
                            if self.game.turn == 'white':
                                self.game.possible_moves = deepcopy(self.game.white_moves[(x_square, y_square)])
                            else:
                                self.game.possible_moves = deepcopy(self.game.black_moves[(x_square, y_square)])

        
        pygame.display.flip()
       