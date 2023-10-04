from EtatJeu import EtatJeu

class EtatEchecs(EtatJeu):
    def __init__(self, Joueur: bool, Valeur: int, Plateau: dict, Mouvements: list):
        self.est_blanc = Joueur
        self.Valeur = Valeur
        self.plateau = Plateau
        Mouvements = self.mouvements = [(x,y) for x in range(8) for y in range (8)]

    def __repr__(self):
      txt = ''
      for x in range(8):
        for y in range(8):
          p = self.plateau.get((x,y), '.')
          txt += str(p)
      return txt

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

    def liste_coups_possibles(self) : 
        pass