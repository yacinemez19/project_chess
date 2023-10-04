from Piece import *
from EtatEchecs import *

class Fou(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'
        self.valeur = 3

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []
        
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                coups.append((x+(i*n),y+(j*n)))
                n+=1
        return coups

                
        