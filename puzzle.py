import pygame
import random

# Dimensions du puzzle et de la fenêtre
TILE_SIZE = 100
GRID_SIZE = 3
WINDOW_SIZE = TILE_SIZE * GRID_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class NPuzzleKSwap:
    def __init__(self, n=8, k=5):
        self.n = n
        self.k = k
        self.size = int((n + 1) ** 0.5)  # Taille de la grille
        self.board = self.generate_board()
        self.moves = 0
        self.selected_tiles = []  # Tuiles sélectionnées pour le swap

    def generate_board(self):
        """Génère un puzzle initial valide mélangé."""
        tiles = list(range(1, self.n + 1)) + [0]
        random.shuffle(tiles)
        while not self.is_solvable(tiles):
            random.shuffle(tiles)
        return [tiles[i:i + self.size] for i in range(0, len(tiles), self.size)]

    def is_solvable(self, tiles):
        """Vérifie si le puzzle est solvable."""
        inversions = 0
        tiles = [tile for tile in tiles if tile != 0]
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1
        return inversions % 2 == 0

    def find_empty(self):
        """Trouve la position de la case vide."""
        for i, row in enumerate(self.board):
            if 0 in row:
                return i, row.index(0)

    def move(self, direction):
        """Déplace la case vide."""
        i, j = self.find_empty()
        if direction == "up" and i > 0:
            self.board[i][j], self.board[i - 1][j] = self.board[i - 1][j], self.board[i][j]
        elif direction == "down" and i < self.size - 1:
            self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
        elif direction == "left" and j > 0:
            self.board[i][j], self.board[i][j - 1] = self.board[i][j - 1], self.board[i][j]
        elif direction == "right" and j < self.size - 1:
            self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
        else:
            return False
        self.moves += 1
        return True

    def swap(self, pos1, pos2):
        """Échange deux pièces."""
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]

    def is_solved(self):
        """Vérifie si le puzzle est résolu."""
        flat_board = [tile for row in self.board for tile in row]
        return flat_board == list(range(1, self.n + 1)) + [0]

def draw_board(screen, game):
    """Dessine le puzzle sur l'écran."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 60)
    for i in range(game.size):
        for j in range(game.size):
            tile = game.board[i][j]
            x, y = j * TILE_SIZE, i * TILE_SIZE
            if tile != 0:
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
                text = font.render(str(tile), True, BLACK)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("n-puzzle-k-swap")

    game = NPuzzleKSwap(n=8, k=5)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // TILE_SIZE, x // TILE_SIZE
                game.selected_tiles.append((row, col))
                if len(game.selected_tiles) == 2:
                    game.swap(*game.selected_tiles)
                    game.selected_tiles.clear()

        draw_board(screen, game)
        pygame.display.flip()

        if game.is_solved():
            print(f"Félicitations! Résolu en {game.moves} mouvements.")
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()