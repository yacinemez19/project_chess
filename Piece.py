class piece:
    def __init__(self, position, est_blanc) -> None:
        self.position = position #prend None si la piece n'est pas sur le plateau
        self.est_blanc = est_blanc
        self.vect_deplacement = None

    def recuperer_nom(self):
        pass

    def coups_possibles(self) -> list:
        pass
