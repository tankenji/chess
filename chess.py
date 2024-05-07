from typing import Dict, List, Tuple, Optional

WHITE = 'white'
BLACK = 'black'

class ChessPiece:
    def __init__(self, color: str):
        self.color = color
    
    def get_color(self) -> str:
        return self.color

class King(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class Queen(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class Rook(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class Bishop(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class Knight(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class Pawn(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)

    def get_color(self) -> str:
        return super().get_color()

class ChessBoard:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]

    def place_piece(self, piece, row, col):
        self.board[row][col] = piece

    def remove_piece(self, row, col):
        self.board[row][col] = None

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

    def get_piece(self, row, col) -> Optional[ChessPiece]:
        return self.board[row][col]


    class Player:
        def __init__(self, color: str):
            self.color = color
        
        def get_color(self) -> str:
            return self.color
        
        def get_owned_pieces(self) -> Dict[ChessPiece, Tuple[int, int]]:
                owned_pieces = {}
                for row in range(8):
                    for col in range(8):
                        piece = self.board.get_piece(row, col)
                        if piece and piece.get_color() == self.color:
                            owned_pieces[piece] = (row, col)
                return owned_pieces



