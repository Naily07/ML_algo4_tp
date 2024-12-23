import heapq

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
    """Algorithme A* pour résoudre le puzzle."""
    start_state = (manhattan_distance(grid, grid_size), 0, grid)  # (coût estimé, nombre de mouvements, grille)
    queue = []
    heapq.heappush(queue, start_state)
    visited = set()
    visited.add(tuple(tuple(row) for row in grid))
    
    while queue:
        estimated_cost, moves, current_grid = heapq.heappop(queue)

        if is_solved(current_grid, grid_size):
            return moves  # Puzzle solved

        empty_row, empty_col = find_empty_tile(current_grid, grid_size)

        # Définir les déplacements possibles pour la tuile vide
        for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = empty_row + d_row, empty_col + d_col
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                # Crée une copie de la grille et applique le déplacement
                new_grid = [row[:] for row in current_grid]
                new_grid[empty_row][empty_col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[empty_row][empty_col]
                new_tuple_grid = tuple(tuple(row) for row in new_grid)

                if new_tuple_grid not in visited:
                    visited.add(new_tuple_grid)
                    new_cost = moves + 1 + manhattan_distance(new_grid, grid_size)
                    heapq.heappush(queue, (new_cost, moves + 1, new_grid))

    return -1  # Si aucune solution n'est trouvée
