from Piece import *
from EtatEchecs import *
from Roi import *

class Cavalier(Piece):
  def __init__(self,position : tuple, est_blanc : bool)-> None : 
    super().__init__(position,est_blanc)
    self.nom = 'C' if est_blanc else 'c'
    self.valeur = 3 if est_blanc else -3

  def coups_possibles(self,etat, verif_echec : bool = False) -> set:
    roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
    x = self.position[0]
    y = self.position[1]
    coups = set()

    for a in [-1,1] : 
      for b in [-2,2] : 
        mouv1 = etat.plateau.get((x+a,y+b), None)
        mouv2 = etat.plateau.get((x+b,y+a), None)
        if mouv1 is None or mouv1.est_blanc != self.est_blanc:
          piece_en_prise = etat.plateau.get((x+a,y+b), None)
          if etat.est_case(x+a,y+b) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):
            if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+a,y+b)):
              coups.add((x+a,y+b))
        if mouv2 is None or mouv2.est_blanc != self.est_blanc:
          piece_en_prise = etat.plateau.get((x+b,y+a), None)
          if etat.est_case(x+b,y+a) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):
            if not verif_echec or not roi.met_en_echec(etat,tuple(self.position), (x+a,y+b)):
              coups.add((x+b,y+a))
    return coups
  
  def __str__(self):
    if self.nom == "C" :
      return "♘"
    else : 
      return "♞"

from Piece import *
from EtatEchecs import *
from Roi import *

class Dame(Piece):
    def __init__(self, position : tuple, est_blanc : bool) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'D' if est_blanc else 'd'
        self.valeur = 9 if est_blanc else -9

    def coups_possibles(self, etat, verif_echec : bool = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x = self.position[0]
        y = self.position[1]
        coups = set()
        
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n)))
                n+=1
            piece_en_prise = etat.plateau.get((x+(i*n),y+(j*n)), None)
            if piece_en_prise is not None and piece_en_prise.est_blanc != self.est_blanc:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n))) 

        return coups
    
    def __str__(self):
        if self.nom == "D" :
            return "♕"
        else : 
            return "♛"

from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *
from time import time
from os import path
from random import randint
import copy
import sys


# crée des erreurs pour les deux interactions avec l'utilisateur
class InputError1(Exception) : 
  pass

class KingNotFoundError(Exception):
  pass

class InputError2(Exception) : 
  pass

class PieceNotExistError(Exception):
  pass

class MovementImpossibleError(Exception):
  pass

class WrongFileError(Exception):
  pass

