import pygame

from node import Node

class Fanorona:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    LINE_COLOR = (0, 0, 0)
    BG_COLOR = (220, 220, 220)
    PIECE_COLOR_1 = (200, 0, 0)
    PIECE_COLOR_2 = (0, 0, 200)
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
        self.state = Node()
        self.pieces_count = {1: 0, 2: 0}
        self.selected_piece = None
        self.placing_pieces = True  # Flag pour savoir si on est dans la phase de placement des pièces

    def draw_board(self):
        self.screen.fill(self.BG_COLOR)

        # Dessiner le quadrillage
        for x1, y1 in self.GRID_POS:
            for x2, y2 in self.GRID_POS:
                if abs(x1 - x2) == 200 and y1 == y2:  # Lignes horizontales
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x1, y1), (x2, y2), 3)
                if abs(y1 - y2) == 200 and x1 == x2:  # Lignes verticales
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x1, y1), (x2, y2), 3)

        pygame.draw.line(self.screen, self.LINE_COLOR, self.GRID_POS[0], self.GRID_POS[8], 3)
        pygame.draw.line(self.screen, self.LINE_COLOR, self.GRID_POS[2], self.GRID_POS[6], 3)

        # Dessiner les pièces
        for i, pos in enumerate(self.GRID_POS):
            if self.state.player1_board & (1 << i):
                pygame.draw.circle(self.screen, self.PIECE_COLOR_1, pos, 30)
            elif self.state.player2_board & (1 << i):
                pygame.draw.circle(self.screen, self.PIECE_COLOR_2, pos, 30)

        if self.selected_piece is not None:
            x, y = self.GRID_POS[self.selected_piece]
            pygame.draw.circle(self.screen, self.SELECT_COLOR, (x, y), 40, 3)

    def handle_click(self, pos):
        for i, (x, y) in enumerate(self.GRID_POS):
            if (x - 30 <= pos[0] <= x + 30) and (y - 30 <= pos[1] <= y + 30):  # Vérifie le clic sur une intersection
                if self.placing_pieces:
                    if not self.state.is_occupied(i):  # Vérifie que la case est libre
                        if self.pieces_count[self.state.current_player] < self.MAX_PIECES:  # Limite de pièces
                            # Placer la pièce
                            if self.state.current_player == 1:
                                self.state.player1_board |= (1 << i)
                            else:
                                self.state.player2_board |= (1 << i)

                            self.pieces_count[self.state.current_player] += 1
                            self.state.current_player = 3 - self.state.current_player  # Alterne joueur

                            # Si les deux joueurs ont placé 3 pièces, on passe à la phase de déplacement
                            if self.pieces_count[1] == 3 and self.pieces_count[2] == 3:
                                self.placing_pieces = False
                else:
                    print(self.selected_piece)
                    if i == self.selected_piece:
                        self.selected_piece = None
                        return

                    if self.selected_piece is None:
                        # Sélectionner la pièce à déplacer
                        if (self.state.current_player == 1 and self.state.player1_board & (1 << i)) or \
                                (self.state.current_player == 2 and self.state.player2_board & (1 << i)):
                            self.selected_piece = i  # Mémorise la case sélectionnée
                        print(self.selected_piece)
                    else:
                        # Déplacer la pièce, vérifier que la case est un voisin valide
                        neighbors = self.get_neighbors(self.GRID_POS[self.selected_piece])
                        if i in neighbors and not self.state.is_occupied(
                                i):  # Vérifie que la case est libre et un voisin
                            if self.state.current_player == 1:
                                self.state.player1_board = (self.state.player1_board & ~(
                                            1 << self.selected_piece)) | (1 << i)
                            else:
                                self.state.player2_board = (self.state.player2_board & ~(
                                            1 << self.selected_piece)) | (1 << i)

                            self.selected_piece = None  # Réinitialise la sélection
                            self.state.current_player = 3 - self.state.current_player  # Alterne joueur
                            break  # Sort du mode déplacement

    def get_neighbors(self, position):
        """Retourne les voisins adjacents d'une case dans la grille."""
        neighbors = []
        x, y = position

        # Vérifie les voisins horizontaux (gauche/droite)
        for i, (px, py) in enumerate(self.GRID_POS):
            if (x == px and abs(y - py) == 200) or (y == py and abs(x - px) == 200):
                neighbors.append(i)

        # Vérifie les voisins verticaux (haut/bas)
        for i, (px, py) in enumerate(self.GRID_POS):
            if (y == py and abs(x - px) == 200) or (x == px and abs(y - py) == 200):
                neighbors.append(i)
        print(self.GRID_POS , " AND ", position)
        # Ajoute les voisins diagonaux (cas spécifiques des lignes 0-8 et 2-6)
        if position == self.GRID_POS[4]:
            neighbors.append(0)  # Diagonale de 0 à 8
            neighbors.append(2)  # Diagonale de 0 à 8
            neighbors.append(6)  # Diagonale de 0 à 8
            neighbors.append(8)  # Diagonale de 0 à 8
        if (
                position == self.GRID_POS[0]
                or position == self.GRID_POS[2]
                or position == self.GRID_POS[6]
                or position == self.GRID_POS[8]
        ):
            neighbors.append(4)  # Diagonale de 2 à 6

        return neighbors

    def run_ai_turn(self):
        """Fait jouer l'IA en utilisant l'algorithme Minimax."""
        if self.state.current_player == 2:  # L'IA joue
            # Si l'IA est encore dans la phase de placement
            if self.pieces_count[2] < self.MAX_PIECES:
                # Chercher une case vide pour placer une pièce
                for i in range(len(self.GRID_POS)):
                    if not self.state.is_occupied(i):  # Vérifie si la case est libre
                        self.handle_click(self.GRID_POS[i])  # Simuler le clic de l'IA
                        break
            else:
                # L'IA joue normalement (en utilisant Minimax si elle a placé ses pièces)
                best_move = None
                best_score = -float('inf')

                # Recherche du meilleur coup via Minimax
                for successor in self.state.get_successor():
                    score = successor.minimax(3, False)
                    if score > best_score:
                        best_score = score
                        best_move = successor

                # Appliquer le meilleur mouvement trouvé
                if best_move:
                    # Récupère l'index de la pièce sélectionnée et la nouvelle position à partir du meilleur mouvement
                    selected_piece_index = best_move.selected_piece
                    target_position_index = best_move.target_position

                    # Déplacer la pièce de la sélection vers la cible
                    self.selected_piece = selected_piece_index
                    self.handle_click(self.GRID_POS[target_position_index])
                    self.state = best_move  # Met à jour l'état du jeu avec le meilleur mouvement

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(self.pieces_count)
                self.handle_click(event.pos)
        return True

    def run(self):
        running = True
        while running:
            if self.state.current_player == 1:
                running = self.handle_events()  # Au tour du joueur
            else:
                self.run_ai_turn()  # Au tour de l'IA
            self.draw_board()
            pygame.display.flip()
        # while running:
        #     running = self.handle_events()


        pygame.quit()
