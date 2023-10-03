class Echecs(Jeu) : 

  

  def liste_coups_possibles(self, est_blanc) :
    coups = {}
    for position, piece in self.plateau.items() : 
      if piece.est_blanc == est_blanc : 
        coups[position] = set()
        if position in piece.coups_possibles(self) : 
          coups[position].append(piece.nom)

    return coups
    