class Echecs(Jeu) : 
  _profondeur = 3
  _cache = {}
  _cache_mouvements = {}
  colonnes =  ['a','b', 'c', 'd', 'e', 'f', 'g', 'h']
  
  def traduire(self, mouvement:str) -> list[tuple[int,int]]:
    '''
    Traduis le mouvement du type e2-e4 en liste de tuple
    
    :mouvement: Le mouvement du type e2-e4
    :return: [ancienne position, nouvelle position]
    '''
    mouv_str = [x.strip() for x in mouvement]
    
    try: 
      # vérifie qu'il s'agit d'un déplacement
      if not mouv_str[0] in self.colonnes : 
        raise MovementImpossibleError
      position1 = (self.colonnes.index(mouv_str[0]),int(mouv_str[1])-1)
      position2 = (self.colonnes.index(mouv_str[3]),int(mouv_str[4])-1)
      if int(mouv_str[1]) > 8 or int(mouv_str[4]) > 8 :
        raise IndexError
    except: 
      return "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"   
    
    return [position1, position2]
  
  def traduire_inverse(self, mouvement: list[tuple[int]])->str:
    '''
    traduit un mouvement de type [position1, position2] en un str de type e2-e4
    '''
    position1, position2 = mouvement
    x1, y1 = position1
    x2, y2 = position2
    return self.colonnes[x1] + str(y1+1) + '-' + self.colonnes[x2] + str(y2+1)
    
  def deplacer(self, mouvement : list[tuple, tuple], etat : EtatEchecs) -> EtatEchecs :
    """
    Renvoie un état du jeu ayant pris en compte le déplacement d'une pièce
    
    :etat: État du jeu
    :mouvement: [position1,position2]
    :return: État du jeu modifié
    """
    e1 = etat.copie_peu_profonde()
    piece = copy.copy(e1.plateau.pop(mouvement[0], None))
    if piece is None or piece.est_blanc != etat.est_blanc:
      raise PieceNotExistError
    if mouvement[1] not in piece.coups_possibles(etat, True):
      raise MovementImpossibleError
    assert isinstance(piece.position,tuple)
    piece.position = mouvement[1]
    e1.plateau[(mouvement[1])] = piece
    e1.est_blanc = not(e1.est_blanc)
    return e1
      
  def mouvements_autorises(self, etat : EtatEchecs) -> list[tuple,tuple] : 
    ''' 
    :joueur: est_blanc
    :return: [[position1, position2]] si [position1,position2] mouvement possible pour ce joueur
    '''
    if etat in self._cache_mouvements :
      print(len(self._cache_mouvements))
      return self._cache_mouvements[etat]
    mouvs = []
    liste_coups_possibles = self.get_liste_coups_possibles(etat, etat.est_blanc)
    for (x,y) in liste_coups_possibles : 
      for (a,b) in liste_coups_possibles[(x,y)] : 
        mouvs.append([(a,b),(x,y)])
    #self._cache_mouvements[etat] = mouvs
    return mouvs
  
  def verif_echec_mat_pat(self, etat : EtatEchecs, joueur_est_blanc : bool):
    '''
      verifie si un joueur d'une couleur donnee n'est pas en echec et mat ou en pat
      renvoie False, False s'il n'y a ni echec ni pat
              True, False si pat
              True, True si echec et mat
    '''
    for piece in etat.plateau.values():
      if piece.est_blanc == joueur_est_blanc and piece.coups_possibles(etat, True):
        return False, False
    roi = etat.roi_blanc if joueur_est_blanc else etat.roi_noir
    return True, roi.est_echec(etat)

  def etat_final(self, etat, historique) : 
    '''
    :historique: ["mouvement"] pour les mouvements déjà joués moins de 50 tours auparavant
    :return: si l'état final est atteint (match nul ou victoire) ou pas, bool
    '''

    raison = None
    etat_final = False
      # vérifie s'il y a échec et mat(fonctionne pas j'ai remplace par la methode verif_echec_et_mat)
      # mon code est temporaire juste pour les test

    if self.verif_echec_mat_pat(etat, etat.est_blanc) == (True, False):
      return True, 'Match nul'
    elif self.verif_echec_mat_pat(etat, etat.est_blanc) == (True, True):
      raison = 'Echec et mat blanc' if etat.est_blanc else 'Echec et mat noir'
      return True, raison

    # état final par manque de matériel
    if len(etat.plateau.keys()) <= 4 : 
      compteur_blanc = 0
      for x in etat.plateau.values() : 
        if x.est_blanc : 
          compteur_blanc += 1

      # s'il reste moins de 2 pièces au blanc, vérifie la nature des pièces
      if compteur_blanc <= 2 : 
        liste = []
        for piece in etat.plateau.values():
          liste.append(isinstance(piece, Roi) or isinstance(piece, Cavalier) or isinstance(piece, Fou))
        etat_final = False not in liste

      # s'il y a moins de quatre pièces, dont 2 sont des cavaliers de même couleur, fin de partie
      couleurs_C = []
      for piece in etat.plateau.values():
        if isinstance(piece, Cavalier) : 
          couleurs_C.append(piece.est_blanc)
      if len(couleurs_C) == 2 and couleurs_C[0] == couleurs_C[1] : 
        etat_final = True
      
    if len(historique) >= 6 :
        #règle des trois coups
      for a in historique[::2]:
        for b in historique[1::2] : 
          if (historique[-1],historique[-2]) == (a,b) :
              etat_final == True
      '''
      # règle des 50 coups
      coups = []
      for coup, c in historique :
          if coup != coup :
              coups.append(coup)
              
          elif isinstance(c,Pion) :
              coups.append(coup)
      if coups == [] :
          etat_final = True
    '''
    if etat_final == True and raison is None:
      raison = "Match nul"
    return etat_final, raison

  def get_liste_coups_possibles(self, etat : EtatEchecs, est_blanc : bool) -> dict[tuple,set[tuple]] :
    '''
    :return: associe à chaque case du plateau où un coup peut être joué les coups qui peuvent y être joués
    '''
    coups = {} 
    for piece in etat.plateau.values() :
      if piece.est_blanc == est_blanc : 
        for coup in piece.coups_possibles(etat, True): 
          coups.setdefault(coup,set()).add(piece.position)
    return coups 

  @staticmethod
  def str_en_piece(c : str, pos : tuple[int, int]) -> Piece:
    '''
    Prend en argument le nom d'une piece et sa position et renvoie la piece
    '''
    #on verifie que la position donnee existe bien
    assert 0 <= pos[0] < 8 and 0 <= pos[1] < 8

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

  def charger(self, chemin) -> EtatEchecs:
    '''
    renvoie l'etat d'une partie a partir du chemin du fichier txt ou elle est stockee

    :param chemin: str donnant le chemin du fichier
    :retur: objet EtatEchecs contenant l'etat charge
    '''
    fichier = open(chemin, 'r')
    etatTxt = fichier.read()
    etatTxt = etatTxt.split()
    couleur_debut = etatTxt.pop(-1) #la derniere ligne devra contenir la couleur de celui qui commence (B pour blanc, sinon c'est le noir)
    if len(etatTxt) != 8 :
      raise WrongFileError('Trop ou pas assez de lignes dans le fichier a charger')
    plateau = dict()
    for i, ligne in enumerate(etatTxt):
      if len(ligne) != 8 :
        raise WrongFileError('Trop ou pas assez de pieces sur une ligne dans le fichier a charger')
      for j, p in enumerate(ligne):
        if p != '.':
          x = j
          y = 7 - i
          plateau[x, y] = self.str_en_piece(p, (x, y))
    titre = chemin.split("/")
    if titre[-1][0] == "B" :
      joueur = True
    else :
      joueur = False
    etat = EtatEchecs(couleur_debut == 'B', 0, plateau) 
    etat.roi_blanc = self.recherche_roi(etat, True)
    etat.roi_noir = self.recherche_roi(etat, False)
    if etat.roi_blanc is None or etat.roi_noir is None:
      raise KingNotFoundError
    return etat
  
  def afficher(self, etat) -> None:
    '''
    affiche le plateau suivant l'etat donne 
    '''
    print(etat, '_______________________________', '\na | b | c | d | e | f | g | h |')
    return None

  def enregister(self, etat, nom) -> None:
    '''
    sauvegarde l'etat de la partie dans un fichier donne
    
    :param etat: etat de la partie a sauvegarder
    :param nom: nom qu'on veut donner au fichier de sauvegarde
    '''
    if path.isfile(nom): 
      nom += str(randint(0,1000))
    fichier = open(nom, 'w+')
    print(repr(etat))
    fichier.write(repr(etat))
    print('Le fichier a ete enregistre sous le nom ', nom)
    return None

  # recueille les choix de l'utilisateur en début de partie
  def menu(self) -> list[str, str]:
    ''' affiche le menu du jeu et récupère les choix du joueurs pour sa partie.
    :return: [choix1,choix2]
    '''
    print("Menu du jeu d'échecs : ")
    print("Si vous voulez commencer une nouvelle partie, entrez n.")
    print("Si vous voulez reprendre une ancienne partie, entrez a.")
    print("Si vous voulez plus d'informations sur l'utilisation de ce programme, entrez help.")
    choix1 = input()
    choix2 = 0
    if choix1 == "n" or choix1 == "a" : 
      choix2 = input("Voulez-vous jouer contre un autre joueur(entrer j), jouer contre une IA (entrer i) ou faire s'afffronter deux IAs (entrer ii) ?")
      print("La partie va commencer. Si vous voulez quitter sans sauvegarder, entrez quit. Si vous voulez sauvegarder votre partie, entrez save. Si vous voulez plus d'informations sur le programme, entrez help.")
    return [choix1, choix2]

  # le plus important, la méthode à lancer au démarrage du programme pour lancer et mener la partie.
  def debut_partie(self):
    ''' lance la partie et la finit'''
    
    choix1, choix2 = self.menu()
    try : 
      # nouvelle partie
      if choix1 == 'n' : 
        etat = self.charger('BNouvelle_partie.txt')
        self.choisir_partie(etat, choix2)
      # partie chargée
      elif choix1 == 'a' :
        try : 
            fichier = input("Donnez le chemin du fichier à charger. ")
            etat = self.charger(fichier)
        except :
            print("Votre chemin n'est pas valide. Si le fichier est dans le dossier du programme, donnez le nom du fichier. Sinon, donnez le chemin. Pour plus d'informations, allez dans help.")
            self.debut_partie()
        self.choisir_partie(etat, choix2)
            
      # affiche le mode d'emploi
      elif choix1 == 'help' : 
          self.afficher_aide()
          self.debut_partie()

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
  def choisir_partie(self,etat, choix) : 
    '''commence la partie selon les choix de joueur (choix2) de l'utilisateur
    :choix: choix2 du menu, str == 'j', 'i' ou 'ii'
    :return: p, historique des mouvements, list[list[tuple]]
    '''
    p = None
    if choix == 'j' : 
        self.partie('humain', 'humain', etat)
    elif choix == 'i' : 
        self.partie('humain','IA', etat)
    elif choix == 'ii' : 
        self.partie('IA','IA', etat)
    else :
        raise InputError2
    return None
      
  def afficher_aide() : 
    ''' affiche le manuel d'utilisation du jeu'''
    with open("mode_d'emploi.txt", 'r') as f: 
      for ligne in f : 
        print(ligne)

  def strategie(self, etat, joueur) : 
    '''traite le mouvement du joueur selon son type
    :joueur: "humain" ou "IA"
    :return: mouvement effectué par le joueur, str
    '''
    
    if joueur == "humain" : 
      couleur = 'blancs' if etat.est_blanc else 'noirs'
      print('Trait aux ', couleur)
      mouv = input("Quel mouvement voulez-vous jouer ? ")
      if mouv == "help" : 
        self.afficher_aide() 
      elif mouv == "quit" : 
        sys.exit()
      elif mouv == "save" :
        nom = input('Donner le nom que vous voulez donner a votre fichier')
        self.enregister(etat, nom)
        sys.exit()
      elif mouv == "abandon" : 
        if etat.est_blanc:
          self.fin_partie('abandon blanc')
        self.fin_partie('abandon noir')
      else :  
        return self.traduire(mouv)
        
    if joueur == "IA" : 
      start = time()
      coup_ia = self.joueur_alpha_beta(etat, self._profondeur)
      end = time()
      print(self.traduire_inverse(coup_ia), ' en ', end-start, ' secondes')
      return coup_ia
  
  def evaluer_coup(self, coup: tuple[list[tuple,tuple], EtatEchecs], etat: EtatEchecs) -> float:
    '''
    Évalue la qualité d'un coup en attribuant un score.

    :param coup: Le coup à évaluer.
    :type coup: Tuple[TypeMouvement, TypeEtat]

    :param etat: L'état actuel du jeu.
    :type etat: EtatEchecs

    :return: Un score représentant la qualité du coup.
    :rtype: float
    '''
    mouvement, etat_suivant = coup

    # Récupérer la pièce qui a été déplacée
    piece_deplacee = etat.plateau[mouvement[0]]

    # Calculer la valeur de la pièce déplacée
    valeur_piece = piece_deplacee.valeur

    # Score de base en fonction de la valeur de la pièce déplacée
    score = valeur_piece

    # Bonus pour les captures
    piece_prise = etat_suivant.plateau.get(mouvement[1])
    if piece_prise:
        score += piece_prise.valeur
    return score

  
  def joueur_alpha_beta(self, etat: EtatEchecs, profondeur: int):
      assert profondeur > 0
      #(profondeur+1)  x 100000 correspond a un mat en 1 coup ainsi pour savoir combien de coups il reste avant le mat suffit de diviser la valeur par 100000 et lui retirer la profondeur
      alpha = -(profondeur + 1) * 100000
      beta = (profondeur + 1) * 100000
      meilleur_coup = None
      # Obtenez la liste des coups possibles
      coups_possibles = list(self.suivants(etat))

      # Triez les coups en fonction de leur score
      coups_possibles.sort(key=lambda coup: self.evaluer_coup(coup, etat), reverse=True)

      for mouvement, etat_suivant in coups_possibles:
          valeur = self.alpha_beta(etat_suivant, profondeur - 1, alpha, beta, not etat.est_blanc)
          if etat.est_blanc and valeur == profondeur * 100000:
              return mouvement

          elif not etat.est_blanc and valeur == -profondeur * 100000:
              return mouvement

          if etat.est_blanc and valeur > alpha:
              alpha = valeur
              meilleur_coup = mouvement

          if not etat.est_blanc and valeur < beta:
              beta = valeur
              meilleur_coup = mouvement

          if beta <= alpha:
              break

      return meilleur_coup

  def jouer_coup(self, joueur1 : str, joueur2 : str, etat : EtatEchecs) -> tuple[str, EtatEchecs]:
    ''' 
    Joue le coup choisi pour ce tour par le joueur selon sa stratégie (son type).
    :joueur1: str, "humain" ou "IA"
    :joueur2: str, "humain" ou "IA"
    :return: mouvement joué (str)
    '''
    try : 
      e1 = copy.deepcopy(etat)
      if etat.est_blanc == True :
        mouv = self.strategie(e1,joueur1)
      else : 
        mouv = self.strategie(e1,joueur2)
      e1 = self.deplacer(mouv, etat)
    except MovementImpossibleError:
      print('Mouvement Impossible')
      mouv, e1 = self.jouer_coup(joueur1, joueur2, etat)
    except PieceNotExistError:
      print('Il n\' y a pas de piece vous appartenant a cet endroit')
      mouv, e1 = self.jouer_coup(joueur1, joueur2, etat)
    return mouv, e1
      

  # déroulé de la partie
  def partie(self, joueur1 : str, joueur2 : str, etat : EtatEchecs) :
    ''' 
    Déroule la partie de son commencement à l'état final
    :etat: etat du jeu
    :joueur1: str, "humain" ou "IA"
    :joueur2: str, "humain" ou "IA"
    :return: historique des mouvements, list[list[tuple]]
    '''
    historique = []
    est_fin = False
    # déroulé de la partie
    while not est_fin :
      # règle des 50
      if len(historique) > 50 :
        historique.pop(0)
      self.afficher(etat)
      mouv, etat = self.jouer_coup(joueur1, joueur2, etat)
      piece_jouee = etat.plateau[mouv[1]]
      historique.append([mouv, piece_jouee])
      etat.roi_blanc = self.recherche_roi(etat, True)
      etat.roi_noir = self.recherche_roi(etat, False)
      etat.valeur = self.eval_statique(etat)
      print(etat.valeur)
      est_fin, raison = self.etat_final(etat, historique)
  
    self.fin_partie(raison)  
    return None
  
  def eval_statique(self, etat: EtatEchecs):
      '''
      retourne une évaluation statique de l'état
      '''
      # Somme des valeurs des pièces (la valeur des pièces noires est négative)
      valeur = sum([piece.valeur for piece in etat.plateau.values()])

      centre = (3.5, 3.5)  # Position centrale de l'échiquier

      nb_tours_blanches = 0 #on initialise le nombre de tours pour encourager leur connexion
      nb_tours_noires = 0
      for position, piece in etat.plateau.items():
          # Calculer la distance euclidienne entre la position de la pièce et le centre
          distance_centre = ((position[0] - centre[0]) ** 2 + (position[1] - centre[1]) ** 2) ** 0.5

          # Attribuer un bonus en fonction de la proximité du centre
          bonus_centre = 1 / (1 + distance_centre)  # Plus la distance est courte, plus le bonus est élevé

          # Ajouter le bonus à la valeur en fonction de la couleur de la pièce
          valeur += bonus_centre if piece.est_blanc else -bonus_centre
          
          if isinstance(piece, Tour):
            if piece.est_blanc :
              nb_tours_blanches += 1
            else :
              nb_tours_noires += 1

      if nb_tours_blanches == 2:
          valeur += 0.2
      if nb_tours_noires == 2:
          valeur -= 0.2
      return valeur


  def recherche_roi(self, etat : EtatEchecs, roi_est_blanc : bool):
    '''
      Retourne le roi de la coulour souhaite
      :param etat: etat du jeu
      :param roi_est_blanc: True si le roi a chercher est blanc, False sinon
    '''
    for piece in etat.plateau.values():
      if isinstance(piece, Roi) and piece.est_blanc == roi_est_blanc:
        return piece

  # fin de partie
  def fin_partie(self,raison_etat_final) :
    ''' 
    Met fin à la partie quand l'état final est atteint ou qu'il y a un abandon.
    :raison_etat_final: self.etat_final[1], str
    '''
    
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
    elif raison_etat_final == "pat blanc":
      print("Pat au joueur blanc")
    else :
      print("Pat au joueur noir")
    sys.exit()
      
  def valeur(self, etat, joueur):
    return self.eval_statique(etat)
  
  @lru_cache(maxsize=None)
  def alpha_beta(self, etat, profondeur, alpha, beta, maximiser_joueur):
      '''
      retourne la valeur d'un etat donne allant jusqua une pronfondeur donnee ou la fin de la partie
      '''
      est_fin, raison = self.etat_final(etat, [])
      if profondeur == 0 :
          return self.valeur(etat, True)
      elif est_fin :
          if raison == 'Match nul':
            return 0
          value = (profondeur + 1) * 100000
          return -value if maximiser_joueur else value
      if maximiser_joueur:
          valeur_max = -(profondeur + 1) * 100000
          for mouv, etat_suivant in self.suivants(etat):
            valeur = self.alpha_beta(etat_suivant, profondeur - 1, alpha, beta, False)
            valeur_max = max(valeur_max, valeur)
            alpha = max(alpha, valeur)
            if beta <= alpha:
                break
          return valeur_max
        
      valeur_min = (profondeur + 1) * 100000
      
      for mouv, etat_suivant in self.suivants(etat):
        valeur = self.alpha_beta(etat_suivant, profondeur - 1, alpha, beta, False)
        valeur_min = min(valeur_min, valeur)
        beta = min(beta, valeur)
        if beta <= alpha:
            break
      return valeur_min


  def alpha_beta_cache(self, etat, profondeur, alpha, beta, maximiser_joueur, cache):
      '''
      retourne la valeur d'un etat donne allant jusqua une pronfondeur donnee ou la fin de la partie
      '''
      est_fin, raison = self.etat_final(etat, [])
      if etat in cache.keys():
        return cache[etat]
      elif profondeur == 0 :
          return self.valeur(etat, True)
      elif est_fin :
          if raison == 'Match nul':
            return 0
          value = (profondeur + 1) * 100000
          return -value if maximiser_joueur else value
      
      coups_suivants = self.suivants(etat)
      if maximiser_joueur:
          valeur_max = -(profondeur + 1) * 100000
          for mouv, etat_suivant in coups_suivants:
            valeur = self.alpha_beta_cache(etat_suivant, profondeur - 1, alpha, beta, False, cache)
            cache[etat_suivant] = valeur
            valeur_max = max(valeur_max, valeur)
            alpha = max(alpha, valeur)
            if beta <= alpha:
                break
          return valeur_max
      valeur_min = (profondeur + 1) * 100000
      for mouv, etat_suivant in self.suivants(etat):
        valeur = self.alpha_beta_cache(etat_suivant, profondeur - 1, alpha, beta, True, cache)
        cache[etat_suivant] = valeur
        valeur_min = min(valeur_min, valeur)
        beta = min(beta, valeur)
        if beta <= alpha:
            break
      return valeur_min
    
