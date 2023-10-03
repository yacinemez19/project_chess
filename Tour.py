from Piece import *
from EtatEchecs import *
from Echecs import *

class Pion(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'T' if est_blanc else 't'

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []

        for i,j in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            while 0 <= x <= 7 and 0 <= y <= 7 and not (x, y) in etat.plateau:
                coups.append(x+i, y+j)
