import copy
from typing import Dict, List, Tuple, Optional

WHITE = 'w'
BLACK = 'b'

class ChessPiece:
    def __init__(self, color: str, row: int, col: int):
        self.color = color
        self.row = row
        self.col = col
        self.available_moves = []
        
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
        # Check for castling moves
        if self.color == WHITE:
            if self.row == 7 and self.col == 4:  # Check if the king is in its initial position
                if chessboard.castling and 'K' in chessboard.castling:  # Check if kingside castling is allowed
                    if chessboard.get_piece(7, 5) is None and chessboard.get_piece(7, 6) is None:  # Check if the squares between the king and rook are empty
                        moves.append((7, 6))  # Add kingside castle move
                if chessboard.castling and 'Q' in chessboard.castling:  # Check if queenside castling is allowed
                    if chessboard.get_piece(7, 3) is None and chessboard.get_piece(7, 2) is None and chessboard.get_piece(7, 1) is None:  # Check if the squares between the king and rook are empty
                        moves.append((7, 2))  # Add queenside castle move
        elif self.color == BLACK:
            if self.row == 0 and self.col == 4:  # Check if the king is in its initial position
                if chessboard.castling and 'k' in chessboard.castling:  # Check if kingside castling is allowed
                    if chessboard.get_piece(0, 5) is None and chessboard.get_piece(0, 6) is None:  # Check if the squares between the king and rook are empty
                        moves.append((0, 6))  # Add kingside castle move
                if chessboard.castling and 'q' in chessboard.castling:  # Check if queenside castling is allowed
                    if chessboard.get_piece(0, 3) is None and chessboard.get_piece(0, 2) is None and chessboard.get_piece(0, 1) is None:  # Check if the squares between the king and rook are empty
                        moves.append((0, 2))  # Add queenside castle move
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
                if (new_row, new_col) == chessboard._get_en_passant():
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

    def _find_king_location(self) -> Optional[Tuple[int, int]]: # TODO: Optimize using FEN string
        active_color = self._get_active_color()
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.get_color() == active_color:
                    return row, col
        return None

    def handle_moves(self, start_row: int, start_col: int, end_row: int, end_col: int):
        piece1 = self.get_piece(start_row, start_col)
        if piece1 is not None and piece1.get_color() != self.active_color:
            print("Invalid move: Cannot move opponent's piece")
            return
            # raise ValueError("Invalid move: Cannot move opponent's piece")
        piece2 = self.get_piece(end_row, end_col)
        if piece2 is not None and piece2.get_color() == self.active_color:
            print("Invalid move: Cannot capture own piece")
            return
            # raise ValueError("Invalid move: Cannot capture own piece")

        # Handle castling
        distance = end_col - start_col
        if isinstance(piece1, King) and abs(distance) == 2 and (end_row, end_col) in piece1.get_available_moves():
            if self.active_color == WHITE:
                if distance > 0:  # Kingside castle
                    self._move_piece(start_row, start_col, start_row, start_col + 2)
                    self._move_piece(start_row, start_col + 3, start_row, start_col + 1)
                else:  # Queenside castle
                    self._move_piece(start_row, start_col, start_row, start_col - 2)
                    self._move_piece(start_row, start_col - 4, start_row, start_col - 1)
                if "K" in self.castling:
                    self.castling = self.castling.replace("K", "")
                if "Q" in self.castling:
                    self.castling = self.castling.replace("Q", "")
            else:  # BLACK
                if distance > 0:  # Kingside castle
                    self._move_piece(start_row, start_col, start_row, start_col + 2)
                    self._move_piece(start_row, start_col + 3, start_row, start_col + 1)
                else:  # Queenside castle
                    self._move_piece(start_row, start_col, start_row, start_col - 2)
                    self._move_piece(start_row, start_col - 4, start_row, start_col - 1)
                if "k" in self.castling:
                    self.castling = self.castling.replace("k", "")
                if "q" in self.castling:
                    self.castling = self.castling.replace("q", "")
            self.en_passant = None
            self._update_half_full_moves()
            self._update_active_color()
            return

        # Check if the move is an en passant
        if isinstance(piece1, Pawn) and self.en_passant == (end_row, end_col) and self.en_passant in piece1.get_available_moves():
            print("ENTERED: en passant move")
            self._move_piece(start_row, start_col, end_row, end_col)
            pawn = None
            if self.active_color == WHITE:
                pawn = self.get_piece(start_row, end_col)
                self._remove_piece(pawn)
            elif self.active_color == BLACK:
                pawn = self.get_piece(start_row, end_col)
                self._remove_piece(pawn)
            self.en_passant = None
            self._update_half_full_moves()
            self._update_active_color()
            return

        # Check if the move is a regular move
        if (end_row, end_col) not in piece1.get_available_moves():
            print("Invalid move: Piece cannot move to that position")
            return

        # Move the piece
        self._move_piece(start_row, start_col, end_row, end_col)

        # Check if the move was a king move to remove castling options
        if isinstance(piece1, King):
            if self.active_color == WHITE:
                if "K" in self.castling:
                    self.castling = self.castling.replace("K", "")
                if "Q" in self.castling:
                    self.castling = self.castling.replace("Q", "")
            else:
                if "k" in self.castling:
                    self.castling = self.castling.replace("k", "")
                if "q" in self.castling:
                    self.castling = self.castling.replace("q", "")

        # Check if the move was a rook move to remove castling options
        if isinstance(piece1, Rook):
            if self.active_color == WHITE:
                if start_row == 7 and start_col == 0 and "Q" in self.castling:
                    self.castling = self.castling.replace("Q", "")
                if start_row == 7 and start_col == 7 and "K" in self.castling:
                    self.castling = self.castling.replace("K", "")
            else:
                if start_row == 0 and start_col == 0 and "q" in self.castling:
                    self.castling = self.castling.replace("q", "")
                if start_row == 0 and start_col == 7 and "k" in self.castling:
                    self.castling = self.castling.replace("k", "")
        
        # Check if the move is a pawn promotion
        if isinstance(piece1, Pawn) and (end_row == 0 or end_row == 7):
            self._remove_piece(piece1)
            self._place_piece(Queen(self.active_color, end_row, end_col), end_row, end_col)

        # Check if move is a pawn double move
        if isinstance(piece1, Pawn) and abs(start_row - end_row) == 2:
            if self.active_color == WHITE:
                self.en_passant = (end_row + 1, end_col)
                print("white en passant set")
            else:
                self.en_passant = (end_row - 1, end_col)
                print("black en passant set")
            # self.en_passant = (end_row, end_col)
        else:
            self.en_passant = None
        print("en passant after move at: " + str(self.en_passant))
        self._update_half_full_moves()
        self._update_active_color()

    def _update_active_color(self):
        if self.active_color == WHITE:
            self.active_color = BLACK
        else:
            self.active_color = WHITE

    def _update_half_full_moves(self):
        self.halfmove_clock += 1
        if self.active_color == BLACK:
            self.fullmove_number += 1

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
            self.en_passant = (8 - int(fen_parts[3][1])), ord(fen_parts[3][0]) - ord('a')
        self.castling = fen_parts[2]
        self.halfmove_clock = int(fen_parts[4])
        self.fullmove_number = int(fen_parts[5])
        self._calculate_all_available_moves()
        self.remove_check_moves()

    def _calculate_all_available_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None:
                    piece.calculate_available_moves(self)

    def remove_check_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None and piece.get_color() == self.active_color:
                    moves = piece.get_available_moves()
                    for move in moves[:]:  # The [:] creates a copy of the list
                        # Check if a castling move results in a check in transition
                        distance = move[1] - piece.get_position()[1]
                        if isinstance(piece, King) and abs(distance) == 2: # Castling move
                            if distance < 0: # Queenside castling
                                print("Queenside castling")
                                if self.simulate_future_move_check(piece, (row, col - 1)):
                                    piece.available_moves.remove(move)
                                    print("KING IN-TRANSITION CHECK")
                            elif distance > 0: # Kingside castling
                                if self.simulate_future_move_check(piece, (row, col + 1)):
                                    piece.available_moves.remove(move)
                        # For all other moves
                        if self.simulate_future_move_check(piece, move):
                            piece.available_moves.remove(move)

    def get_available_moves_for_black(self) -> List[Tuple[int, int]]:
        available_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None and piece.get_color() == BLACK:
                    moves = piece.get_available_moves()
                    for move in moves:
                        available_moves.append(move)
        return available_moves
    
    def get_available_moves_for_white(self) -> List[Tuple[int, int]]:
        available_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None and piece.get_color() == WHITE:
                    moves = piece.get_available_moves()
                    for move in moves:
                        available_moves.append(move)
        return available_moves

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
            print(f"en passant when updating fen: {self.en_passant}")
            row = 8 - self.en_passant[0]
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

    def simulate_future_move_check(self, piece: ChessPiece, new_move: Tuple[int, int]) -> bool:
        """Simulate a future move to check if it results in a check."""
        # Create a copy of the current board
        board_copy = copy.deepcopy(self)
        
        # Get the current position of the piece
        current_row, current_col = piece.get_position()
        
        # Get the new position of the piece after the move
        new_row, new_col = new_move
        
        # Check if the new position is within the board boundaries
        if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
            return False
        
        # Check if the new position is the same as the current position
        if new_row == current_row and new_col == current_col:
            return False
        
        # Note: we already check if the move is in the available moves in the main function
        
        # Check if the new position is occupied by a piece of the same color
        if board_copy.get_piece(new_row, new_col) is not None and board_copy.get_piece(new_row, new_col).get_color() == piece.get_color():
            return False
        
        # Move the piece from the current position to the new position
        board_copy._move_piece(current_row, current_col, new_row, new_col)
        board_copy._calculate_all_available_moves()
        # Check if the move results in a check
        king_location = board_copy._find_king_location()
        if board_copy.active_color == WHITE and king_location is not None and king_location in board_copy.get_available_moves_for_black():
            return True
        if board_copy.active_color == BLACK and king_location is not None and king_location in board_copy.get_available_moves_for_white():
            return True
        return False
        