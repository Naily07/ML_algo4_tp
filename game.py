import pygame
import sys
import random
from PIL import Image

class GamePuzzle:
    def __init__(self, grid_size, swap_interval, image_path):
        """Initialise le jeu avec une taille de grille et un intervalle de swaps."""
        self.initialGrid = list(range(1, grid_size + 1) )
        self.grid_size = int((grid_size + 1) ** 0.5)  # Taille de la grille (par exemple, 3 pour une grille 3x3)
        self.image_path = image_path
        self.swap_interval = swap_interval  # Intervalle des swaps
        self.move_count = 0
        self.swap_mode = False  # Indique si le mode swap est actif
        self.selected_tiles = []  # Cases sélectionnées pour un swap
        self.running = True

        # Calcul des tailles des cases et de la fenêtre en fonction de la grille
        self.window_size = 500  # Taille de la fenêtre (peut être ajustée)
        self.tile_size = self.window_size // self.grid_size
        self.font_size = 50
        self.background_color = (30, 30, 30)
        self.tile_color = (100, 150, 200)
        self.selected_tile_color = (255, 0, 0)  # Couleur pour les cases sélectionnées
        self.text_color = (255, 255, 255)
    
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size + self.window_size, self.window_size ))
        # self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption(f"Puzzle {self.grid_size}x{self.grid_size}")
        self.font = pygame.font.Font(None, self.font_size)
        self.image = Image.open(self.image_path)
        # self.image_slices = self.image_slicer()
        self.object = self.image_slicer()
        # Création du puzzle
        self.grid = self.create_puzzle()

    def image_slicer(self):
        """Découpe l'image en morceaux pour le puzzle."""
        # image = Image.open(self.image_path)
        largeur, hauteur = self.image.size

        morceau_largeur = largeur // self.grid_size
        morceau_hauteur = hauteur // self.grid_size

        morceaux = []
        image_map = {}
        print("Initial, ", self.initialGrid)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                left = j * morceau_largeur
                upper = i * morceau_hauteur
                right = (j + 1) * morceau_largeur
                lower = (i + 1) * morceau_hauteur
                morceau = self.image.crop((left, upper, right, lower))
                morceaux.append(pygame.image.fromstring(morceau.tobytes(), morceau.size, morceau.mode))
        
        for i, tile_id in enumerate(self.initialGrid):
            image_map[tile_id] = morceaux[i]

        deletemor = morceaux.pop()
        return image_map
    
    def create_puzzle(self):
        """Crée une grille mélangée pour le puzzle."""
        tiles = self.initialGrid.copy()  # Utilisez les chiffres inital
        tiles.append(None)
        random.shuffle(tiles)
        print("Tiles", tiles)
        return [tiles[i:i + self.grid_size] for i in range(0, len(tiles), self.grid_size)]

    def draw_puzzle(self):
        """Dessine la grille de puzzle et l'image originale redimensionnée sur l'écran."""
        self.screen.fill(self.background_color)

        # Dessiner la grille du puzzle
        #self.grid contient initalGridShuffle
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.grid[row][col]
                x, y = col * self.tile_size, row * self.tile_size
                if tile is not None:  # Ne dessine pas l'espace vide
                    self.screen.blit(pygame.transform.scale(self.object[self.grid[row][col]], (self.tile_size, self.tile_size)), (x, y))

        # Afficher l'image originale redimensionnée
        original_width = self.window_size   # Largeur fixée pour l'image originale
        original_height = self.window_size      # Hauteur ajustée proportionnellement

        # Convertir l'image PIL en une surface Pygame si ce n'est pas encore fait
        if not hasattr(self, 'image_surface'):
            image_resized = self.image.resize((original_width, original_height))  # Redimensionner
            self.image_surface = pygame.image.fromstring(image_resized.tobytes(), image_resized.size, image_resized.mode)

        # Blit (dessiner) l'image redimensionnée
        self.screen.blit(self.image_surface, (self.grid_size * self.tile_size, 0))

        # Mettre à jour l'affichage
        pygame.display.flip()

    def move_tile(self, row, col):
        """Déplace une case sélectionnée si elle est adjacente à l'espace vide."""
        empty_row, empty_col = None, None

        # Recherche de l'espace vide dans la grille
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] is None:
                    empty_row, empty_col = r, c
                    break
            if empty_row is not None:  # Arrêter la recherche une fois trouvé
                break

        # Vérifie si la case sélectionnée est adjacente à l'espace vide
        if empty_row is not None and empty_col is not None:
            if (abs(row - empty_row) + abs(col - empty_col)) == 1:
                # Échange des positions
                self.grid[empty_row][empty_col], self.grid[row][col] = (
                    self.grid[row][col],
                    self.grid[empty_row][empty_col],
                )

    def swap_tiles(self, row1, col1, row2, col2):
        """Échange deux cases sélectionnées."""
        self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]

    def is_solved(self):
        """Vérifie si le puzzle est résolu."""
        # Crée l'ordre correct des morceaux avec l'espace vide à la fin
        correct_order = self.initialGrid.copy()  
        # correct_order.append(None)  # Ajoutez l'espace vide à la fin
        # Applatir la grille actuelle
        flat_grid = [tile for row in self.grid for tile in row]
        flat_grid.pop()
        return flat_grid == correct_order  # Compare si la grille actuelle correspond à l'ordre correct

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
    grid_size = 8  # Exemple de taille de puzzle (4x4)
    swap_interval = 5  # Intervalle pour passer en mode swap
    game = GamePuzzle(grid_size, swap_interval, "paysage.jpg")
    game.run()
