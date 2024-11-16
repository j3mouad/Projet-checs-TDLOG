import pygame
import sys
from copy import deepcopy
import time
from random import shuffle
import pieces
# Initialization de Pygame
pygame.init()
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")  # Ensure you have a click.wav file in the same directory
click_sound_chess=pygame.mixer.Sound("chess_move_soundf.mp3")
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
pygame.display.set_caption("Chess")
# Colors
white = (255, 255, 255)
grey=(128,128,128)
red = (255,0,0)
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 200, 100)  #green
button_hover_color = (150, 250, 150)  
selected_piece=None

# Taille de la case
square_size = screen_width // 8

# Charger les images des pièces
pieces_images = {
    'bR': pygame.image.load('black_rook.png'),
    'bN': pygame.image.load('black_knight.png'),
    'bB': pygame.image.load('black_bishop.png'),
    'bQ': pygame.image.load('black_queen.png'),
    'bK': pygame.image.load('black_king.png'),
    'bP': pygame.image.load('black_pawn.png'),
    'wR': pygame.image.load('white_rook.png'),
    'wN': pygame.image.load('white_knight.png'),
    'wB': pygame.image.load('white_bishop.png'),
    'wQ': pygame.image.load('white_queen.png'),
    'wK': pygame.image.load('white_king.png'),
    'wP': pygame.image.load('white_pawn.png')
}

