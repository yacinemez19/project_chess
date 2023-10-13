from Piece import *
from EtatEchecs import *

class Tour(Piece):
    def __init__(self, position : tuple, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'T' if est_blanc else 't'
        self.valeur = 5

    def coups_possibles(self, etat) -> set:
        x = self.position[0]
        y = self.position[1]
        coups = set()

        for i,j in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                coups.add((x+(i*n),y+(j*n)))
                n+=1
            piece_en_prise = etat.plateau.get((x+(i*n),y+(j*n)), None)
            if piece_en_prise is not None and piece_en_prise.est_blanc != self.est_blanc:
                coups.add((x+(i*n),y+(j*n))) 

        return coups
