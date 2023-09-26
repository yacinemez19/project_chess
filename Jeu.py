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
    def __repr__(self):
        pass
    def __str__(self):
        pass