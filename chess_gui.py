import pygame
from chess_logic import Board, Piece

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SQUARE_SIZE = SCREEN_WIDTH // 8

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for rendering piece symbols
FONT = pygame.font.Font(None, 80)

# Piece Symbols (Unicode Chess Pieces)
PIECE_SYMBOLS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}


def draw_board(screen, board):
    """Draw the chessboard and pieces."""
    for row in range(8):
        for col in range(8):
            # Draw squares
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw pieces
            piece = board.grid[row, col]
            if piece:
                symbol = PIECE_SYMBOLS[repr(piece)]
                text = FONT.render(symbol, True, BLACK if piece.color == 'white' else WHITE)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                  row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text, text_rect)


def main():
    # Initialize the board
    board = Board(start=True)

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Variables for dragging pieces
    dragging_piece = None
    dragging_piece_pos = None
    selected_square = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the square clicked
                mouse_x, mouse_y = event.pos
                row, col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE

                # If there's a piece in the square, start dragging
                if board.grid[row, col]:
                    dragging_piece = board.grid[row, col]
                    dragging_piece_pos = (row, col)
                    selected_square = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_piece:
                    # Get the square where the piece is dropped
                    mouse_x, mouse_y = event.pos
                    drop_row, drop_col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE

                    # Move the piece
                    board.move_piece(dragging_piece_pos, (drop_row, drop_col))

                    # Reset dragging variables
                    dragging_piece = None
                    dragging_piece_pos = None
                    selected_square = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_piece:
                    selected_square = None

        # Draw the board and pieces
        screen.fill(WHITE)
        draw_board(screen, board)

        # Highlight the selected square
        if selected_square:
            row, col = selected_square
            pygame.draw.rect(screen, HIGHLIGHT, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

        # Render the dragging piece
        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            symbol = PIECE_SYMBOLS[repr(dragging_piece)]
            text = FONT.render(symbol, True, BLACK if dragging_piece.color == 'white' else WHITE)
            screen.blit(text, (mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2))

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
