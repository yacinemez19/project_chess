from Piece import *
from EtatEchecs import *
 

class Pion(Piece):
    def __init__(self, position, est_blanc : bool) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'P' if est_blanc else 'p'
        self.valeur = 1 if est_blanc else -1


    def coups_possibles(self, etat : EtatEchecs, verif_echec : bool = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x, y = self.position
        coups = set()
        est_premier_coups = y == 1 if self.est_blanc else y == 6
        dir = 1 if self.est_blanc else -1

        if est_premier_coups and not (x, y+2*dir) in etat.plateau and not (x, y+dir) in etat.plateau:
            if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x,y+(2*dir))):
                coups.add((x,y+(2*dir)))

        if y != 7 and y != 0 :
            #test si le pion peut avancer (ou reculer)
            if not (x, y+dir) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x,y+dir)):
                    coups.add((x, y+dir))

            for i in [-1, 1] :
                if (x+i, y+dir) in etat.plateau and etat.plateau[x+i,y+dir].est_blanc != self.est_blanc:
                    if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+i,y+dir)):
                        coups.add((x+i,y+dir))
        return coups
    
    def __str__(self):
        if self.nom == "P" :
            return "♙"
        else : 
            return "♟︎"
