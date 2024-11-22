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
pygame.display.set_caption("Puzzle 3x3")
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
            move_tile(grid, row, col)
            move_count += 1  # Incrémenter le compteur de mouvements

            # Effectuer un swap si le mouvement actuel est un multiple de k
            if move_count % k == 0:
                # Rechercher deux cases adjacentes non vides pour le swap
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE - 1):
                        if grid[r][c] != 0 and grid[r][c + 1] != 0:
                            swap_tiles(grid, r, c, r, c + 1)
                            break
                    else:
                        continue
                    break

    if is_solved(grid):
        print(f"Félicitations ! Vous avez résolu le puzzle en {move_count} mouvements.")
        running = False

pygame.quit()
