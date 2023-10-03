from Piece import *
from EtatEchecs import *
from Echecs import *


class Fou(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'
        self.valeur = 9

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []
        
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
            while 0 <= x+i <= 7 or 0 <= y+j <= 7 and not (x,y) in etat.plateau:
                coups.append(x + i,y + j)