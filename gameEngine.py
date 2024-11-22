import random

GRID_SIZE = 3  # Taille par défaut de la grille

class GamePuzzle():
    def __init__(self) -> None:
        
def create_puzzle():
    """Crée une grille mélangée pour le puzzle."""
    tiles = list(range(1, GRID_SIZE**2)) + [0]  # 0 représente l'espace vide
    random.shuffle(tiles)
    return [tiles[i:i + GRID_SIZE] for i in range(0, len(tiles), GRID_SIZE)]

def move_tile(grid, row, col):
    """Déplace une case sélectionnée si elle est adjacente à l'espace vide."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                empty_row, empty_col = r, c
                break
    if (abs(row - empty_row) + abs(col - empty_col)) == 1:
        grid[empty_row][empty_col], grid[row][col] = grid[row][col], grid[empty_row][empty_col]

def swap_tiles(grid, row1, col1, row2, col2):
    """Échange deux cases sélectionnées."""
    grid[row1][col1], grid[row2][col2] = grid[row2][col2], grid[row1][col1]

def is_solved(grid):
    """Vérifie si le puzzle est résolu."""
    correct = list(range(1, GRID_SIZE**2)) + [0]
    flat_grid = [tile for row in grid for tile in row]
    return flat_grid == correct