from __future__ import annotations
from EtatJeu import EtatJeu


class EtatEchecs(EtatJeu):
    def __init__(self, Joueur: bool, Valeur: int, Plateau):
        self.est_blanc = Joueur
        self.Valeur = Valeur
        self.plateau = Plateau
        self.roi_blanc = None
        self.roi_noir = None
        self.mouvements = None

    def copie_peu_profonde(self):
        new_state = EtatEchecs(self.est_blanc, self.Valeur, dict(self.plateau))
        new_state.roi_blanc = self.roi_blanc 
        new_state.roi_noir = self.roi_noir
        return new_state

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
          p = self.plateau.get((x,7-y), None)
          txt += repr(p) if p else '.'
        txt += '\n'
      txt += 'B' if self.est_blanc else 'N'
      return txt

    def __eq__(self, other : EtatEchecs) -> bool:
      return self.plateau == other.plateau and self.est_blanc == other.est_blanc
    
    def __ne__(self, other : EtatEchecs) -> bool:
       return not self.__eq__(other)
    
    def __hash__(self) -> int:
        # Utilisez une combinaison des valeurs de hachage des attributs nécessaires
        return hash((frozenset(self.plateau.items()), self.est_blanc))

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

class EtatJeu:
    def __init__(self,Joueur,Valeur,Plateau,Mouvements):
        self.joueur = Joueur # joueur qui doit jouer
        self.valeur = Valeur # valeur du jeu
        self.plateau = Plateau # dictionnaire qui représente le plateau du jeu
        self.mouvements = Mouvements # liste des mouvements autorisés à partir de la position courante
    def __str__(self) -> str:
        pass

