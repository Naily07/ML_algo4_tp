import pygame
import sys
import random

class GamePuzzle:
    def __init__(self, grid_size, swap_interval):
        """Initialise le jeu avec une taille de grille et un intervalle de swaps."""
        self.grid_size = grid_size  # Taille de la grille (par exemple, 3 pour une grille 3x3)
        self.swap_interval = swap_interval  # Intervalle des swaps
        self.move_count = 0
        self.swap_mode = False  # Indique si le mode swap est actif
        self.selected_tiles = []  # Cases sélectionnées pour un swap
        self.running = True

        # Calcul des tailles des cases et de la fenêtre en fonction de la grille
        self.window_size = 300  # Taille de la fenêtre (peut être ajustée)
        self.tile_size = self.window_size // self.grid_size
        self.font_size = 50
        self.background_color = (30, 30, 30)
        self.tile_color = (100, 150, 200)
        self.text_color = (255, 255, 255)

        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption(f"Puzzle {self.grid_size}x{self.grid_size}")
        self.font = pygame.font.Font(None, self.font_size)

        # Création du puzzle
        self.grid = self.create_puzzle()

    def create_puzzle(self):
        """Crée une grille mélangée pour le puzzle."""
        tiles = list(range(1, self.grid_size ** 2)) + [0]  # 0 représente l'espace vide
        random.shuffle(tiles)
        return [tiles[i:i + self.grid_size] for i in range(0, len(tiles), self.grid_size)]

    def draw_puzzle(self):
        """Dessine la grille de puzzle sur l'écran."""
        self.screen.fill(self.background_color)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.grid[row][col]
                x, y = col * self.tile_size, row * self.tile_size
                if tile != 0:  # Ne dessine pas l'espace vide
                    pygame.draw.rect(self.screen, self.tile_color, (x, y, self.tile_size, self.tile_size))
                    text = self.font.render(str(tile), True, self.text_color)
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)
        pygame.display.flip()

    def move_tile(self, row, col):
        """Déplace une case sélectionnée si elle est adjacente à l'espace vide."""
        empty_row, empty_col = next(
            (r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0
        )
        if (abs(row - empty_row) + abs(col - empty_col)) == 1:
            self.grid[empty_row][empty_col], self.grid[row][col] = self.grid[row][col], self.grid[empty_row][empty_col]

    def swap_tiles(self, row1, col1, row2, col2):
        """Échange deux cases sélectionnées."""
        self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]

    def is_solved(self):
        """Vérifie si le puzzle est résolu."""
        correct = list(range(1, self.grid_size ** 2)) + [0]
        flat_grid = [tile for row in self.grid for tile in row]
        return flat_grid == correct

    def handle_events(self):
        """Gère les événements utilisateur."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // self.tile_size, y // self.tile_size

                if not self.swap_mode:  # Mode normal : déplacement des cases
                    self.move_tile(row, col)
                    self.move_count += 1

                    # Active le mode swap si nécessaire
                    if self.move_count % self.swap_interval == 0:
                        self.swap_mode = True
                        print("Mode swap activé ! Sélectionnez deux cases à échanger.")

                else:  # Mode swap : sélection des cases
                    self.selected_tiles.append((row, col))
                    if len(self.selected_tiles) == 2:
                        # Effectue le swap
                        r1, c1 = self.selected_tiles[0]
                        r2, c2 = self.selected_tiles[1]
                        self.swap_tiles(r1, c1, r2, c2)
                        self.selected_tiles.clear()
                        self.swap_mode = False
                        print("Swap effectué. Retour au mode normal.")

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.draw_puzzle()

            if self.is_solved():
                print(f"Félicitations ! Vous avez résolu le puzzle en {self.move_count} mouvements.")
                self.running = False

        pygame.quit()


# Exécution du jeu
if __name__ == "__main__":
    grid_size = 3  # Exemple de taille de puzzle (4x4)
    swap_interval = 5  # Intervalle pour passer en mode swap
    game = GamePuzzle(grid_size, swap_interval)
    game.run()
