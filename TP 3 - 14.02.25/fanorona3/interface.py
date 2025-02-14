import pygame
from node import Node

class Fanorona:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    LINE_COLOR = (0, 0, 0)
    BG_COLOR = (220, 220, 220)
    PIECE_COLOR_1 = (200, 0, 0)   # Joueur 1
    PIECE_COLOR_2 = (0, 0, 200)   # Joueur 2 (IA)
    SELECT_COLOR = (255, 255, 0)

    GRID_POS = [
        (100, 100), (300, 100), (500, 100),
        (100, 300), (300, 300), (500, 300),
        (100, 500), (300, 500), (500, 500)
    ]

    MAX_PIECES = 3

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Fanorona")
        self.state = Node()  # État initial du jeu
        self.selected_piece = None  # Pour la phase de déplacement
        # La phase de placement est active tant que l'un des joueurs n'a pas placé MAX_PIECES
        self.placing_pieces = (self.state.placed_pieces[0] < self.MAX_PIECES or
                                self.state.placed_pieces[1] < self.MAX_PIECES)

    def update_phase(self):
        """Met à jour le flag de phase en fonction du nombre de pièces placées."""
        self.placing_pieces = (self.state.placed_pieces[0] < self.MAX_PIECES or
                                self.state.placed_pieces[1] < self.MAX_PIECES)

    def draw_board(self):
        self.screen.fill(self.BG_COLOR)

        # Dessiner le quadrillage
        for x1, y1 in self.GRID_POS:
            for x2, y2 in self.GRID_POS:
                if abs(x1 - x2) == 200 and y1 == y2:  # Lignes horizontales
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x1, y1), (x2, y2), 3)
                if abs(y1 - y2) == 200 and x1 == x2:  # Lignes verticales
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x1, y1), (x2, y2), 3)

        # Dessiner les diagonales spécifiques
        pygame.draw.line(self.screen, self.LINE_COLOR, self.GRID_POS[0], self.GRID_POS[8], 3)
        pygame.draw.line(self.screen, self.LINE_COLOR, self.GRID_POS[2], self.GRID_POS[6], 3)

        # Dessiner les pièces en fonction des bitboards de Node
        for i, pos in enumerate(self.GRID_POS):
            if self.state.player1_board & (1 << i):
                pygame.draw.circle(self.screen, self.PIECE_COLOR_1, pos, 30)
            elif self.state.player2_board & (1 << i):
                pygame.draw.circle(self.screen, self.PIECE_COLOR_2, pos, 30)

        # Indiquer la pièce sélectionnée en phase de déplacement
        if self.selected_piece is not None:
            pos = self.GRID_POS[self.selected_piece]
            pygame.draw.circle(self.screen, self.SELECT_COLOR, pos, 40, 3)

    def handle_click(self, pos):
        """
        Interprète le clic de l'utilisateur.
        En phase de placement, si la case cliquée est libre et valide,
        on applique le coup correspondant. En phase de déplacement,
        on sélectionne d'abord une pièce, puis on valide la destination.
        """
        # Déterminer l'index de la case cliquée
        clicked_index = None
        for i, grid_pos in enumerate(self.GRID_POS):
            x, y = grid_pos
            if (x - 30 <= pos[0] <= x + 30) and (y - 30 <= pos[1] <= y + 30):
                clicked_index = i
                break
        if clicked_index is None:
            return

        # Récupérer la liste des coups valides pour l'état actuel
        valid_moves = self.state.get_valid_moves()

        if self.placing_pieces:
            # En phase de placement, le coup doit être ("place", clicked_index)
            if ("place", clicked_index) in valid_moves:
                idx = valid_moves.index(("place", clicked_index))
                successors = self.state.get_successors()
                self.state = successors[idx]
                self.selected_piece = None  # Réinitialise la sélection si nécessaire
                self.update_phase()
        else:
            # En phase de déplacement
            if self.selected_piece is None:
                # Si aucune pièce n'est sélectionnée, vérifier que la case contient une pièce du joueur courant
                if self.state.current_player == 1 and (self.state.player1_board & (1 << clicked_index)):
                    self.selected_piece = clicked_index
                elif self.state.current_player == 2 and (self.state.player2_board & (1 << clicked_index)):
                    self.selected_piece = clicked_index
            else:
                # Une pièce a été sélectionnée : on tente de jouer le coup ("move", selected_piece, clicked_index)
                move_tuple = ("move", self.selected_piece, clicked_index)
                if move_tuple in valid_moves:
                    idx = valid_moves.index(move_tuple)
                    successors = self.state.get_successors()
                    self.state = successors[idx]
                    self.selected_piece = None
                    self.update_phase()
                else:
                    # Si l'utilisateur reclique sur la même pièce, on annule la sélection
                    if clicked_index == self.selected_piece:
                        self.selected_piece = None
                    # Ou, si une autre pièce du joueur est cliquée, on change la sélection
                    elif (self.state.current_player == 1 and (self.state.player1_board & (1 << clicked_index))) or \
                         (self.state.current_player == 2 and (self.state.player2_board & (1 << clicked_index))):
                        self.selected_piece = clicked_index

    def run_ai_turn(self):
        """Fait jouer l'IA (joueur 2) en appliquant un coup via Minimax (find_best_move) pour le placement et le déplacement."""
        if self.state.current_player == 2:
            # Utiliser find_best_move() pour choisir le meilleur coup, quelle que soit la phase.
            best_state = self.state.find_best_move()
            if best_state:
                self.state = best_state
                self.update_phase()
            self.selected_piece = None  # Réinitialiser la sélection

    def handle_events(self):
        """Gestion des événements Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Le joueur humain (joueur 1) ne peut jouer que pendant son tour
                if self.state.current_player == 1:
                    self.handle_click(event.pos)
        return True

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            if self.state.is_winner(1):
                print("Joueur 1 (X) gagne !")
                break
            elif self.state.is_winner(2):
                print("Joueur 2 (O) gagne !")
                break
            running = self.handle_events()
            # Si c'est le tour de l'IA, la laisser réfléchir puis jouer
            if self.state.current_player == 2:
                pygame.time.delay(500)  # Petit délai pour visualiser le tour de l'IA
                self.run_ai_turn()
            self.draw_board()
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

