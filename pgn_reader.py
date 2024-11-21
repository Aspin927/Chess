import chess_logic  # Import the Board and Piece classes
import re

def parse_pgn(pgn_path):
    """
    Parse a PGN file and return a list of moves.
    Args:
        pgn_path (str): Path to the PGN file.
    Returns:
        List[str]: List of moves in the game.
    """
    with open(pgn_path, 'r') as file:
        pgn_data = file.read()

    # Remove metadata (anything between square brackets) and split moves
    pgn_data = re.sub(r"\[.*\]", "", pgn_data)
    moves = re.findall(r"[a-h1-8NBRQKx+#=-]+", pgn_data)
    return moves

def move_from_notation(board, move, turn):
    """
    Interpret and apply a single move from algebraic notation to the board.
    Args:
        board (Board): The chess board.
        move (str): The move in algebraic notation.
        turn (str): 'white' or 'black' indicating the current turn.
    """
    # For simplicity, we'll map moves based on assumptions and skip complex logic.
    # A proper chess library (like python-chess) can be used for full PGN support.
    
    piece_map = {
        'P': 'pawn', 'N': 'knight', 'B': 'bishop',
        'R': 'rook', 'Q': 'queen', 'K': 'king'
    }
    
    if move in ["O-O", "O-O-O"]:  # Castling
        # Simplified castling logic
        if move == "O-O":  # King-side castling
            king_start, king_end = (7, 4), (7, 6) if turn == 'white' else (0, 4), (0, 6)
            rook_start, rook_end = (7, 7), (7, 5) if turn == 'white' else (0, 7), (0, 5)
        else:  # Queen-side castling
            king_start, king_end = (7, 4), (7, 2) if turn == 'white' else (0, 4), (0, 2)
            rook_start, rook_end = (7, 0), (7, 3) if turn == 'white' else (0, 0), (0, 3)

        board.move_piece(king_start, king_end)
        board.move_piece(rook_start, rook_end)
        return

    # For now, treat all other moves as pawn moves or simplified moves
    start_row, start_col = None, None
    end_col = ord(move[-2]) - ord('a')  # Extract column from move
    end_row = 8 - int(move[-1])         # Extract row from move

    for row in range(8):
        for col in range(8):
            piece = board.grid[row, col]
            if piece and piece.color == turn and (piece_map.get(move[0], 'pawn') == piece.type):
                if col == end_col or (move[0].lower() == 'p' and abs(col - end_col) <= 1):  # Example match
                    start_row, start_col = row, col
                    break

    if start_row is not None:
        board.move_piece((start_row, start_col), (end_row, end_col))


def play_pgn(pgn_path):
    """
    Read a PGN file, parse moves, and play them on the board.
    Args:
        pgn_path (str): Path to the PGN file.
    """
    board = chess_logic.Board(start=True)
    moves = parse_pgn(pgn_path)
    turn = 'white'

    for move in moves:
        print(f"{turn.capitalize()} plays: {move}")
        move_from_notation(board, move, turn)
        board.show()  # Visualize the current board position
        turn = 'black' if turn == 'white' else 'white'


if __name__ == "__main__":
    # Replace 'sample.pgn' with the path to your PGN file
    play_pgn('sample.pgn')
    input()