class ChessGame:
    def __init__(self):
        self.screen = screen
        self.chess_board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.chess_board_squares = [
    ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
    ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
    ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
    ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
    ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
    ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
    ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
    ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
    ]
        
        self.list_of_boards=[self.chess_board for _ in range(10000)]
        self.len_list_of_boards=0 
        self.list_of_times=[[0,0] for _ in range(10000)]
        self.turn = 'white'
        self.player='white'
        self.last_move=[]
        self.winner = None
        self.cooldown=0.2
        self.white_time = -1  # 10 minutes en secondes
        self.black_time = -1
        self.white_king_moved=False
        self.black_king_moved=False
        self.initial_white_time = self.white_time
        self.initial_black_time = self.black_time
        self.last_time_update = pygame.time.get_ticks()
        self.running = True
        self.x_square_clicked=None
        self.y_square_clicked=None
        self.number_of_time_same_piece_clicked= 0
        self.last_click_time=0
        self.is_back_button_pressed=0
        self.white_king_check=False
        self.black_king_check=False
        self.classic=True
        self.selected_piece=[]
        self.pion_passant=False
        self.last_time_back_clicked=0
    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    def draw_pieces(self):
        font = pygame.font.Font(None, 12)

        for row in range(8):
            for col in range(8):
                text = font.render(self.chess_board_squares[col][row], True, (0, 0, 255)) 
                screen.blit(text, (row*square_size, col*square_size))
                piece = self.chess_board[row][col]
                if piece != '--':
                    resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                    self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
                    

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)

        pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
        self.screen.blit(white_timer_surface, (screen_width + 20, 450))
        self.screen.blit(black_timer_surface, (screen_width + 20, 50))

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
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.button_rect.collidepoint(mouse_pos):
                if self.turn == 'white':
                    self.black_time += 5
                else:
                    self.white_time += 5

    
    def display_rematch_button(self, window, font, button_x=50, button_y=100, button_width=200, button_height=50):
        self.rematch_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_current = white if not self.rematch_button_rect.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(window, button_color_current, self.rematch_button_rect)

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
                        print("Added 5 seconds to black's time.")
                    else:
                        self.white_time += 5  # Add 5 seconds to white's time
                        print("Added 5 seconds to white's time.")

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
    def game_ends(self):
        if (self.white_time<=0 ):
            self.running=False
            self.winner = 'black'
            return True
        if (self.black_time<=0):
            self.running = False
            self.winner = 'white'
            return True
        return False
    def flip_board(self):
        L= [[self.chess_board[i][j] for j in range(8)] for i in range(7,-1,-1)]
        self.chess_board=deepcopy(L)
    def show_winner(self):
        self.game_ends()
        if (self.running):
            return 
        screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        winner = self.winner
        screen.fill(white)
        font = pygame.font.Font(None, 48)
        winner_text = font.render(f'{winner} a gagné!', True, black)
        screen.blit(winner_text, (50, 50))
        self.display_rematch_button(screen, font)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rematch_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        waiting = False
                        return
        pygame.quit()
        sys.exit()

    def display_rematch_button(self, window, font, button_x=50, button_y=100, button_width=200, button_height=400):
        self.rematch_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_current = white if not self.rematch_button_rect.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(window, button_color_current, self.rematch_button_rect)

        rematch_text = font.render("Rejouer", True, black)
        text_x = button_x + (button_width - rematch_text.get_width()) // 2
        text_y = button_y + (button_height - rematch_text.get_height()) // 2
        window.blit(rematch_text, (text_x, text_y))
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
        print("Back button clicked!")
        self.last_time_back_clicked = time
        self.len_list_of_boards-=1
        l=self.len_list_of_boards
        self.white_time, self.black_time = self.list_of_times[l - 1]
        self.chess_board = deepcopy(self.list_of_boards[l - 1])
        #self.selected_piece=[]
        self.draw_board()
        self.draw_pieces()
        self.last_move=[]
        self.turn = 'black' if self.turn == 'white' else 'white'
        pygame.display.flip()
        pygame.time.delay(100)


    def choose_game(self):
        window = pygame.display.set_mode((screen_width + added_screen_width, screen_height),pygame.RESIZABLE)
        pygame.display.set_caption("Let's play Chess!")
        font = pygame.font.Font(None, 28)
        text = font.render("Choose color and time ", True, black)
        window.blit(text, (50, 50))
        
        button_width = 250
        button_height = 50
        button_margin = 20
        button_x = 50
        button_y = 100

        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_2v2 = pygame.Rect(button_x+button_width+20, button_y +  (button_height + button_margin), button_width, button_height)
        button_random=pygame.Rect(button_x, button_y+4*button_height, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_rapid = pygame.Rect(button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_classic = pygame.Rect(button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_blitz = pygame.Rect(button_x + button_width+40 , button_y + 2 * (button_height + button_margin), button_width/2, button_height)
        first_choosing=True
        second_choosing = True
        white_time=0
        black_time=0
        while first_choosing or second_choosing:
            mouse_pos = pygame.mouse.get_pos()
            window.fill(white)
            window.blit(text, (50, 50))

            pygame.draw.rect(window, white if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, white if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)

            black_text = font.render("Black pieces", True, black)
            white_text = font.render("White pieces", True, black)
            window.blit(black_text, (button_x + 10, button_y + 10))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))

            pygame.draw.rect(window, grey if not button_2v2.collidepoint(mouse_pos) else button_hover_color, button_2v2)
            pygame.draw.rect(window, grey if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, grey if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            pygame.draw.rect(window, grey if not button_rapid.collidepoint(mouse_pos) else button_hover_color, button_rapid)
            pygame.draw.rect(window, grey if not button_classic.collidepoint(mouse_pos) else button_hover_color, button_classic)
            pygame.draw.rect(window, grey if not button_blitz.collidepoint(mouse_pos) else button_hover_color, button_blitz) 
            pygame.draw.rect(window, grey if not button_random.collidepoint(mouse_pos) else button_hover_color, button_random)


            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            classic_text = font.render("Jeu classic",True,black) 
            blitz_text = font.render("Jeu blitz",True,black)
            rapid_text= font.render("Jeu rapid",True,black)
            twovtwo_text = font.render("Jeu 2v2",True,black)
            random_text=font.render("Jeu de Fisher",True,black)
            window.blit(black_text, (button_x + 10, button_y + (button_height - black_text.get_height()) // 2))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + (button_height - white_text.get_height()) // 2))
            window.blit(classic_text, (button_x + button_width / 2 + button_margin + 10, button_y + 2 * (button_height + button_margin) + (button_height - classic_text.get_height()) // 2))
            window.blit(rapid_text, (button_x +10 , button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(blitz_text, (button_x + 50+button_width, button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(random_text, (button_x +50, button_y + 4 * (button_height) + (button_height - random_text.get_height()) // 2))
            window.blit(twovtwo_text, (button_x+button_width+30, button_y +  (button_height + button_margin) + (button_height - random_text.get_height()) // 2))

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_black.collidepoint(event.pos):
                        first_choosing = False
                        self.turn = 'black'
                        self.flip_board()
                    
                    elif button_white.collidepoint(event.pos):
                        first_choosing = False
                        self.player = 'white'
                    elif button_classic.collidepoint(event.pos) :
                        second_choosing=False
                        self.time_reg(3600,3600)
                        white_time=3600
                        black_time=3600
                    elif button_rapid.collidepoint(event.pos) : 
                        second_choosing=False
                        self.time_reg(600,600)
                        white_time=600
                        black_time=600
                        self.classic=False
                    elif button_blitz.collidepoint(event.pos) :
                        second_choosing = False
                        self.time_reg(60,60)
                        white_time=60
                        black_time=60
                    elif button_random.collidepoint(event.pos) :
                        shuffle(self.chess_board[0])
                        shuffle(self.chess_board[7])
                    elif  button_2v2.collidepoint(event.pos) : 
                        first_choosing = False
                        self.player = 'white'
        self.list_of_boards[0]=[self.chess_board]
        self.len_list_of_boards+=1
        return (white_time,black_time)    

    def change_player(self) :
        if (self.turn=='white') :
            self.turn='black'
        else :
            self.turn='white'

    def update_timers(self):

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) // 1000

        if elapsed_time > 0:
            if self.turn == 'white':
                self.white_time -= elapsed_time
            else:
                self.black_time -= elapsed_time
            self.last_time_update = current_time

        if self.white_time <= 0 or self.black_time <= 0:
            self.winner = "black" if self.white_time <= 0 else "white"

    def is_valid_move(self, start, end):
            x, y = start
            mx, my = end
            start_piece = self.chess_board[y][x]
            end_piece = self.chess_board[my][mx]
            # Check if piece belongs to the current player and destination is not occupied by own piece
            if start_piece == '--' or (end_piece[0] == start_piece[0]):
                return False

            piece_type = start_piece[1]

            # Pawn moves
            if piece_type == 'P':
                direction = -1 if start_piece[0] == 'w' else 1  # White pawns move up (-1), black pawns move down (+1)
                if mx == x:  # Moving straight
                    if my == y + direction and end_piece == '--':  # Single step forward
                        return True
                    if (y == 1 or y == 6) and my == y + 2 * direction and end_piece == '--' and \
                            self.chess_board[y + direction][x] == '--':  # Double step from start row
                        return True
                elif abs(mx - x) == 1 and my == y + direction:
                    if end_piece != '--':  # Capture move
                        return True
                    # En passant capture
                    elif (y == 3 and start_piece[0] == 'w') or (y == 4 and start_piece[0] == 'b'):
                        last_move = self.last_move  # Store last move as (start, end) coordinates
                        
                        if last_move and self.chess_board[last_move[1][1]][last_move[1][0]][1] == 'P':
                            
                            if abs(last_move[1][0] - mx) == 0 and last_move[1][1] == y and \
                                    self.chess_board[last_move[1][1]][last_move[1][0]]=='bP' :
                                self.pion_passant=True
                                return True

            # Rook moves
            elif piece_type == 'R':
                if x == mx or y == my:  # Horizontal or vertical move
                    step_x = 1 if mx > x else -1 if mx < x else 0
                    step_y = 1 if my > y else -1 if my < y else 0
                    for i in range(1, max(abs(mx - x), abs(my - y))):
                        if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                            return False
                    return True

            # Knight moves
            elif piece_type == 'N':
                if (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2):
                    return True

            # Bishop moves
            elif piece_type == 'B':
                if abs(mx - x) == abs(my - y):  # Diagonal move
                    step_x = 1 if mx > x else -1
                    step_y = 1 if my > y else -1
                    for i in range(1, abs(mx - x)):
                        if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                            return False
                    return True

            # King moves (including castling)
            elif piece_type == 'K':
                if max(abs(mx - x), abs(my - y)) == 1:  # One square in any direction
                    return True
                
                # Castling move
                

            # Queen moves
            elif piece_type == 'Q':
                if abs(mx - x) == abs(my - y) or x == mx or y == my:  # Diagonal, horizontal, or vertical move
                    step_x = 1 if mx > x else -1 if mx < x else 0
                    step_y = 1 if my > y else -1 if my < y else 0
                    for i in range(1, max(abs(mx - x), abs(my - y))):
                        if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                            return False
                    return True

            return False

    def get_possible_moves(self, x, y):
        """Returns moves for the piece at (x, y) that don't put its king in check."""
        moves = []


        # Check all potential moves
        for my in range(8):
            for mx in range(8):
                if self.is_valid_move((x, y), (mx, my)):
                    
                    moves.append((mx, my))
        return moves


    def move_piece(self, start, x, y): 
        """Moves the piece from start to (x, y). Handles en passant captures."""
        mx, my = start
        moving_piece = self.chess_board[my][mx]
        if (self.chess_board[my][mx][1]=='K') :
            color = self.chess_board[my][mx][0] 
            if (color=='w') :
                self.white_king_moved=True
            else :
                self.black_king_moved=True
        # Move the piece from start to (x, y)
        self.chess_board[y][x], self.chess_board[my][mx] = moving_piece, '--'

        # Handle en passant capture
        if (self.pion_passant) :
            # Clear the square of the pawn captured via en passant
            
            self.chess_board[y+1][x] = '--'
            
        
            # Reset en passant if no double-step pawn move occurred
        self.pion_passant = False

    def back_move_piece(self, start, x, y, piece): 
        """Reverts a move to restore board state."""
        mx, my = start
        self.chess_board[y][x], self.chess_board[my][mx] = self.chess_board[my][mx], piece

    def is_king_in_check(self):
        """Checks if the player's king is in check."""
        color=self.turn[0]
        #print(color)
        king_position = self.get_king_position()
        if not king_position:
            # King not found, possibly captured
            self.running=False
            self.winner = 'black' if color=='w' else 'white'
            
            return True

        x_king, y_king = king_position
        opponent_color = 'b' if color == 'w' else 'w'
        # Check if any opponent piece can capture the king's position
        for y in range(8):
            for x in range(8):
                piece = self.chess_board[y][x]
                if piece[0] == opponent_color :
                    self.turn
                    if self.is_valid_move((x, y), (x_king, y_king)):
                        print('in_check')
                        self.turn='black' if self.turn=='white' else 'black'
                        return True

        return False

    def simulate_move_and_check(self, start, end):
        """Simulates a move and checks if it puts the player's king in check."""
        piece = self.chess_board[start[1]][start[0]]
        target_piece = self.chess_board[end[1]][end[0]]
        
        # Make the move temporarily
        self.chess_board[end[1]][end[0]] = piece
        self.chess_board[start[1]][start[0]] = "--"
        # Check if the king is in check after the move
        in_check = self.is_king_in_check()

        # Undo the move
        self.chess_board[start[1]][start[0]] = piece
        self.chess_board[end[1]][end[0]] = target_piece

        return  not in_check

    def get_valid_moves(self, x_square, y_square):
        """Returns a list of valid moves that do not put the player's own king in check."""
        possible_moves = self.get_possible_moves(x_square, y_square)
        valid_moves = [move for move in possible_moves if self.simulate_move_and_check((x_square, y_square), move)]
        return valid_moves

    def check(self, x_square, y_square):
        """Checks if the move puts the opponent's king in check."""
        moves = self.get_valid_moves(x_square, y_square)
        opponent_color = 'b' if self.turn[0] == 'w' else 'w'
        opponent_king = opponent_color + 'K'

        for move in moves:
            if self.chess_board[move[1]][move[0]] == opponent_king:
                return move  # Returns the position of the king in check

        return [-1, -1]
    def get_king_position(self):
        """Finds and returns the position of the king of the given color."""
        color = self.turn[0]
       # print(color)
        king = color + 'K'
        for y in range(8):
            for x in range(8):
                if self.chess_board[y][x] == king:
                    return (x, y)
        return None