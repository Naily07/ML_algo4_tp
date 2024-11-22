class NPuzzleKSwap:
    def __init__(self, n=8, k=5):
        self.n = n
        self.k = k
        self.size = int((n + 1) ** 0.5)  # Taille de la grille
        self.board = self.generate_board()
        self.d = 0
        self.selected_tiles = []  # Tuiles sélectionnées pour le swap

    def generate_board(self):
        """Génère un puzzle initial valide mélangé."""
        tiles = np.array(range(1, self.n + 1 )) + [0]
        tiles = tiles.reshape((3, 3))
        random.shuffle(tiles)
        while not self.is_solvable(tiles):
            random.shuffle(tiles)
        return [tiles[i:i + self.size] for i in range(0, len(tiles), self.size)]