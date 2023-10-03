from Piece import *
from EtatEchecs import *
from Echecs import *


class Pion(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'P' if est_blanc else 'p'

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []

        if y == 1 and not etat.plateau.haskey([x, y + 2]):
            coups.append((x,y+2))

        if y != 7 and y != 0 :
            if etat.plateau.haskey((x, y+1)):
                coups.append((x, y+1))
            if etat.plateau.haskey((x+1, y+1)) and etat.plateau(x+1,y+1).est_blanc != self.est_blanc:
                coups.append((x+1,y+1))
            if etat.plateau.haskey((x+1,y-1)) and etat.plateau(x+1,y-1).est_blanc != self.est_blanc:
                coups.append((x+1,y-1))