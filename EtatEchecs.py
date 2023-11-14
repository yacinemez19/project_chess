from __future__ import annotations
from EtatJeu import EtatJeu


class EtatEchecs(EtatJeu):
    def __init__(self, Joueur: bool, Valeur: int, Plateau):
        self.est_blanc = Joueur
        self.Valeur = Valeur
        self.plateau = Plateau
        self.roi_blanc = None
        self.roi_noir = None
        self.mouvements = None

    def copie_peu_profonde(self):
        new_state = EtatEchecs(self.est_blanc, self.Valeur, dict(self.plateau))
        new_state.roi_blanc = self.roi_blanc 
        new_state.roi_noir = self.roi_noir
        return new_state

    def __str__(self):
      txt = ''
      for y in range(8):
        for x in range(8):
          p = self.plateau.get((x,7-y), '.')
          txt += str(p) + ' | '
        txt += '\n'
      return txt
    
    def __repr__(self):
      txt = ''
      for y in range(8):
        for x in range(8):
          p = self.plateau.get((x,7-y), '.')
          txt += str(p)
        txt += '\n'
      txt += str(self.est_blanc)
      return txt

    def __eq__(self, other : EtatEchecs) -> bool:
      return self.plateau == other.plateau and self.est_blanc == other.est_blanc
    
    def __ne__(self, other : EtatEchecs) -> bool:
       return not self.__eq__(other)
    
    def __hash__(self) -> int:
        # Utilisez une combinaison des valeurs de hachage des attributs nécessaires
        return hash((frozenset(self.plateau.items()), self.est_blanc))

    '''
    def __str__(self):
      txt = ''
      for y in range(7, -1, -1):
        txt+=str(y+1)+' '
        for x in range(8):
          p = self.plateau.get((x,y), '.')
          txt += str(p)
        txt += '\n'
      txt += '  abcdefgh'
      return txt
    '''

    @staticmethod
    def est_case(x,y):
       '''
       retourne vrai si (x,y) representent les coordonnees d'une case sur le plateau
       '''
       return 0<=x<=7 and 0 <= y <= 7