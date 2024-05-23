from typing import Dict, List, Tuple, Optional

WHITE = 'w'
BLACK = 'b'

class ChessPiece:
    def __init__(self, color: str, row: int, col: int):
        self.color = color
        self.row = row
        self.col = col
        self.available_moves = None
        
    def get_color(self) -> str:
        return self.color
    
    def get_position(self) -> Tuple[int, int]:
        return self.row, self.col
    
    def update_position(self, new_row: int, new_col: int) -> None:
        self.row = new_row
        self.col = new_col
        return

    def get_available_moves(self) -> List[Tuple[int, int]]:
        return self.available_moves
    
    def calculate_available_moves(self, board):
        """Calculate the available moves for this piece given the current state of the board."""
        raise NotImplementedError("This method must be implemented in a subclass.")
    
class King(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a King."""
        moves = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_row, new_col = self.row + dx, self.col + dy
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check that the move is on the board.
                new_spot = chessboard.get_piece(new_row, new_col)
                if new_spot is None or new_spot.color != self.color:  # Destination square is empty or contains an opponent's piece.
                    moves.append((new_row, new_col))
        self.available_moves = moves

class Queen(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a Queen."""
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            new_row, new_col = self.row + dx, self.col + dy
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                new_spot = chessboard.get_piece(new_row, new_col)
                if new_spot is None:
                    moves.append((new_row, new_col))
                elif new_spot.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dx
                new_col += dy
        self.available_moves = moves


class Rook(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a Rook."""
        moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            new_row, new_col = self.row + dx, self.col + dy
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = chessboard.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.get_color() != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dx
                new_col += dy
        self.available_moves = moves

class Bishop(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a Bishop."""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            new_row, new_col = self.row + dx, self.col + dy
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = chessboard.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.get_color() != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dx
                new_col += dy
        self.available_moves = moves

class Knight(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a Knight."""
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in directions:
            new_row, new_col = self.row + dx, self.col + dy
            if 0 <= new_row < 8 and 0 <= new_col < 8 and (chessboard.get_piece(new_row, new_col) is None or chessboard.get_piece(new_row, new_col).color != self.color):
                moves.append((new_row, new_col))
        self.available_moves = moves

class Pawn(ChessPiece):
    def calculate_available_moves(self, chessboard: 'ChessBoard'):
        """Calculate the available moves for a Pawn."""
        moves = []
        row, col = self.get_position()
        color = self.get_color()
        # Determine the direction of movement based on the color of the pawn
        if color == WHITE:
            direction = -1
        else:
            direction = 1
        # Check if the pawn can move forward one square
        new_row = row + direction
        if 0 <= new_row < 8 and chessboard.get_piece(new_row, col) is None:
            moves.append((new_row, col))
            # Check if the pawn is in its starting position and can move forward two squares
            if (color == WHITE and row == 6) or (color == BLACK and row == 1):
                new_row2 = row + 2 * direction
                if chessboard.get_piece(new_row2, col) is None:
                    moves.append((new_row2, col))
        # Check if the pawn can capture diagonally
        for dcol in [-1, 1]: # Check left and right
            new_row = row + direction
            new_col = col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = chessboard.get_piece(new_row, new_col)
                if piece is not None and piece.get_color() != color:
                    moves.append((new_row, new_col))
        self.available_moves = moves
        

class ChessBoard:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.active_color = None
        self.en_passant = None
        self.castling = None
        self.halfmove_clock = 0
        self.fullmove_number = 0

    def _place_piece(self, piece: ChessPiece, row: int, col: int):
        self.board[row][col] = piece
        piece.update_position(row, col)

    def _remove_piece(self, piece: ChessPiece):
        row, col = piece.get_position()
        self.board[row][col] = None
        piece.update_position(-1, -1)

    def get_piece(self, row, col) -> Optional[ChessPiece]:
        return self.board[row][col]

    def _get_active_color(self) -> str:
        return self.active_color

    def _get_en_passant(self) -> Optional[Tuple[int, int]]:
        return self.en_passant

    def _move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        self._remove_piece(piece)
        self._place_piece(piece, end_row, end_col)

    def handle_moves(self, start_row: int, start_col: int, end_row: int, end_col: int):
        piece1 = self.get_piece(start_row, start_col)
        if piece1 is not None and piece1.get_color() != self.active_color:
            raise ValueError("Invalid move: Cannot move opponent's piece")
        piece2 = self.get_piece(end_row, end_col)
        if piece2 is not None and piece2.get_color() == self.active_color:
            raise ValueError("Invalid move: Cannot capture own piece")

        # Check if the move is a castle
        castle_side = None
        if isinstance(piece1, King) and isinstance(piece2, Rook):
            castle_side = self._check_castle_side(piece1, piece2)
        if castle_side is not None and self.castling is not None:
            self._handle_castling(castle_side)
            return

        # Check if the move is an en passant
        if isinstance(piece1, Pawn) and self.en_passant == (end_row, end_col):
            pawn = None
            if self.active_color == WHITE:
                pawn = self.get_piece(end_row - 1, end_col)
            else: # BLACK
                pawn = self.get_piece(end_row + 1, end_col)
            if pawn is not None and not isinstance(pawn, Pawn):
                self._handle_en_passant(piece1, pawn)
                return

        # Check if the move is a regular move
        if (end_row, end_col) not in piece1.get_available_moves():
            raise ValueError("Invalid move: Piece cannot move to that position")

        # Move the piece
        self._move_piece(start_row, start_col, end_row, end_col)
        self._update_half_full_moves()
        self._update_active_color()
        
        # Check if the move is a pawn promotion
        if isinstance(piece1, Pawn) and (end_row == 0 or end_row == 7):
            self._remove_piece(piece1)
            self._place_piece(Queen(self.active_color, end_row, end_col), end_row, end_col)


    def _update_active_color(self):
        if self.active_color == WHITE:
            self.active_color = BLACK
        else:
            self.active_color = WHITE

    def _update_half_full_moves(self):
        self.halfmove_clock += 1
        if self.active_color == BLACK:
            self.fullmove_number += 1
    
    def _handle_en_passant(self, piece1: ChessPiece, piece2: ChessPiece):
        row1, col1 = piece1.get_position() # starting pawn
        row2, col2 = piece2.get_position()
        if row1 == row2 and abs(col1 - col2) == 1:
            self._move_piece(row1, col1, row2, col2)
            self.en_passant = None
            return

    def _check_castle_side(self, piece1: ChessPiece, piece2: ChessPiece) -> str:
        active_color = self._get_active_color()
        if not piece1.color == active_color or not piece2.color == active_color:
            return None
        if active_color == WHITE:
            if piece2.col > piece1.col and self.castling.find("K") != -1:
                return "kingside"
            elif piece2.col < piece1.col and self.castling.find("Q") != -1:
                return "queenside"
        if active_color == BLACK:
            if piece2.col > piece1.col and self.castling.find("k") != -1:
                return "kingside"
            elif piece2.col < piece1.col and self.castling.find("q") != -1:
                return "queenside"
        return None

    def _handle_castling(self, side: str):
        if self.active_color == WHITE:
            king_row = 7
        else:
            king_row = 0

        if side == "kingside":
            rook_col = 7
            new_king_col = 6
            new_rook_col = 5
        elif side == "queenside":
            rook_col = 0
            new_king_col = 2
            new_rook_col = 3
        else:
            raise ValueError("Invalid castle side")

        king = self.get_piece(king_row, 4)
        rook = self.get_piece(king_row, rook_col)

        if not isinstance(king, King) or not isinstance(rook, Rook):
            raise ValueError("Invalid castle move")

        if king.get_color() != self.active_color or rook.get_color() != self.active_color:
            raise ValueError("Invalid castle move")

        if king.get_position() != (king_row, 4) or rook.get_position() != (king_row, rook_col):
            raise ValueError("Invalid castle move")

        # Check if there are any pieces between the king and rook
        # TODO: Check if the king is in check, moves through check, or ends in check
        if rook_col == 7:
            for col in range(5, 7):
                if self.get_piece(king_row, col) is not None:
                    raise ValueError("Invalid castle move")
        else:
            for col in range(1, 4):
                if self.get_piece(king_row, col) is not None:
                    raise ValueError("Invalid castle move")

        # Update the board
        self._move_piece(king_row, 4, king_row, new_king_col)
        self._move_piece(king_row, rook_col, king_row, new_rook_col)

        # Update the fen string
        if side == "kingside":
            if self.active_color == WHITE:
                self.castling = self.castling.replace("K", "")
            else:  # BLACK
                self.castling = self.castling.replace("k", "")
        elif side == "queenside":
            if self.active_color == WHITE:
                self.castling = self.castling.replace("Q", "")
            else:  # BLACK
                self.castling = self.castling.replace("q", "")
        if self.castling == "":
            self.castling = None

    def _place_pieces_from_fen(self, fen: str):
        rows = fen.split('/')
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
                    self._place_piece(piece, row, col)
                    col += 1

    def process_fen_string(self, fen: str):
        fen_parts = fen.split(' ')
        self._place_pieces_from_fen(fen_parts[0])
        self.active_color = fen_parts[1]
        if fen_parts[3] == '-':
            self.en_passant = None
        else:
            self.en_passant = (int(fen_parts[3][1]), ord(fen_parts[3][0]) - ord('a'))
        self.castling = fen_parts[2]
        self.halfmove_clock = int(fen_parts[4])
        self.fullmove_number = int(fen_parts[5])
        self._calculate_all_available_moves()

    def _calculate_all_available_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None:
                    piece.calculate_available_moves(self)

    def get_fen_string(self) -> str:
        fen = self._get_board_fen_string()
        fen += f" {self._get_active_color()}"
        if self.castling is None:
            fen += " -"
        else:
            fen += f" {self.castling}"
        if self.en_passant is None:
            fen += " -"
        else:
            row = self.en_passant[0]
            col = chr(self.en_passant[1] + ord('a'))
            fen += f" {col}{row}"
        fen += f" {self.halfmove_clock}"
        fen += f" {self.fullmove_number}"
        return fen

    def _get_board_fen_string(self) -> str:
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

# class Player:
#     def __init__(self, color: str, board: ChessBoard):
#         self.color = color
#         self.board = board
    
#     def get_color(self) -> str:
#         return self.color
    
#     def get_owned_pieces(self) -> Dict[ChessPiece, Tuple[int, int]]:
#             owned_pieces = {}
#             for row in range(8):
#                 for col in range(8):
#                     piece = self.board.get_piece(row, col)
#                     if piece and piece.get_color() == self.color:
#                         owned_pieces[piece] = (row, col)
#             return owned_pieces
    


# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR