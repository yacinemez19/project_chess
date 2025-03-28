from Piece import *
from EtatEchecs import *


class Cavalier(Piece):
  def __init__(self,position : tuple, est_blanc : bool)-> None : 
    super().__init__(position,est_blanc)
    self.nom = 'C' if est_blanc else 'c'
    self.valeur = 3 if est_blanc else -3

  def coups_possibles(self,etat, verif_echec : bool = False) -> set:
    roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
    x = self.position[0]
    y = self.position[1]
    coups = set()

    for a in [-1,1] : 
      for b in [-2,2] : 
        mouv1 = etat.plateau.get((x+a,y+b), None)
        mouv2 = etat.plateau.get((x+b,y+a), None)
        if mouv1 is None or mouv1.est_blanc != self.est_blanc:
          piece_en_prise = etat.plateau.get((x+a,y+b), None)
          if etat.est_case(x+a,y+b) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):
            if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+a,y+b)):
              coups.add((x+a,y+b))
        if mouv2 is None or mouv2.est_blanc != self.est_blanc:
          piece_en_prise = etat.plateau.get((x+b,y+a), None)
          if etat.est_case(x+b,y+a) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):
            if not verif_echec or not roi.met_en_echec(etat,tuple(self.position), (x+b,y+a)):
              coups.add((x+b,y+a))
    return coups
  
  def __str__(self):
    if self.nom == "C" :
      return "♘"
    else : 
      return "♞"
