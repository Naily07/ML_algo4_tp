class Node:
    """Représente un état du jeu avec bitboards."""

    def __init__(self, player1_board=0, player2_board=0, current_player=1):
        self.player1_board = player1_board  # Bitboard pour le joueur 1
        self.player2_board = player2_board  # Bitboard pour le joueur 2
        self.current_player = current_player

    def is_occupied(self, pos):
        """Vérifie si une position est occupée par un des joueurs."""
        return (self.player1_board | self.player2_board) & (1 << pos)

    def get_successor(self):
        """Génère tous les états possibles après un coup valide."""
        successors = []
        for i in range(9):
            if not self.is_occupied(i):  # Vérifie si la case est libre
                new_p1, new_p2 = self.player1_board, self.player2_board
                if self.current_player == 1:
                    new_p1 |= (1 << i)  # Ajoute une pièce du joueur 1
                else:
                    new_p2 |= (1 << i)  # Ajoute une pièce du joueur 2

                successors.append(Node(new_p1, new_p2, 3 - self.current_player))
        return successors

    def move_piece(self, from_pos, to_pos):
        """Déplace une pièce d'une position à une autre, et met à jour l'état."""
        # Vérification si la case de départ est occupée par le joueur courant
        if self.current_player == 1 and not (self.player1_board & (1 << from_pos)):
            raise ValueError(f"Le joueur 1 n'a pas de pièce à la position {from_pos}")
        elif self.current_player == 2 and not (self.player2_board & (1 << from_pos)):
            raise ValueError(f"Le joueur 2 n'a pas de pièce à la position {from_pos}")

        # Vérification si la case d'arrivée est vide
        if self.is_occupied(to_pos):
            raise ValueError(f"La position {to_pos} est déjà occupée.")

        # Effacer la pièce de l'ancienne position (en la retirant du bitboard)
        if self.current_player == 1:
            self.player1_board &= ~(1 << from_pos)  # Enlève la pièce du joueur 1
        else:
            self.player2_board &= ~(1 << from_pos)  # Enlève la pièce du joueur 2

        # Met à jour la position de la pièce sur la nouvelle case
        if self.current_player == 1:
            self.player1_board |= (1 << to_pos)  # Ajoute la pièce du joueur 1 à la nouvelle position
        else:
            self.player2_board |= (1 << to_pos)  # Ajoute la pièce du joueur 2 à la nouvelle position

        # Change de joueur
        self.current_player = 3 - self.current_player

    def evaluate(self):
        """Évalue l'état actuel du jeu pour déterminer la faveur du joueur courant."""
        if self.is_winner(1):  # Si le joueur 1 gagne
            return 10
        elif self.is_winner(2):  # Si le joueur 2 gagne
            return -10
        return 0  # Pas de gagnant encore

    def is_winner(self, player):
        """Vérifie si le joueur a gagné."""
        # En fonction de la règle du jeu, ajouter les conditions de victoire
        # Exemple : Si un joueur a toutes ses pièces sur des cases spécifiques, il gagne.
        return False  # Cette fonction doit être personnalisée selon les règles de Fanorona

    def minimax(self, depth, is_maximizing_player):
        """Retourne la meilleure valeur selon l'algorithme Minimax."""
        score = self.evaluate()

        # Si un joueur a gagné ou si la profondeur maximale est atteinte
        if score == 10 or score == -10:
            return score

        # Si la grille est pleine (plus de coups possibles)
        if all(self.is_occupied(i) for i in range(9)):
            return 0

        if is_maximizing_player:
            best = -float('inf')
            for successor in self.get_successor():
                best = max(best, successor.minimax(depth - 1, False))
            return best
        else:
            best = float('inf')
            for successor in self.get_successor():
                best = min(best, successor.minimax(depth - 1, True))
            return best

    def find_best_move(self):
        """Retourne le meilleur coup pour le joueur courant selon Minimax."""
        best_val = -float('inf')
        best_move = None

        for successor in self.get_successor():
            move_val = successor.minimax(3, False)  # Profondeur maximale de 3 pour l'IA
            if move_val > best_val:
                best_move = successor
                best_val = move_val

        return best_move

    def __repr__(self):
        """Affiche le bitboard sous forme de grille pour debug."""
        grid = ['.' if not self.is_occupied(i) else ('X' if (self.player1_board & (1 << i)) else 'O')
                for i in range(9)]
        return f"\n{grid[0]} {grid[1]} {grid[2]}\n{grid[3]} {grid[4]} {grid[5]}\n{grid[6]} {grid[7]} {grid[8]}"