from Piece import *
from EtatEchecs import *
from Roi import *

class Fou(Piece):
    def __init__(self, position : tuple, est_blanc) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'F' if est_blanc else 'f'
        self.valeur = 3 if est_blanc else -3

    def coups_possibles(self, etat, verif_echec = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x = self.position[0]
        y = self.position[1]
        coups = set()

        #fait un while
        for i, j in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n)))
                n+=1
            piece_en_prise = etat.plateau.get((x+(i*n),y+(j*n)), None)
            if piece_en_prise is not None and piece_en_prise.est_blanc != self.est_blanc:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n))) 
        return coups

    def __str__(self):
        if self.nom == "F" :
            return "♗"
        else : 
            return "♝"
                
from math import inf
from functools import lru_cache

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
        pass
    def est_final(self, etat):
        return not etat.mouvements
    def joueur(self, etat):
        "retourne le joueur qui doit jouer dans cet etat"
        return etat.doit_jouer
    def suivants(self, etat):  
        """retourne  la liste des etats suivants 
           suite aux mouvements autorises 
 
          :return: list[tuple[mouvement, etat_suivant]]
        """
        return [(m, self.deplacer(m, etat))
                for m in self.mouvements_autorises(etat)]
    def afficher(self, etat):
        pass

    '''
    def joueur_minimax(jeu,etat):
      #Etant donne un etat de jeu calcule le meilleur mouvement en cherchant en profondeur tous les etats jusqu'aux etats terminaux
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
      v = (-math.inf)
      for (m,s) in jeux.suivants(etat) : 
        v = max(v , min_valeur(s))
      return v
    
      
    # min valeur #
    def min_valeur(etat) :
      if jeu.est_final(etat):
        return jeu.valeur(etat,j)
      v = math.inf
      for (m,s) in jeux.suivants(etat) : 
        v = min(v , min_valeur(s))
      return v
    '''
    def __repr__(self):
        pass
    def __str__(self):
        pass

