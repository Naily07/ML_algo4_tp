class Node:
    """Représente un état du jeu Fanorona Telo avec bitboards et Minimax."""

    WINNING_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Lignes horizontales
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Lignes verticales
        (0, 4, 8), (2, 4, 6)              # Diagonales
    ]

    def __init__(self, player1_board=0, player2_board=0, current_player=1, placed_pieces=(0, 0)):
        self.player1_board = player1_board  # Bitboard pour le joueur 1
        self.player2_board = player2_board  # Bitboard pour le joueur 2
        self.current_player = current_player
        self.placed_pieces = placed_pieces  # (nb_pieces_J1, nb_pieces_J2)

    def is_occupied(self, pos):
        """Vérifie si une position est occupée par un des joueurs."""
        return (self.player1_board | self.player2_board) & (1 << pos)

    def is_winner(self, player):
        """Vérifie si un joueur a gagné."""
        board = self.player1_board if player == 1 else self.player2_board
        return any((board & (1 << a)) and (board & (1 << b)) and (board & (1 << c)) for a, b, c in self.WINNING_LINES)

    def evaluate(self):
        """Évalue l'état actuel du jeu."""
        if self.is_winner(1):
            return 10
        elif self.is_winner(2):
            return -10
        return 0

    def get_valid_moves(self):
        """Retourne les coups valides (placement ou déplacement)."""
        moves = []
        p1_count, p2_count = self.placed_pieces

        if p1_count < 3 or p2_count < 3:  # Phase de placement
            for i in range(9):
                if not self.is_occupied(i):
                    moves.append(("place", i))
        else:  # Phase de déplacement
            board = self.player1_board if self.current_player == 1 else self.player2_board
            for i in range(9):
                if board & (1 << i):  # Si c'est une pièce du joueur courant
                    for j in self.get_adjacent_positions(i):
                        if not self.is_occupied(j):  # Si la case est libre
                            moves.append(("move", i, j))
        return moves

    def get_adjacent_positions(self, pos):
        """Retourne les positions adjacentes autorisées pour un déplacement."""
        adjacent_map = {
            0: [1, 3, 4], 1: [0, 2, 4], 2: [1, 4, 5],
            3: [0, 4, 6], 4: [0, 1, 2, 3, 5, 6, 7, 8], 5: [2, 4, 8],
            6: [3, 4, 7], 7: [4, 6, 8], 8: [4, 5, 7]
        }
        return adjacent_map[pos]

    def get_successors(self):
        """Génère tous les états possibles après un coup valide."""
        successors = []
        for move in self.get_valid_moves():
            if move[0] == "place":  # Placement d'une pièce
                pos = move[1]
                new_p1, new_p2 = self.player1_board, self.player2_board
                p1_count, p2_count = self.placed_pieces

                if self.current_player == 1:
                    new_p1 |= (1 << pos)
                    p1_count += 1
                else:
                    new_p2 |= (1 << pos)
                    p2_count += 1

                successors.append(Node(new_p1, new_p2, 3 - self.current_player, (p1_count, p2_count)))

            elif move[0] == "move":  # Déplacement d'une pièce
                from_pos, to_pos = move[1], move[2]
                new_p1, new_p2 = self.player1_board, self.player2_board

                if self.current_player == 1:
                    new_p1 &= ~(1 << from_pos)
                    new_p1 |= (1 << to_pos)
                else:
                    new_p2 &= ~(1 << from_pos)
                    new_p2 |= (1 << to_pos)

                successors.append(Node(new_p1, new_p2, 3 - self.current_player, self.placed_pieces))

        return successors

    def minimax(self, depth, is_maximizing):
        """Retourne la meilleure valeur selon l'algorithme Minimax."""
        score = self.evaluate()
        if score in [10, -10] or depth == 0:
            return score

        if is_maximizing:
            best = -float('inf')
            for successor in self.get_successors():
                best = max(best, successor.minimax(depth - 1, False))
            return best
        else:
            best = float('inf')
            for successor in self.get_successors():
                best = min(best, successor.minimax(depth - 1, True))
            return best

    def find_best_move(self):
        """Retourne le meilleur coup pour le joueur courant selon Minimax."""
        best_move = None
        best_val = -float('inf') if self.current_player == 1 else float('inf')

        for successor in self.get_successors():
            move_val = successor.minimax(3, self.current_player == 2)
            if (self.current_player == 1 and move_val > best_val) or (self.current_player == 2 and move_val < best_val):
                best_val = move_val
                best_move = successor

        return best_move

    def __repr__(self):
        """Affiche l'état du jeu."""
        grid = ['.' if not self.is_occupied(i) else ('X' if self.player1_board & (1 << i) else 'O') for i in range(9)]
        return f"\n{grid[0]} {grid[1]} {grid[2]}\n{grid[3]} {grid[4]} {grid[5]}\n{grid[6]} {grid[7]} {grid[8]}"

# === BOUCLE DE JEU ===
# def play():
#     """Boucle pour jouer contre l'IA."""
#     game = Node()
#     while True:
#         print(game)

#         if game.is_winner(1):
#             print("Joueur 1 (X) gagne !")
#             break
#         elif game.is_winner(2):
#             print("Joueur 2 (O) gagne !")
#             break

#         if game.current_player == 1:  # Joueur humain
#             move_type = "move" if game.placed_pieces[0] + game.placed_pieces[1] == 6 else "place"
#             if move_type == "place":
#                 print( game.placed_pieces[0] + game.placed_pieces[1])
#                 pos = int(input("Position (0-8) : "))
#                 game = Node(game.player1_board | (1 << pos), game.player2_board, 2, (game.placed_pieces[0] + 1, game.placed_pieces[1]))
#             elif move_type == "move":
#                 from_pos, to_pos = map(int, input("De où à où (ex: 3 4): ").split())
#                 game = game.find_best_move()
#         else:  # IA joue
#             print("L'IA réfléchit...")
#             game = game.find_best_move()

# play()
