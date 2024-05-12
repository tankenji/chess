import pygame
import sys
import chess

# Initialize Pygame
pygame.init()

# Set up the window size and load the board
square_size = 100
board_size = square_size * 8
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption('Two-click Chess Movement')

# Load board and chess piece images
board = pygame.image.load('pngs/rect-8x8.png')
board = pygame.transform.scale(board, (board_size, board_size))

# # White chess pieces
# white_rook = pygame.image.load('pngs/white-rook.png')
# white_rook = pygame.transform.scale(white_rook, (square_size, square_size))
# white_king = pygame.image.load('pngs/white-king.png')
# white_king = pygame.transform.scale(white_king, (square_size, square_size))
# white_queen = pygame.image.load('pngs/white-queen.png')
# white_queen = pygame.transform.scale(white_queen, (square_size, square_size))
# white_bishop = pygame.image.load('pngs/white-bishop.png')
# white_bishop = pygame.transform.scale(white_bishop, (square_size, square_size))
# white_knight = pygame.image.load('pngs/white-knight.png')
# white_knight = pygame.transform.scale(white_knight, (square_size, square_size))
# white_pawn = pygame.image.load('pngs/white-pawn.png')
# white_pawn = pygame.transform.scale(white_pawn, (square_size, square_size))

# # Black chess pieces
# black_rook = pygame.image.load('pngs/black-rook.png')
# black_rook = pygame.transform.scale(black_rook, (square_size, square_size))
# black_king = pygame.image.load('pngs/black-king.png')
# black_king = pygame.transform.scale(black_king, (square_size, square_size))
# black_queen = pygame.image.load('pngs/black-queen.png')
# black_queen = pygame.transform.scale(black_queen, (square_size, square_size))
# black_bishop = pygame.image.load('pngs/black-bishop.png')
# black_bishop = pygame.transform.scale(black_bishop, (square_size, square_size))
# black_knight = pygame.image.load('pngs/black-knight.png')
# black_knight = pygame.transform.scale(black_knight, (square_size, square_size))
# black_pawn = pygame.image.load('pngs/black-pawn.png')
# black_pawn = pygame.transform.scale(black_pawn, (square_size, square_size))

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
    print(f"FEN String: {fen_string}")
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

# Variables to handle the two-click movement
selected_piece = None
selected_position = None

# Main loop
chessboard = chess.ChessBoard()
chessboard.place_pieces_from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
draw_pieces(chessboard.get_fen_string())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_y // square_size
            clicked_col = mouse_x // square_size

            if selected_piece is None:
                # First click: select a piece if it's at the clicked position
                piece = chessboard.get_piece(clicked_row, clicked_col)
                
                if piece is not None:
                    selected_piece = str(piece)
                    selected_position = (clicked_row, clicked_col)
            else:
                # Second click: move the piece to the clicked position
                chessboard.move_piece(selected_position[0], selected_position[1], clicked_row, clicked_col)
                draw_pieces(chessboard.get_fen_string())
                selected_piece = None
                selected_position = None
                pygame.display.flip()

pygame.quit()
sys.exit()