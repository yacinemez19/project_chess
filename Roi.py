from Piece import *
from EtatEchecs import *
import copy

class Roi(Piece):

  def __init__(self,position : tuple,est_blanc) : 
    super().__init__(position,est_blanc)
    #self.est_echec = est_echec
    self.nom = 'R' if est_blanc else 'r'

  def coups_possibles(self,etat) -> set:
    x = self.position[0]
    y = self.position[1]
    coups = set()
    for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
      if etat.est_case(x+i,y+j) and not (x+i,y+j) in etat.plateau:
        coups.add((x+i,y+j))

    return coups
  
  def coups_adverses(self, etat):
    '''
    methode utile qui renvoie les coups adverses possibles, utile pour la methode est echec
    :param etat: etat du jeu

    :return: set avec tous les coups adverses possibles
    '''
    coups = set()
    for piece in etat.plateau.values() : 
      if piece.est_blanc != self.est_blanc : 
        coups = coups | piece.coups_possibles(etat)
    return coups  

  def est_echec(self, etat : EtatEchecs):
    '''verifie si le roi est en echec'''
    if tuple(self.position) in self.coups_adverses(etat):
      return True
    
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
    etat1 = copy.deepcopy(etat)
    piece = etat1.plateau.pop(old_pos)
    etat1.plateau[new_pos] = piece
    if old_pos not in etat.plateau:
      print('depression')
    return self.est_echec(etat1)