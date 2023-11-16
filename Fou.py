from Piece import *
from EtatEchecs import *
 

class Fou(Piece):
    def __init__(self, position : tuple, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'
        self.valeur = 3 if est_blanc else -3

    def coups_possibles(self, etat, verif_echec = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x = self.position[0]
        y = self.position[1]
        coups = set()

        #fait un while
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n)))
                n+=1
            piece_en_prise = etat.plateau.get((x+(i*n),y+(j*n)), None)
            if piece_en_prise is not None and piece_en_prise.est_blanc != self.est_blanc:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n))) 
        return coups

    def __str__(self):
        if self.nom == "F" :
            return "♗"
        else : 
            return "♝"
                
        