from __future__ import annotations
from abc import ABC, abstractmethod

class Piece(ABC):

    def __init__(self, position : tuple, est_blanc) -> None:
        self.position = position #prend None si la piece n'est pas sur le plateau
        self.est_blanc = est_blanc
        self.nom = None

    @abstractmethod
    def coups_possibles(self, etat) -> set:
        pass

    def coup_est_possible(self, etat, position) -> bool : 
        return position in self.coups_possibles(self,etat)
    
    def __str__(self):
        pass
    
    def __repr__(self):
        return self.nom
    
    def __eq__(self, other : Piece) -> bool:
        return self.position == other.position and self.est_blanc == other.est_blanc
    
    def __hash__(self):
        # Utilisez une combinaison de valeurs immuables qui résume l'état de l'objet
        return hash((self.est_blanc, self.position, self.nom))

from Piece import *
from EtatEchecs import *
from Roi import *

class Pion(Piece):
    def __init__(self, position, est_blanc : bool) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'P' if est_blanc else 'p'
        self.valeur = 1 if est_blanc else -1


    def coups_possibles(self, etat : EtatEchecs, verif_echec : bool = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x = self.position[0]
        y = self.position[1]
        coups = set()
        est_premier_coups = y == 1 if self.est_blanc else y == 6
        dir = 1 if self.est_blanc else -1

        if est_premier_coups and not (x, y+2*dir) in etat.plateau and not (x, y+dir) in etat.plateau:
            if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x,y+(2*dir))):
                coups.add((x,y+(2*dir)))

        if y != 7 and y != 0 :
            #test si le pion peut avancer (ou reculer)
            if not (x, y+dir) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x,y+dir)):
                    coups.add((x, y+dir))

            for i in [-1, 1] :
                if (x+i, y+dir) in etat.plateau and etat.plateau[x+i,y+dir].est_blanc != self.est_blanc:
                    if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+i,y+dir)):
                        coups.add((x+i,y+dir))
        return coups
    
    def __str__(self):
        if self.nom == "P" :
            return "♙"
        else : 
            return "♟︎"

