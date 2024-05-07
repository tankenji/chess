import sys
from random import random, shuffle
from typing import Dict, List, Optional

import pygame
import chess

# Game Screen dimensions in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Chess Board
CHESS_BOARD = 'pngs/rect-8x8.png'

# Chess Piece Images
BLACK_PAWN = 'pngs/black_pawn.png'
BLACK_ROOK = 'pngs/black_rook.png'
BLACK_KNIGHT = 'pngs/black_knight.png'
BLACK_BISHOP = 'pngs/black_bishop.png'
BLACK_QUEEN = 'pngs/black_queen.png'
BLACK_KING = 'pngs/black_king.png'

WHITE_PAWN = 'pngs/white_pawn.png'
WHITE_ROOK = 'pngs/white_rook.png'
WHITE_KNIGHT = 'pngs/white_knight.png'
WHITE_BISHOP = 'pngs/white_bishop.png'
WHITE_QUEEN = 'pngs/white_queen.png'
WHITE_KING = 'pngs/white_king.png'

class ChessGame:
    """User interface of the Chess game.

    """