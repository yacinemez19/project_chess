from Piece import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Cavalier import *


import copy

class Roi(Piece):

  def __init__(self,position : tuple,est_blanc) : 
    super().__init__(position,est_blanc)
    self.nom = 'R' if est_blanc else 'r'
    self.valeur = 0

  def coups_possibles(self, etat, verif_echec : bool = False) -> set:
    '''
    methode qui test les coups possibles en testant si cela met le roi en echec
    '''
    x, y = self.position
    plateau = etat.plateau
    coups = set()
    deplacements = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]
    for i, j in deplacements:
      piece_en_prise = plateau.get((x+i,y+j), None)
      if etat.est_case(x+i,y+j) and (not piece_en_prise or piece_en_prise.est_blanc != self.est_blanc):   
        if not verif_echec or not self.met_en_echec(etat,tuple(self.position), (x+i,y+j)):
          coups.add((x+i,y+j))

    return coups

  def est_echec(self, etat : EtatEchecs):
    '''verifie si le roi est en echec'''
    #recherche de dame et de tour sur les droites horizontales et verticales
    x, y = self.position
    plateau = etat.plateau
    for i, j in ((1,0),(-1,0),(0,1),(0,-1)):    
      n = 1
      new_x, new_y = x + i, y + j
      piece_visee = plateau.get((new_x, new_y), None)
      while etat.est_case(new_x, new_y) and not piece_visee:
        n += 1
        new_x, new_y = x + i*n, y + j*n
        piece_visee = plateau.get((new_x, new_y), None)
        
      if piece_visee and piece_visee.est_blanc != self.est_blanc and (isinstance(piece_visee, Tour) or isinstance(piece_visee, Dame)):
        return True
      
    #recherche de dame et de fou sur les diagonales
    for i in [-1,1]:
      for j in [1,-1]:
        n = 1
        new_x, new_y = x + i, y + j
        piece_visee = plateau.get((new_x, new_y), None)
        while etat.est_case(new_x, new_y) and not piece_visee:
          n += 1
          new_x, new_y = x + i*n, y + j*n
          piece_visee = plateau.get((new_x, new_y), None)
          
        if piece_visee and piece_visee.est_blanc != self.est_blanc and (isinstance(piece_visee, Fou) or isinstance(piece_visee, Dame)):
          return True
    
    #recherche de cavalier sur les "L"
    for i in [1, -1]:
      for j in [2, -2]:
        new_x, new_y = x + i, y + j
        piece_visee = plateau.get((new_x, new_y), None)
        if piece_visee and piece_visee.est_blanc != self.est_blanc and isinstance(piece_visee, Cavalier):
          return True
        new_x, new_y = x + j, y + i
        piece_visee = plateau.get((new_x, new_y), None)
        if piece_visee and piece_visee.est_blanc != self.est_blanc and isinstance(piece_visee, Cavalier):
          return True
        
    #recherche du roi adverse autour du roi
    n = 1
    deplacements = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]
    for i, j in deplacements:
      new_x, new_y = x + i, y + j
      piece_visee = plateau.get((new_x, new_y), None)
      #on ne teste pas si la piece est de differente couleur puisqu'en principe il n'y a qu'un seul roi
      if piece_visee and isinstance(piece_visee, Roi):
        return True
      
    #recherche d'un pion sur les 2 case diagonales
    dir = 1 if self.est_blanc else -1
    pion_gauche, pion_droit = plateau.get((x+1, y+dir), None), plateau.get((x-1, y+dir), None)
    return (pion_gauche and isinstance(pion_gauche, Pion) and pion_gauche.est_blanc != self.est_blanc) or (pion_droit and isinstance(pion_droit, Pion) and pion_droit.est_blanc != self.est_blanc)

        
        
    
  def met_en_echec(self, etat : EtatEchecs, old_pos : tuple, new_pos : tuple):
    '''
    Méthode qui vérifie si un coup joué par un joueur met son propre roi en échec
    :param etat: etat du jeu
    :param old_pos: ancienne position de la piece
    :param new_pos: nouvelle position de la piece

    :return: vrai si le roi est mis en echec par le coup
    '''
    if old_pos not in etat.plateau:
      raise AttributeError('Erreur dans la position de la piece')
    etat1 = etat.copie_peu_profonde()
    piece = copy.copy(etat1.plateau.pop(old_pos))
    piece.position = new_pos
    etat1.plateau[new_pos] = piece
    if isinstance(piece, Roi):
      #si la piece est le roi alors est_echec doit verifier si le roi a la nouvelle position est mit en echec sans changer la position du vrai roi
      return piece.est_echec(etat1)
    return self.est_echec(etat1)
  
  def __str__(self):
    if self.nom == "R" :
      return "♔"
    else : 
      return "♚"