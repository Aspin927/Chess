import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define the Piece class
class Piece:
    def __init__(self, type: str, position: tuple[int, int], color: str, castled=False):
        self.type = type
        self.position = position
        self.color = color
        self.castled = castled

    def __repr__(self):
        symbols = {
            'pawn': 'P', 'bishop': 'B', 'knight': 'N', 
            'rook': 'R', 'queen': 'Q', 'king': 'K'
        }
        return symbols[self.type] if self.color == 'white' else symbols[self.type].lower()


# Define the Board class
class Board:
    def __init__(self, start: bool = True):
        self.grid = np.full((8, 8), None)
        if start:
            self.setup_starting_position()

    def setup_starting_position(self):
        """Set up the board with the standard chess starting position."""
        for col in range(8):
            self.grid[1, col] = Piece('pawn', (1, col), 'black')
            self.grid[6, col] = Piece('pawn', (6, col), 'white')

        back_rank = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col, piece in enumerate(back_rank):
            self.grid[0, col] = Piece(piece, (0, col), 'black')
            self.grid[7, col] = Piece(piece, (7, col), 'white')

    def move_piece(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        """
        Move a piece from start to end.
        Args:
            start: (row, col) of the piece to move.
            end: (row, col) of the target position.
        Returns:
            True if the move was successful, False otherwise.
        """
        # Validate starting position
        start_row, start_col = start
        end_row, end_col = end

        if self.grid[start_row, start_col] is None:
            print("No piece at the starting position.")
            return False

        # Perform the move
        piece = self.grid[start_row, start_col]
        self.grid[end_row, end_col] = piece
        self.grid[start_row, start_col] = None

        # Update piece's internal position
        piece.position = (end_row, end_col)
        return True

    def show(self):
        """Display the board using matplotlib."""
        board_colors = sns.color_palette("pastel", 2)
        board = np.zeros((8, 8, 3))
        for row in range(8):
            for col in range(8):
                color = board_colors[(row + col) % 2]
                board[row, col] = color

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(board, extent=[0, 8, 0, 8])

        for row in range(8):
            for col in range(8):
                piece = self.grid[row, col]
                if piece:
                    ax.text(col + 0.5, 7.5 - row, repr(piece), 
                            ha='center', va='center', fontsize=16, fontweight='bold')

        ax.set_xticks(np.arange(8) + 0.5)
        ax.set_yticks(np.arange(8) + 0.5)
        ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        ax.set_yticklabels([str(i) for i in range(1, 9)])
        ax.tick_params(left=False, bottom=False, labelsize=12)

        ax.grid(color='black', linestyle='-', linewidth=1, which='both')
        ax.set_xticks(np.arange(8), minor=True)
        ax.set_yticks(np.arange(8), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

        plt.show()


# Example usage
if __name__ == "__main__":
    board = Board(start=True)
    board.show()

    # Example moves
    print("Moving pawn from (6, 4) to (4, 4)")
    board.move_piece((6, 4), (4, 4))  # Move white pawn from e2 to e4
    board.show()

    print("Moving knight from (7, 1) to (5, 2)")
    board.move_piece((7, 1), (5, 2))  # Move white knight from b1 to c3
    board.show()
