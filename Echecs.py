from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *

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

    def liste_coups_possibles(self, etat, est_blanc) :
      coups = {}
      for position, piece in self.plateau.items() : 
        if piece.est_blanc == est_blanc : 
          coups[position] = set()
          if position in piece.coups_possibles(self) : 
            coups[position].append(piece.nom)

      return coups
    
    @staticmethod
    def strEnPiece(c : str, pos : [int, int]):
      '''
      Prend en argument le nom d'une piece et sa position et renvoie la piece
      '''
      est_blanc = c.isupper() #les pieces blanches sont ecrites en majuscule
      c = c.lower()

      if c == 'p':
          return Pion(pos, est_blanc)
      if c == 't':
          return Tour(pos, est_blanc)
      if c == 'c':
          return Cavalier(pos, est_blanc)
      if c == 'f':
          return Fou(pos, est_blanc)
      if c == 'd':
          return Dame(pos, est_blanc)
      if c == 'r':
          return Roi(pos, est_blanc)

    def charger(self, chemin):
        fichier = open(chemin, 'r')
        etatTxt = fichier.read()
        etatTxt = etatTxt.split()
        plateau = dict()
        for i, ligne in enumerate(etatTxt):
            for j, p in enumerate(ligne):
                if p != '.':
                    plateau[j, i] = self.strEnPiece(p, [j, i])
        etat = EtatEchecs(True, 3, plateau, [])
        return etat


Partie = Echecs()

pion = Pion((0,7), True)
print(Partie.charger('test.txt'))
      