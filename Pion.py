from Piece import *
from EtatEchecs import *
from Roi import Roi

class Pion(Piece):
    def __init__(self, position, est_blanc : bool) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'P' if est_blanc else 'p'
        self.valeur = 1

    def coups_possibles(self, etat : EtatEchecs) -> set:
        x = self.position[0]
        y = self.position[1]
        coups = set()
        est_premier_coups = y == 1 or y == 6
        dir = 1 if self.est_blanc else -1

        if est_premier_coups and not (x, y + 2) in etat.plateau:
            coups.add((x,y+(2*dir)))

        if y != 7 and y != 0 :
            #test si le pion peut avancer (ou reculer)
            if not (x, y+dir) in etat.plateau:
                coups.add((x, y+dir))

            for i in [-1, 1] :
                if (x+i, y+dir) in etat.plateau and etat.plateau[x+i,y+dir].est_blanc != self.est_blanc:
                    if isinstance(etat.plateau[x+i,y+dir], Roi):
                        print("le roi peut être mangé")
                    coups.add((x+i,y+dir))

        return coups
