class Roi(Piece):

  def __init__(self,position,est_blanc,est_echec) : 
    super().__init__(position,est_blanc)
    self.est_echec = est_echec
    self.nom = 'P' if est_blanc else 'p'

  def coups_possibles(self,etat) -> list:
    x = self.position[0]
    y = self.position[1]
    coups = []

    for a in [x-1,x,x+1] : 
      for b in [y-1,y,y+1] : 
        mouv = etat.plateau(a,b)
        if mouv is None or mouv.est_blanc != self.est_blanc:
      coups.append((a,b))

    return coups
    

  def est_possible(self,position) : 
    return position in coups_possibles(self)
