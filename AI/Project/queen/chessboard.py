import pygame
import sys

class Chessboard:
    def __init__(self, size=8):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.piece_images = {}

    def load_piece_images(self, piece_images):
        self.piece_images = piece_images

    def set_queen_positions(self, positions):
        """Clear board and place queens at specified column positions per row"""
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for row, col in enumerate(positions):
            self.board[row][col] = 'queen'

    def draw(self, screen):
        square_size = screen.get_width() // self.size
        for row in range(self.size):
            for col in range(self.size):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))
                piece = self.board[row][col]
                if piece and piece in self.piece_images:
                    resized_img = pygame.transform.scale(self.piece_images[piece], (square_size, square_size))
                    screen.blit(resized_img, (col * square_size, row * square_size))


def load_queen_images():
    piece_images = {}
    image_path = 'img/queen.png'
    try:
        piece_images['queen'] = pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")
    return piece_images


def create_chessboard(n, queen_positions):
    pygame.init()
    window_size = min(900, max(400, n * 80))  # scale size dynamically
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption(f"{n}-Queens Visualization")
    
    chessboard = Chessboard(n)
    piece_images = load_queen_images()
    chessboard.load_piece_images(piece_images)
    chessboard.set_queen_positions(queen_positions)
    
    return chessboard, screen


def main(n=8, queen_positions=None):
    if queen_positions is None:
        # default example for 8-queens
        queen_positions = [0, 4, 7, 5, 2, 6, 1, 3]
    
    if len(queen_positions) != n:
        print("❌ The number of queen positions must match n!")
        sys.exit(1)

    chessboard, screen = create_chessboard(n, queen_positions)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        chessboard.draw(screen)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    # Example usage for N=10
    solution = [0, 2, 4, 7, 9, 3, 1, 8, 5, 6]  # must be size N
    main(n=10, queen_positions=solution)
