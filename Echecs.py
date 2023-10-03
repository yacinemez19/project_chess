from Jeu import *

class Echecs(Jeu) : 

    def traduire(self, mouvement) : 
      colonnes =  {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}
      mouv_str = [x.strip() for x in mouvement.split()]
      try: 
        if mouv_str[0] in colonnes : 
          position1 = (colonnes[mouv_str[0]],int(mouv_str[1]))
          position2 = (colonnes[mouv_str[2]],int(mouv_str[3]))
          assert int(mouv_str[1]) < 8 and int(mouv_str[3]) < 8
        else :  
          position1 = (colonnes[mouv_str[1]],int(mouv_str[2]))
          position2 = (colonnes[mouv_str[3]],int(mouv_str[4]))
          assert int(mouv_str[2]) < 8 and int(mouv_str[4]) < 8    
      except: 
        return "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture. Pour plus d'informations sur le format, appeler help"   
      return [position1, position2]
  
    def deplacer(self, mouvement, etat) : 
      e1 = copy.deepcopy(etat)
      mouv = self.traduire(mouvement)
      a = e1.plateau[(mouv[0])].pop()
      e1.plateau[(mouv[1])] = a
      e1.est_blanc = not(e1.est_blanc)
      return e1
      
    def mouvements_autorises(self, etat, joueur) : 
      mouvs = []
      for (x,y) in etat.mouvements : 
        if (x,y) in self.liste_coups_possibles(joueur, etat) : 
          for (a,b) in self.liste_coups_possibles(joueur, etat)[x,y] : 
            mouvs.append((a,b),(x,y))

      return mouvs
        
    def valeur(self, etat, joueur) :
        sum_valeur = 0
        for piece in etat.plateau : 
            if piece.est_blanc == joueur :
                sum_valeur += piece.valeur

        return sum_valeur
                
    def etat_final(self, etat) : 
        
        for piece in etat.plateau.values() : 
            if isinstance(piece, Roi) :
                etat_final = piece.est_echec and piece.coups_possibles == []
                
        etat_final = self.mouvements_autorises(etat, joueur) == None
        
        if len(etat.plateau.keys()) <= 4 : 
            compteur_blanc = 0
            for x in etat.plateau.keys() : 
                if x.est_blanc : 
                    compteur_blanc += 1
                    
            if compteur_blanc <= 2 : 
                for a in etat.plateau.values():
                    liste = isinstance(a, Roi) or isinstance(a, Cavalier) or isinstance(a, Fou)
                etat_final = False not in liste
                
            couleurs_C = []
            for a in etat.plateau.values():
                if isinstance(a, Cavalier) : 
                    couleurs_C.append(a.est_blanc)
            if len(couleurs_C) == 2 and couleurs_C[0] == couleurs_C[1] : 
                etat_final = True

    def liste_coups_possibles(self, est_blanc) :
      coups = {}
      for position, piece in self.plateau.items() : 
        if piece.est_blanc == est_blanc : 
          coups[position] = set()
          if position in piece.coups_possibles(self) : 
            coups[position].append(piece.nom)

      return coups
    
