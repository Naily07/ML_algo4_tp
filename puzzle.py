import pygame
import sys
from gameMenu import menu_selection
from gameEngine import create_puzzle, move_tile, swap_tiles, is_solved, astar_solver

# Configuration de la fenêtre
WINDOW_SIZE = 400
FONT_SIZE = 50
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (100, 150, 200)
TEXT_COLOR = (255, 255, 255)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Puzzle Game")
font = pygame.font.Font(None, FONT_SIZE)

def draw_text(text, x, y, color=TEXT_COLOR, center=True):
    """Affiche du texte centré."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(surface, rect)

def draw_puzzle(grid, grid_size, tile_size):
    """Dessine la grille de puzzle sur l'écran."""
    for row in range(grid_size):
        for col in range(grid_size):
            tile = grid[row][col]
            x, y = col * tile_size, row * tile_size
            if tile != 0:  # Ne dessine pas l'espace vide
                pygame.draw.rect(screen, BUTTON_COLOR, (x, y, tile_size, tile_size))
                draw_text(str(tile), x + tile_size // 2, y + tile_size // 2)

def main():
    # Afficher le menu de sélection
    grid_size, k, is_ai_mode = menu_selection(screen)

    # Configuration dynamique
    tile_size = WINDOW_SIZE // grid_size
    grid = create_puzzle(grid_size)
    move_count = 0
    swap_mode = False
    selected_tiles = []
    ai_generator = None

    if is_ai_mode:
        path, steps_taken = astar_solver(grid, grid_size)  # Obtenez les étapes et le nombre de mouvements
        ai_generator = iter(path)  # Crée un générateur à partir des étapes
        print(f"L'IA résoudra le puzzle en {steps_taken} mouvements.")

    # Boucle principale
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_puzzle(grid, grid_size, tile_size)
        
        pygame.display.flip()

        # Si en mode IA, afficher chaque étape successivement
        if is_ai_mode and ai_generator:
            try:
                grid = next(ai_generator)  # Obtient la prochaine étape
                pygame.time.delay(300)  # Pause pour chaque mouvement
            except StopIteration:
                print(f"L'IA a résolu le puzzle en {steps_taken} mouvements.")
                is_ai_mode = False
                ai_generator = None  # Termine le mode IA

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_ai_mode:
                x, y = event.pos
                col, row = x // tile_size, y // tile_size

                if not swap_mode:  # Mode normal
                    move_tile(grid, row, col, grid_size)
                    move_count += 1

                    if move_count % k == 0:
                        swap_mode = True
                        print("Mode swap activé : sélectionnez deux cases.")

                else:  # Mode swap
                    selected_tiles.append((row, col))
                    if len(selected_tiles) == 2:
                        r1, c1 = selected_tiles[0]
                        r2, c2 = selected_tiles[1]
                        swap_tiles(grid, r1, c1, r2, c2)
                        selected_tiles.clear()
                        swap_mode = False
                        print("Swap effectué. Retour au mode normal.")

        if is_solved(grid, grid_size) and not is_ai_mode:
            print(f"Félicitations ! Résolu en {move_count} mouvements.")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
