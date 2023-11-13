from Piece import *
from EtatEchecs import *
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
    x = self.position[0]
    y = self.position[1]
    coups = set()
    for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
      piece_en_prise = etat.plateau.get((x+i,y+j), None)
      if etat.est_case(x+i,y+j) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):   
        if not verif_echec or not self.met_en_echec(etat,tuple(self.position), (x+i,y+j)):
          coups.add((x+i,y+j))

    return coups
  
  def coups_adverses(self, etat):
    '''
    methode utile qui renvoie les coups adverses possibles, utile pour la methode est echec
    :param etat: etat du jeu

    :return: set avec tous les coups adverses possibles
    '''
    coups = set()
    for position, piece in etat.plateau.items() : 
      if piece.est_blanc != self.est_blanc : 
        coups |= piece.coups_possibles(etat, False)
    return coups  

  def est_echec(self, etat : EtatEchecs):
    '''verifie si le roi est en echec'''
    return tuple(self.position) in self.coups_adverses(etat)
    
  def met_en_echec(self, etat : EtatEchecs, old_pos : tuple, new_pos : tuple):
    '''
    methode qui verifie si un coup joue par un joueur met son propre roi en echec
    :param etat: etat du jeu
    :param old_pos: ancienne position de la piece
    :param new_pos: nouvelle position de la piece

    :return: vrai si le roi est mis en echec par le coup
    '''
    if old_pos not in etat.plateau:
      raise AttributeError('Erreur dans la position de la piece')
    etat1 = etat.copie_peu_profonde()
    piece = copy.copy(etat1.plateau.pop(old_pos))
    piece.position = list(new_pos)
    etat1.plateau[new_pos] = piece
    if isinstance(piece, Roi):
      #si la piece est le roi alors est_echec doit verifier si le roi a la nouvelle position est mit en echec sans changer la position du vrai roi
      return piece.est_echec(etat1)
    return self.est_echec(etat1)