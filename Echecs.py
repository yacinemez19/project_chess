from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *
import copy

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
                
        etat_final = self.mouvements_autorises(etat, etat.joueur) == None
        
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

    def liste_coups_possibles(self, etat, est_blanc) :
      coups = {}
      for position, piece in etat.plateau.items() : 
        if piece.est_blanc == est_blanc : 
          if position in piece.coups_possibles(etat) : 
            coups[position] = set()
            coups[position].append(piece.nom)

      return coups  

    @staticmethod
    def str_en_piece(c : str, pos : [int, int]):
      '''
      Prend en argument le nom d'une piece et sa position et renvoie la piece
      '''
      #on verifie que la position donnee existe bien
      #if not etat.est_case(pos[0], pos[1]):
      #   raise AttributeError('La case n\'existe pas')

      est_blanc = c.isupper() #les pieces blanches sont ecrites en majuscule
      c = c.lower()

      #renvoie une piece en fonction du caractere donne
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
        '''
        renvoie l'etat d'une partie a partir du chemin du fichier txt ou elle est stockee

        :param chemin: str donnant le chemin du fichier
        :retur: objet EtatEchecs contenant l'etat charge
        '''
        fichier = open(chemin, 'r')
        etatTxt = fichier.read()
        etatTxt = etatTxt.split()
        plateau = dict()
        for i, ligne in enumerate(etatTxt):
            for j, p in enumerate(ligne):
                if p != '.':
                    x = j
                    y = 7 - i
                    plateau[x, y] = self.str_en_piece(p, [x, y])
        etat = EtatEchecs(True, 3, plateau, [])
        return etat
    
    def afficher(self, etat):
      '''
      affiche le plateau suivant l'etat donne 
      '''
      print(etat)
      return 
    
    def enregister(self, etat, nom) -> None:
      '''
      sauvegarde l'etat de la partie dans un fichier donne
      
      :param etat: etat de la partie a sauvegarder
      :param nom: nom qu'on veut donner au fichier de sauvegarde
      '''
      fichier = open(nom, 'w')
      fichier.write()
      
      return None
