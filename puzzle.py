import pygame
import sys
from gameEngine import create_puzzle, move_tile, swap_tiles, is_solved, GRID_SIZE

# Configuration
WINDOW_SIZE = 300
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
FONT_SIZE = 50
BACKGROUND_COLOR = (30, 30, 30)
TILE_COLOR = (100, 150, 200)
TEXT_COLOR = (255, 255, 255)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption(f"Puzzle {GRID_SIZE}x{GRID_SIZE}")
font = pygame.font.Font(None, FONT_SIZE)

def draw_puzzle(grid):
    """Dessine la grille de puzzle sur l'écran."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if tile != 0:  # Ne dessine pas l'espace vide
                pygame.draw.rect(screen, TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
                text = font.render(str(tile), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)

# Initialisation
grid = create_puzzle()
running = True
move_count = 0  # Compteur de mouvements
k = 5  # Intervalle des swaps
swap_mode = False  # Indique si le mode swap est actif
selected_tiles = []  # Cases sélectionnées pour un swap

# Boucle principale
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_puzzle(grid)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE

            if not swap_mode:  # Mode normal : déplacement des cases
                move_tile(grid, row, col)
                move_count += 1

                # Active le mode swap si nécessaire
                if move_count % k == 0:
                    swap_mode = True
                    print("Mode swap activé ! Sélectionnez deux cases à échanger.")

            else:  # Mode swap : sélection des cases
                selected_tiles.append((row, col))
                if len(selected_tiles) == 2:
                    # Effectue le swap
                    r1, c1 = selected_tiles[0]
                    r2, c2 = selected_tiles[1]
                    swap_tiles(grid, r1, c1, r2, c2)
                    selected_tiles.clear()
                    swap_mode = False
                    print("Swap effectué. Retour au mode normal.")

    if is_solved(grid):
        print(f"Félicitations ! Vous avez résolu le puzzle en {move_count} mouvements.")
        running = False

pygame.quit()
