from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *
import copy
# crée des erreurs pour les deux interactions avec l'utilisateur
class InputError1(Exception) : 
  pass

class InputError2(Exception) : 
  pass

class Echecs(Jeu) : 
  def traduire(self, mouvement) :
    colonnes =  ['a','b', 'c', 'd', 'e', 'f', 'g', 'h']
    mouv_str = [x.strip() for x in mouvement]
    
    try: 
      # vérifie qu'il s'agit d'un déplacement
      if mouv_str[0] in colonnes : 
        position1 = (colonnes.index(mouv_str[0]),int(mouv_str[1]))
        position2 = (colonnes.index(mouv_str[3]),int(mouv_str[4]))
        if int(mouv_str[1]) < 8 and int(mouv_str[4]) < 8 :
          raise IndexError
          
      # sinon, si le mouvement est valide, il d'agit d'une capture de pièce
      else :  
        position1 = (colonnes.index(mouv_str[1]),int(mouv_str[2]))
        position2 = (colonnes.index(mouv_str[4]),int(mouv_str[5]))
        if int(mouv_str[2]) < 8 and int(mouv_str[5]) < 8  :
          raise IndexError
        
    except: 
      return "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"   
    
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
              
  def etat_final(self, etat, a, historique) : 

    raison = None

    # vérifie si le joueur a abandonné
    if a == True : 
      etat_final = True
      raison = "abandon"

      # vérifie s'il y a échec et mat
      for piece in etat.plateau.values() : 
        if isinstance(piece, Roi) :
          etat_final = piece.est_echec and piece.coups_possibles == []
          if etat_final == True :
            couleur = piece.est_blanc

      # La raison de l'état final est que le roi est en échec et mat
      if etat_final == True and raison == None:
        if couleur : 
          raison = "Echec et mat blanc"
        else : 
          raison = "Echec et mat noir"

      # etat_final car plus de mouvements autorisés
      etat_final = self.mouvements_autorises(etat, etat.joueur) == None
      if etat_final == True and raison == None:
        raison = "Match nul"

      # état final par manque de matériel
      if len(etat.plateau.keys()) <= 4 : 
        compteur_blanc = 0
        for x in etat.plateau.keys() : 
          if x.est_blanc : 
            compteur_blanc += 1

      # s'il reste moins de 2 pièces au blanc, vérifie la nature des pièces
      if compteur_blanc <= 2 : 
        liste = []
        for a in etat.plateau.values():
          liste = isinstance(a, Roi) or isinstance(a, Cavalier) or isinstance(a, Fou)
        etat_final = False not in liste

      # s'il y a moins de quatre pièces, dont 2 sont des cavaliers de même couleur, fin de partie
      couleurs_C = []
      for a in etat.plateau.values():
        if isinstance(a, Cavalier) : 
          couleurs_C.append(a.est_blanc)
      if len(couleurs_C) == 2 and couleurs_C[0] == couleurs_C[1] : 
        etat_final = True
        

        #règle des trois coups
        for a in historique[::2]:
          for b in historique[1::2] : 
            if (historique[-1],historique[-2]) == (a,b) :
                etat_final == True

        # règle des 50 coups
        coups = []
        for coup,c in historique :
            if coup.lower() != coup :
                coups.append(coup)
                
            elif isinstance(c,Pion) :
                coup.append(coup)
        if coups == [] :
            etat_final = True
            

        if etat_final == True and raison == None:
          raison = "Match nul"
        return [etat_final,raison]

  def liste_coups_possibles(self, etat, est_blanc) :
    coups = {}
    for position, piece in etat.plateau.items() : 
      if piece.est_blanc == est_blanc : 
        if position in piece.coups_possibles(etat) : 
          coups[position] = set()
          coups[position].add(piece.nom)

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
    etat = EtatEchecs(True, 3, plateau, []) #True car quand on charge la partie on sait pas si blanc ou noir commence
    return etat
  
  def afficher(self, etat) -> None:
    '''
    affiche le plateau suivant l'etat donne 
    '''
    etat += '\n'
    etat += 'abcdefgh'
    print(etat)
    return None

  def enregister(self, etat, nom) -> None:
    '''
    sauvegarde l'etat de la partie dans un fichier donne
    
    :param etat: etat de la partie a sauvegarder
    :param nom: nom qu'on veut donner au fichier de sauvegarde
    '''
    fichier = open(nom, 'w')
    fichier.write()
    
    return None

  # recueille les choix de l'utilisateur en début de partie
  def menu(self) :
    print("Menu du jeu d'échecs : ")
    print("Si vous voulez commencer une nouvelle partie, entrez n.")
    print("Si vous voulez reprendre une ancienne partie, entrez a.")
    print("Si vous voulez plus dinformations sur l'utilisation de ce programme, entrez help.")
    choix1 = input()
    choix2 = 0
    if choix1 == "n" or choix1 == "a" : 
      choix2 = input("Voulez-vous jouer contre un autre joueur(entrer j), jouer contre une IA (entrer i) ou faire s'afffronter deux IAs (entrer ii) ?")
      print("La partie va commencer. Si vous voulez quitter sans sauvegarder, entrez quit. Si vous voulez sauvegarder votre partie, entrez save. Si vous voulez plus d'informations sur le programme, entrez help.")
    return [choix1, choix2]

  # le plus important, la méthode à lancer au démarrage du programme pour lancer et mener la partie.
  def debut_partie(self):
    choix1, choix2 = self.menu()
    try : 
      # nouvelle partie
      if choix1 == 'n' : 
        Etat = self.charger(Nouvelle_partie)
        abandon = self.choisir_partie(choix2)[-1]
        self.fin_partie(etat_final(EtatEchecs, abandon, historique))

      # partie chargée
      elif choix1 == 'a' : 
        try : 
            fichier = input("Donnez le chemin du fichier à charger.")
            Etat = self.charger(fichier)
            abandon = self.choisir_partie(choix2)[-1]
        
        except :
            print("Votre chemin n'est pas valide. Si le fichier eset dans le dossier du programme, donnez le nom du fichier. Sinon, donnez le chemin. Pour plus d'informations, allez dans help.")
            self.debut_partie()
        self.fin_partie(etat_final(EtatEchecs, abandon, historique))
            
      # affiche le mode d'emploi
      elif choix1 == help : 
          self.afficher_aide()

      # Si l'input ne fait pas partie des choix, lève une erreur
      else :
          raise InputError1

      # ramène l'utilisateur au menu initial si son choix n'est pas valide
    except InputError1 : 
        print("Votre choix ne fait pas partie des options. Il faut choisir entre n, a et help.")
        self.debut_partie()
    except InputError2 :
        print("Votre choix ne fait pas partie des options. Il faut choisir entre j, i et ii.")
        self.debut_partie()


  # démarre la partie avec les joueurs choisis par l'utilisateur
  def choisir_partie(self,choix) : 
    if choix == 'j' : 
        p = self.partie('humain', 'humain')
    elif choix == 'i' : 
        p = self.partie('humain','IA')
    elif choix == 'ii' : 
        p = self.partie('IA','IA')
    else :
        raise InputError2
    return p
      
  def afficher_aide() : 
    with open("mode_d'emploi.txt",r) as f: 
      for ligne in f : 
        print(ligne)

  def strategie(self,joueur) : 
    if joueur == "humain" : 
      abandon = False
      mouv = input("Quel mouvement voulez-vous jouer ?")
      if mouv == "help" : 
        self.afficher_aide() 
      elif mouv == "quit" : 
        self.menu()
      elif mouv == "abondon" : 
        return None
      else :  
        return mouv
    if joueur == "IA" : 
        pass
    
  # déroulé de la partie
  def partie(self,joueur1, joueur2) : 
    historique = []
    # déroulé de la partie
    while not(Echecs.etat_final(EtatEchecs, mouv, historique)[0]) :
      # règle des 50
      if len(historique) > 50 :
        historique.pop(0)
      if EtatEchecs.est_blanc == True :
        mouv = self.strategie(joueur1)
      else : 
        mouv = self.strategie(joueur2)
      piece_jouee = EtatEchecs.plateau[self.traduire(mouv)[0]]
      historique.append([mouv, piece_jouee])
      return historique
  
  # fin de partie
  def fin_partie(self,raison_etat_final) : 
    print("La partie est terminée.")
    if raison_etat_final == 'Echec et mat blanc' :
      print("Le joueur blanc a gagné la partie.")
    elif raison_etat_final == 'Echec et mat noir' :
      print("Le joueur noir a gagné la partie.")
    elif raison_etat_final == 'Match nul' :
      print("Cette partie se termine par un match nul.")
    elif raison_etat_final == "abandon blanc" :
      print("Le joueur noir a gagné la partie par abandon.")
    elif raison_etat_final == "abandon noir" :
      print("Le joueur blanc a gagné la partie par abandon.")
