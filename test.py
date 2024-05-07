import pygame
import sys

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

# Load a sample chess piece (e.g., rook)
rook = pygame.image.load('pngs/white-rook.png')
rook = pygame.transform.scale(rook, (square_size, square_size))

# Initial positions (0-based indices for rows and columns)
rook_position = (0, 0)

# Variables to handle the two-click movement
selected_piece = None
selected_position = None

# Main loop
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
                if rook_position == (clicked_row, clicked_col):
                    selected_piece = 'rook'
                    selected_position = rook_position
            else:
                # Second click: move the piece to the clicked position
                rook_position = (clicked_row, clicked_col)
                selected_piece = None
                selected_position = None

    # Draw the board
    screen.blit(board, (0, 0))

    # Draw the rook at the new position
    screen.blit(rook, (rook_position[1] * square_size, rook_position[0] * square_size))

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()