from Piece import *
from EtatEchecs import *


class Roi(Piece):

  def __init__(self,position,est_blanc) : 
    super().__init__(position,est_blanc)
    #self.est_echec = est_echec
    self.nom = 'R' if est_blanc else 'r'

  def coups_possibles(self,etat) -> list:
    x = self.position[0]
    y = self.position[1]
    coups = []

    '''
    Yacine : g mit ton code en commentaire puisque en le testant ce ne fonctionne pas, g mit a la place le code de la reine 
             si tarrive a ameliorer le tiens pour quil puisse marcher ou si tu penses que ya des choses a ameliorer dit le moi 
    for a in [x-1,x,x+1] : 
      for b in [y-1,y,y+1] : 
        mouv = etat.plateau[(a,b)]
        if mouv is None or mouv.est_blanc != self.est_blanc:
          coups.append((a,b))
    '''
    
    for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
      if etat.est_case(x+i,y+j) and not (x+i,y+j) in etat.plateau:
        coups.append((x+i,y+j))

    return coups
  
  def est_echec(self, etat):
    '''verifie si le roi est en echec'''
    if self.position in []:
      pass