from Piece import *
from EtatEchecs import *
from Roi import *

class Fou(Piece):
    def __init__(self, position : tuple, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'
        self.valeur = 3

    def coups_possibles(self, etat) -> set:
        x = self.position[0]
        y = self.position[1]
        coups = set()
        for p in etat.values :
            if type(p) == Roi and p.est_blanc == self.est_blanc:
                break
        
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                
                coups.add((x+(i*n),y+(j*n)))
                n+=1
        return coups

                
        