import random
import heapq

def create_puzzle(grid_size):
   while True:
        # Crée une grille mélangée
        tiles = list(range(1, grid_size**2)) + [0]  # 0 représente l'espace vide
        random.shuffle(tiles)
        grid = [tiles[i:i + grid_size] for i in range(0, len(tiles), grid_size)]

        # Vérifie si la grille est solvable
        if is_solvable(grid):
            return grid  # Si la grille est solvable, retourne-la

def move_tile(grid, row, col, grid_size):
    """Déplace une case sélectionnée si elle est adjacente à l'espace vide."""
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == 0:
                empty_row, empty_col = r, c
                break
    if (abs(row - empty_row) + abs(col - empty_col)) == 1:
        grid[empty_row][empty_col], grid[row][col] = grid[row][col], grid[empty_row][empty_col]

def swap_tiles(grid, row1, col1, row2, col2):
    """Échange deux cases sélectionnées."""
    grid[row1][col1], grid[row2][col2] = grid[row2][col2], grid[row1][col1]

def is_solved(grid, grid_size):
    """Vérifie si le puzzle est résolu."""
    correct = list(range(1, grid_size**2)) + [0]
    flat_grid = [tile for row in grid for tile in row]
    return flat_grid == correct

def is_solvable(grid):
    """Vérifie si le puzzle est solvable en fonction des inversions."""
    # Convertir la grille en une liste 1D en excluant le zéro (espace vide)
    tiles = [tile for row in grid for tile in row if tile != 0]

    # Compter le nombre d'inversions
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    # Le puzzle est solvable si le nombre d'inversions est pair
    return inversions % 2 == 0

def manhattan_distance(grid, grid_size):
    """Calcule la somme des distances de Manhattan pour chaque tuile."""
    distance = 0
    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            if value != 0:
                target_row = (value - 1) // grid_size
                target_col = (value - 1) % grid_size
                distance += abs(row - target_row) + abs(col - target_col)
    return distance

def find_empty_tile(grid, grid_size):
    """Trouve la position de la tuile vide (0) dans la grille."""
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 0:
                return row, col

def astar_solver(grid, grid_size):
    """Algorithme A* pour résoudre le puzzle en retournant chaque étape intermédiaire."""
    # Créer l'état de départ avec la distance de Manhattan et 0 comme nombre de mouvements
    start_state = (manhattan_distance(grid, grid_size), 0, grid, [])
    
    # File de priorité pour gérer les états à explorer
    queue = []
    heapq.heappush(queue, start_state)

    # Ensemble pour suivre les états visités
    visited = set()
    visited.add(tuple(tuple(row) for row in grid))

    while queue:
        estimated_cost, moves, current_grid, path = heapq.heappop(queue)

        # Si la grille est résolue, retourner le chemin et le nombre de mouvements
        if is_solved(current_grid, grid_size):
            return path, moves

        empty_row, empty_col = find_empty_tile(current_grid, grid_size)

        # Déplacer les tuiles adjacentes
        for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = empty_row + d_row, empty_col + d_col
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                # Copier l'état actuel
                new_grid = [row[:] for row in current_grid]
                new_grid[empty_row][empty_col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[empty_row][empty_col]
                new_tuple_grid = tuple(tuple(row) for row in new_grid)

                # Si l'état n'a pas encore été visité
                if new_tuple_grid not in visited:
                    visited.add(new_tuple_grid)
                    new_path = path + [new_grid]  # Ajouter le nouvel état au chemin
                    new_cost = moves + 1 + manhattan_distance(new_grid, grid_size)  # Coût = déplacement + heuristique
                    heapq.heappush(queue, (new_cost, moves + 1, new_grid, new_path))

    return [], 0  # Si aucune solution n'est trouvée