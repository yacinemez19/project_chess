from Piece import *
from EtatJeu import *
from Jeu import *


class Fou(Piece):
    def __init__(self, position, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'

    def coups_possibles(self, etat) -> list:
        x = self.position[0]
        y = self.position[1]
        coups = []
        
        
        if etat.plateau[(x+i,y+i) for i in range(7)] is None:
            coups.append()
                
        