from Piece import *
from EtatEchecs import *

class Cavalier(Piece):

  def __init__(self,position,est_blanc) : 
    super().__init__(position,est_blanc)
    self.nom = 'C' if est_blanc else 'c'
    self.valeur = 3

  def coups_possibles(self,etat) -> list:
    x = self.position[0]
    y = self.position[1]
    coups = []

    for a in [-1,1] : 
      for b in [-2,2] : 
        mouv1 = etat.plateau.get([(x+a,y+b)], None)
        mouv2 = etat.plateau.get([(x+b,y+a)], None)
        if mouv1 is None or mouv1.est_blanc != self.est_blanc:
          coups.append((x+a,y+2))
        if mouv2 is None or mouv2.est_blanc != self.est_blanc:
          coups.append((x+2,y+a))

    return coups
