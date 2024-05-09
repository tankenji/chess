from typing import Dict, List, Tuple, Optional

WHITE = 'white'
BLACK = 'black'

class ChessPiece:
    def __init__(self, color: str, row: int, col: int):
        self.color = color
        self.row = row
        self.col = col
        
    def get_color(self) -> str:
        return self.color
    
    def get_position(self) -> Tuple[int, int]:
        return self.row, self.col        
    
class King(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()

    def __str__(self) -> str:
        if self.color == WHITE:
            return 'K'
        return 'k'

class Queen(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()
    
    def __str__(self) -> str:
        if self.color == WHITE:
            return 'Q'
        return 'q'

class Rook(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()

    def __str__(self) -> str:
        if self.color == WHITE:
            return 'R'
        return 'r'

class Bishop(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()

    def __str__(self) -> str:
        if self.color == WHITE:
            return 'B'
        return 'b'

class Knight(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()
    
    def __str__(self) -> str:
        if self.color == WHITE:
            return 'N'
        return 'n'

class Pawn(ChessPiece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)

    def get_color(self) -> str:
        return super().get_color()
    
    def __str__(self) -> str:
        if self.color == WHITE:
            return 'P'
        return 'p'

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

    def place_pieces_from_fen(self, fen: str):
        fen_parts = fen.split(' ')
        fen_positions = fen_parts[0]
        rows = fen_positions.split('/')
        for row, fen_row in enumerate(rows):
            col = 0
            for char in fen_row:
                if char.isdigit():
                    col += int(char)
                else:
                    if char.isupper():
                        color = WHITE
                    else:
                        color = BLACK
                    if char.lower() == 'r':
                        piece = Rook(color, row, col)
                    elif char.lower() == 'n':
                        piece = Knight(color, row, col)
                    elif char.lower() == 'b':
                        piece = Bishop(color, row, col)
                    elif char.lower() == 'q':
                        piece = Queen(color, row, col)
                    elif char.lower() == 'k':
                        piece = King(color, row, col)
                    elif char.lower() == 'p':
                        piece = Pawn(color, row, col)
                    else:
                        raise ValueError(f"Invalid FEN string: {fen}")
                    self.place_piece(piece, row, col)
                    col += 1
                    
    def get_fen_string(self) -> str:
        fen = ""
        empty_count = 0
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    if isinstance(piece, King):
                        fen += 'k' if piece.get_color() == BLACK else 'K'
                    elif isinstance(piece, Queen):
                        fen += 'q' if piece.get_color() == BLACK else 'Q'
                    elif isinstance(piece, Rook):
                        fen += 'r' if piece.get_color() == BLACK else 'R'
                    elif isinstance(piece, Bishop):
                        fen += 'b' if piece.get_color() == BLACK else 'B'
                    elif isinstance(piece, Knight):
                        fen += 'n' if piece.get_color() == BLACK else 'N'
                    elif isinstance(piece, Pawn):
                        fen += 'p' if piece.get_color() == BLACK else 'P'
                else:
                    empty_count += 1
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            if row < 7:
                fen += '/'
        return fen

class Player:
    def __init__(self, color: str, board: ChessBoard):
        self.color = color
        self.board = board
    
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
    


# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR