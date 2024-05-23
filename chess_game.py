import pygame
import sys
import chess_board

# Initialize Pygame
pygame.init()

# Set up the window size and load the board
square_size = 100
board_size = square_size * 8
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption('Two-click Chess Movement')

# Create a chess board using white and gray squares
board = pygame.Surface((board_size, board_size))
white_color = (255, 255, 255)
gray_color = (128, 128, 128)
square_size = board_size // 8

for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            pygame.draw.rect(board, white_color, (col * square_size, row * square_size, square_size, square_size))
        else:
            pygame.draw.rect(board, gray_color, (col * square_size, row * square_size, square_size, square_size))

# Initial positions (0-based indices for rows and columns)
rook_position = (1, 0)

def draw_pieces(fen_string: str):
    # Mapping of FEN characters to image paths
    piece_images = {
        'r': 'pngs/black-rook.png',
        'n': 'pngs/black-knight.png',
        'b': 'pngs/black-bishop.png',
        'q': 'pngs/black-queen.png',
        'k': 'pngs/black-king.png',
        'p': 'pngs/black-pawn.png',
        'R': 'pngs/white-rook.png',
        'N': 'pngs/white-knight.png',
        'B': 'pngs/white-bishop.png',
        'Q': 'pngs/white-queen.png',
        'K': 'pngs/white-king.png',
        'P': 'pngs/white-pawn.png'
    }
    
    # Clear the board
    screen.blit(board, (0, 0))
    
    # Split the FEN string into its components
    # print(f"FEN String: {fen_string}")
    fen_parts = fen_string.split(' ')
    board_state = fen_parts[0]
    # active_color = fen_parts[1]
    
    # Calculate the size of each square
    square_size = board_size // 8
    
    # Loop through each character in the board state
    row = 0
    col = 0
    for char in board_state:
        if char == '/':
            # Move to the next row
            row += 1
            col = 0
        elif char.isdigit():
            # Skip empty squares
            col += int(char)
        else:
            # Get the image path for the piece
            image_path = piece_images[char]
            # Load and scale the image
            piece_image = pygame.image.load(image_path)
            piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
            # Draw the piece on the board
            screen.blit(piece_image, (col * square_size, row * square_size))
            col += 1
    # Update the display
    pygame.display.flip()

def place_green_squares(locations):
    for location in locations:
        row, col = location
        pygame.draw.rect(board, (0, 255, 0), (col * square_size, row * square_size, square_size, square_size))

def clear_green_squares():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(board, white_color, (col * square_size, row * square_size, square_size, square_size))
            else:
                pygame.draw.rect(board, gray_color, (col * square_size, row * square_size, square_size, square_size))

# Variables to handle the two-click movement
selected_piece = None
selected_position = None

# Main loop
fen_string = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
chessboard = chess_board.ChessBoard()
running = True
while running:
    for event in pygame.event.get():
        # print(f"FEN String: {fen_string}")
        draw_pieces(fen_string)
        chessboard.process_fen_string(fen_string)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_y // square_size
            clicked_col = mouse_x // square_size

            if selected_piece is None:
                # First click: select a piece if it's at the clicked position
                piece = chessboard.get_piece(clicked_row, clicked_col)
                # print(f"Piece: {piece} at row: {clicked_row} and col: {clicked_col}")
                if piece is not None and piece.color == chessboard.active_color:
                    available_moves = piece.get_available_moves()
                    print(f"Available moves: {available_moves}")
                    place_green_squares(available_moves)
                    pygame.display.flip()

                if piece is not None:
                    selected_piece = piece
                    selected_position = (clicked_row, clicked_col)
            else:
                # Second click: move the piece to the clicked position
                clear_green_squares()
                chessboard.handle_moves(selected_position[0], selected_position[1], clicked_row, clicked_col)
                fen_string = chessboard.get_fen_string()
                print(f"FEN String: {fen_string}")
                selected_piece = None
                selected_position = None
                pygame.display.flip()

pygame.quit()
sys.exit()