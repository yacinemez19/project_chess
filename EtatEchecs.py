from EtatJeu import EtatJeu

class EtatEchecs(EtatJeu):
    def __init__(self, Joueur: bool, Valeur: int, Plateau: dict):
        self.est_blanc = Joueur
        self.Valeur = Valeur
        self.plateau = Plateau
        self.roi_blanc = None
        self.roi_noir = None
        #Mouvements = self.mouvements = [(x,y) for x in range(8) for y in range (8)]

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
      txt += self.est_blanc
      return txt

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

    def liste_coups_possibles(self) : 
        pass