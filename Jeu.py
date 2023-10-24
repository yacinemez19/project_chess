class Jeu:
    """ 
      Cette classe est destinee a etre heritee par les
    jeux concrets consideres.
    """
    def mouvements_autorises(self, etat):
        """retourne la liste des mouvents autorises 
         dans etat
        """
        pass
    def deplacer(self, mouvement, etat):
        """retourne l'etat qui resulte de
          mouvement dans etat
        """
        pass          
    def valeur(self, etat, joueur):
        "retourne la valeur de etat pour joueur "
    def est_final(self, etat):
        return not self.mouvements_autorises(etat)
    def joueur(self, etat):
        "retourne le joueur qui doit jouer dans cet etat"
        return etat.doit_jouer
    def suivants(self, etat):
        """retourne  la liste des etats suivants 
           suite aux mouvements autorises
        """
        return [(m, self.deplacer(m, etat))
                for m in self.mouvements_autorises(etat)]
        
    def afficher(self, etat):
        pass

    def joueur_minimax(jeu,etat):
      '''Etant donne un etat de jeu calcule le meilleur mouvement en cherchant en profondeur tous les etats jusqu'aux etats terminaux'''
      j = jeu.joueur(etat)
      # decision minmax #
      tab_suivants = jeu.suivants(etat)
      min_suivants = [min_valeur(s) for (e,s) in tab_suivants]
      M = max( min_suivants )
      mouvement , e = tab_suivants[min_suivants.index(M)]
      return mouvement

    # max valeur #
    def max_valeur(etat) :
      if jeu.est_final(etat):
        return jeu.valeur(etat,j)
      v = −math.inf
      for (m,s) in jeux.suivants(etat) : 
        v = max(v , min_valeur(s))
      return v
  
    # min valeur #
    def min_valeur(etat) :
      if jeu.est_final(etat)
        return jeu.valeur(etat,j)
      v = math.inf
      for (m,s) in jeux.suivants(etat) : 
        v = min(v , min_valeur(s))
      return v
    
    def __repr__(self):
        pass
    def __str__(self):
        pass
