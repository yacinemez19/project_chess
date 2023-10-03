from Piece import *
from EtatEchecs import *
from Echecs import *


class Pion(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'P' if est_blanc else 'p'
        self.est_premier_coup = position.y == 1

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []

        if y == 1 and etat.plateau[x][y+2] is None:
            coups.append([x,y+2])

        if y < 7 :
            if etat.plateau[x][y+1] is None:
                coups.append([x][y+1])
            if etat.plateau[x+1][y+1] is not None and etat.plateau[x+1][y+1].est_blanc != self.est_blanc:
                coups.append([x+1][y+1])
            if etat.plateau[x+1][y-1] is not None and etat.plateau[x+1][y-1].est_blanc != self.est_blanc:
                coups.append([x+1][y-1])