from Piece import *
from EtatEchecs import *
import copy

class Roi(Piece):

  def __init__(self,position : tuple,est_blanc) : 
    super().__init__(position,est_blanc)
    self.nom = 'R' if est_blanc else 'r'
    self.valeur = 0

  def coups_possibles(self, etat, verif_echec : bool = False) -> set:
    '''
    methode qui test les coups possibles en testant si cela met le roi en echec
    '''
    x = self.position[0]
    y = self.position[1]
    coups = set()
    for i, j in [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]:
      piece_en_prise = etat.plateau.get((x+i,y+j), None)
      if etat.est_case(x+i,y+j) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):   
        if not verif_echec or not self.met_en_echec(etat,tuple(self.position), (x+i,y+j)):
          coups.add((x+i,y+j))

    return coups
  
  def coups_adverses(self, etat):
    '''
    methode utile qui renvoie les coups adverses possibles, utile pour la methode est echec
    :param etat: etat du jeu

    :return: set avec tous les coups adverses possibles
    '''
    coups = set()
    for position, piece in etat.plateau.items() : 
      if piece.est_blanc != self.est_blanc : 
        coups |= piece.coups_possibles(etat, False)
    return coups  

  def est_echec(self, etat : EtatEchecs):
    '''verifie si le roi est en echec'''
    return tuple(self.position) in self.coups_adverses(etat)
    
  def met_en_echec(self, etat : EtatEchecs, old_pos : tuple, new_pos : tuple):
    '''
    methode qui verifie si un coup joue par un joueur met son propre roi en echec
    :param etat: etat du jeu
    :param old_pos: ancienne position de la piece
    :param new_pos: nouvelle position de la piece

    :return: vrai si le roi est mis en echec par le coup
    '''
    if old_pos not in etat.plateau:
      raise AttributeError('Erreur dans la position de la piece')
    etat1 = etat.copie_peu_profonde()
    piece = copy.copy(etat1.plateau.pop(old_pos))
    piece.position = list(new_pos)
    etat1.plateau[new_pos] = piece
    if isinstance(piece, Roi):
      #si la piece est le roi alors est_echec doit verifier si le roi a la nouvelle position est mit en echec sans changer la position du vrai roi
      return piece.est_echec(etat1)
    return self.est_echec(etat1)
  
  def __str__(self):
    if self.nom == "R" :
      return "♔"
    else : 
      return "♚"

from Piece import *
from EtatEchecs import *
from Roi import *

class Tour(Piece):
    def __init__(self, position : tuple, est_blanc : bool) -> None:
        super().__init__(position, est_blanc)
        self.nom = 'T' if est_blanc else 't'
        self.valeur = 5 if est_blanc else -5

    def coups_possibles(self, etat : EtatJeu, verif_echec : bool = False) -> set:
        roi = etat.roi_blanc if self.est_blanc else etat.roi_noir
        x = self.position[0]
        y = self.position[1]
        coups = set()

        for i,j in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            n = 1
            while etat.est_case(x+(i*n),y+(j*n)) and not (x+(i*n),y+(j*n)) in etat.plateau:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n)))
                n+=1
            piece_en_prise = etat.plateau.get((x+(i*n),y+(j*n)), None)
            if piece_en_prise is not None and piece_en_prise.est_blanc != self.est_blanc:
                if not verif_echec or not roi.met_en_echec(etat, tuple(self.position), (x+(i*n),y+(j*n))):
                    coups.add((x+(i*n),y+(j*n))) 

        return coups

    def __str__(self):
        if self.nom == "T" :
            return "♖"
        else : 
            return "♜"