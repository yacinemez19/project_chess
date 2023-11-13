class EtatJeu:
    def __init__(self,Joueur,Valeur,Plateau,Mouvements):
        self.joueur = Joueur # joueur qui doit jouer
        self.valeur = Valeur # valeur du jeu
        self.plateau = Plateau # dictionnaire qui représente le plateau du jeu
        self.mouvements = Mouvements # liste des mouvements autorisés à partir de la position courante
    def __str__(self) -> str:
        pass

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
          p = self.plateau.get((x,7-y), '.')
          txt += str(p)
        txt += '\n'
      txt += str(self.est_blanc)
      return txt

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
   
from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *
import math
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

class Echecs(Jeu) : 
  _profondeur = 2

  def traduire(self, mouvement) :
    '''
    :mouvement: "mouvement"
    :return: [ancienne position, nouvelle postion]
    '''
    colonnes =  ['a','b', 'c', 'd', 'e', 'f', 'g', 'h']
    mouv_str = [x.strip() for x in mouvement]
    
    try: 
      # vérifie qu'il s'agit d'un déplacement
      if not mouv_str[0] in colonnes : 
        raise MovementImpossibleError
      position1 = (colonnes.index(mouv_str[0]),int(mouv_str[1])-1)
      position2 = (colonnes.index(mouv_str[3]),int(mouv_str[4])-1)
      if int(mouv_str[1]) > 8 or int(mouv_str[4]) > 8 :
        raise IndexError
    except: 
      return "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"   
    
    return [position1, position2]
  
  def deplacer(self, mouv : list[tuple, tuple], etat : EtatEchecs) :
    """
    :etat: etat du jeu
    :mouv: [position1,position2]
    :return: état modifié
    """
    e1 = etat.copie_peu_profonde()
     # if mouv not in self.mouvements_autorises(e1, e1.est_blanc):
     #   raise MovementError
    piece = copy.copy(e1.plateau.pop(mouv[0], None))
    if piece is None or piece.est_blanc != etat.est_blanc:
      raise PieceNotExistError
    if mouv[1] not in piece.coups_possibles(etat, True):
      raise MovementImpossibleError
    piece.position = mouv[1]
    e1.plateau[(mouv[1])] = piece
    e1.est_blanc = not(e1.est_blanc)
    return e1
      
  def mouvements_autorises(self, etat) : 
    ''' 
    :joueur: est_blanc
    :return: [[position1, position2]] si [position1,position2] mouvement possible pour ce joueur
    '''
    mouvs = []
    liste_coups_possibles = self.get_liste_coups_possibles(etat, etat.est_blanc)
    for (x,y) in liste_coups_possibles : 
      for (a,b) in liste_coups_possibles[(x,y)] : 
        mouvs.append([(a,b),(x,y)])
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
    roi = self.roi_blanc if joueur_est_blanc else etat.roi_noir
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
      for x in etat.plateau.keys() : 
        if x.est_blanc : 
          compteur_blanc += 1

      # s'il reste moins de 2 pièces au blanc, vérifie la nature des pièces
      if compteur_blanc <= 2 : 
        liste = []
        for piece in etat.plateau.values():
          liste = isinstance(piece, Roi) or isinstance(piece, Cavalier) or isinstance(piece, Fou)
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
          coups.setdefault(coup,set()).add(tuple(piece.position))
    return coups 

  @staticmethod
  def str_en_piece(c : str, pos : [int, int]) -> Piece:
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
    plateau = dict()
    for i, ligne in enumerate(etatTxt):
      for j, p in enumerate(ligne):
        if p != '.':
          x = j
          y = 7 - i
          plateau[x, y] = self.str_en_piece(p, [x, y])
    etat = EtatEchecs(True, 0, plateau) #True car quand on charge la partie on sait pas si blanc ou noir commence
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
    fichier = open(nom, 'w')
    fichier.write()
    
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
        etat = self.charger('Nouvelle_partie.txt')
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
      elif mouv == "abandon" : 
        if etat.est_blanc:
          self.fin_partie('abandon blanc')
        else :
          self.fin_partie('abandon noir')
      else :  
        return self.traduire(mouv)
        
    if joueur == "IA" : 
      return self.joueur_alpha_beta(etat, self._profondeur)
  
  def joueur_alpha_beta(self, etat : EtatEchecs, profondeur : int):
    '''
    retourne le meilleur coup selon minimax a une profondeur donnee
    '''
    assert profondeur > 0
    tab_suivants = self.suivants(etat)
    valeur_suivants = []
    for mouv, etat_suivant in tab_suivants :
      valeur_suivants.append(self.alpha_beta(etat_suivant, profondeur, -inf, inf, not etat.est_blanc))
      #on arrete si on trouve un echec et mat en un coup
      if (valeur_suivants[-1] == profondeur * 1000 and etat.est_blanc) or (valeur_suivants[-1] == -profondeur * 1000 and not etat.est_blanc):
        break
    meilleure_valeur = max(valeur_suivants) if etat.est_blanc else min(valeur_suivants)
    return tab_suivants[valeur_suivants.index(meilleure_valeur)][0]

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
  
  def eval_statique(self, etat : EtatEchecs):
    return sum([piece.valeur for piece in etat.plateau.values()])

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
    elif raison_etat_final == "pat noir":
      print("Pat au joueur noir")
    else: 
      print('prblm')
    sys.exit()
      
  def valeur(self, etat, joueur):
    return self.eval_statique(etat)
  
  @lru_cache(maxsize=None)
  def alpha_beta(self, etat, profondeur, alpha, beta, maximiser_joueur):
      '''
      retourne la valeur d'un etat donne allant jusqua une pronfondeur donnee ou la fin de la partie
      '''
      if profondeur == 0 :
          return self.valeur(etat, True)
      elif self.etat_final(etat, []) :
          value = (profondeur + 1) * 1000
          return -value if maximiser_joueur else value
      if maximiser_joueur:
          valeur_max = -inf
          for mouv, new_etat in self.suivants(etat):
            valeur = self.alpha_beta(new_etat, profondeur - 1, alpha, beta, False)
            valeur_max = max(valeur_max, valeur)
            alpha = max(alpha, valeur)
            if beta <= alpha:
                break
          return valeur_max
      else :
          valeur_min = inf
          for mouv, new_etat in self.suivants(etat):
            valeur = self.alpha_beta(new_etat, profondeur - 1, alpha, beta, False)
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
      if etat in cache:
        print(cache, etat)
        return cache[etat]
      elif profondeur == 0 :
          return self.valeur(etat, True)
      elif est_fin :
          if raison == 'Match nul':
            return 0
          print(etat, profondeur)
          value = (profondeur + 1) * 1000
          return -value if maximiser_joueur else value
        
      if maximiser_joueur:
          valeur_max = -inf
          for mouv, new_etat in self.suivants(etat):
            valeur = self.alpha_beta_cache(new_etat, profondeur - 1, alpha, beta, False, cache)
            cache[new_etat] = valeur
            valeur_max = max(valeur_max, valeur)
            alpha = max(alpha, valeur)
            if beta <= alpha:
                break
          return valeur_max
      else :
          valeur_min = inf
          for mouv, new_etat in self.suivants(etat):
            valeur = self.alpha_beta_cache(new_etat, profondeur - 1, alpha, beta, True, cache)
            cache[new_etat] = valeur
            valeur_min = min(valeur_min, valeur)
            beta = min(beta, valeur)
            if beta <= alpha:
                break
          return valeur_min

  
  
  def construire_dict_mouvs(self,position, prof_max,etat):
    """renvoie dict_mouvs tel que chaque position pouvant être jouée jusqu'à la profondeur 3 soit associé à chaque posiiton pouvant être jouée à partir de cette position

    Args:
        position (tuple(int)): position à partir de laquelle on commence à remplir dict_mouvs
          prof_max (int): profondeur à laquelle on s'arrête de remplir dict_mouvs
          etat (EtatEchecs): etat après avoir joué position

    Returns:
        dict[tuple]: dictionnaire associant chaque position pouvant être jouée jusqu'à la profondeur 3 à chaque posiiton pouvant être jouée à partir de cette position
    """
    dict_mouvs = {}
    
    def nouvelle_prof(position, prof,etat, prof_max):
      """remplit dict_mouvs de telle sorte que chaque position pouvant être jouée jusqu'à la profondeur 3 soit associé à chaque posiiton pouvant être jouée à partir de cette position

      Args:
          position (tuple(int)): position à partir de laquelle on commence à remplir dict_mouvs
          prof (int): profondeur à laquelle on est depuis position
          prof_max (int): profondeur à laquelle on s'arrête de remplir dict_mouvs
          etat (EtatEchecs): etat après avoir joué position

      Returns: None
      """
      if prof > prof_max:
          return None
      mouvs = (etat.plateau[position]).coups_possibles(etat)
      elmts_dict = ((m,self.deplacer(m,etat)) for m in mouvs)
      dict_mouvs[position] = elmts_dict
      for position_suivante in mouvs:
          nouvelle_prof(position_suivante, prof+1, self.deplacer([position,position_suivante],etat),prof_max)

    nouvelle_prof(position, 0,etat, prof_max)
    return dict_mouvs
  '''
  def graphe_jeu(self,etat, position) :
    """crée un graphe des possibilités de jeu après avoie joué à position en dernier

    Args:
        etat (EtatEchecs): état après avoir joué à position
        position (tuple(int)): coordonées d'arrivée de la pièce déplacée en dernier

    Returns:
        Graphe: graphe des possibilités de jeu après avoie joué à position en dernier
    """
    mouvs = self.construire_dict_mouvs(position, 3, etat)
    mouvements_graphe = set()
    for position1 in mouvs.keys():
      for position2 in mouvs[position1] : 
        mouvements_graphe.add((position1, position2))
    return Graphe({x for x in mouvs.keys()},mouvements_graphe, position)
    
  def alphabeta_valeur(self,noeud, profondeur, alpha, beta, joueur_max) :
    """retourne la valeur d'un noeud donné selon si le joueur après ce noeud est le joueur max ou min

    Args:
        noeud (Graphe): noeud dont on veut calculer la valeur 
        profondeur (int): profondeur à laquelle on s'arrête et donne la valeur du plateau
        alpha (int): valeur max des autres noeuds de même profondeur que noeud
        beta (int): valeur min des autres noeuds de même profondeur que noeud
        joueur_max (boolean): vrai si le joueur jouant après ce noeud est le joueur maximisant ses noeuds

    Returns:
        int: valeur du noeud donné
    """
    if profondeur == 0 or noeud.est_feuille:
      valeur0 = self.valeur(noeud.noeud_initial[1],joueur_max)-self.valeur(noeud.noeud_initial[1],not joueur_max)
      return valeur0
        
    elif joueur_max : 
      valeur_noeud = (-math.inf)
      for fils in noeud.adj:
        graphe_fils =  self.graphe_jeu(fils[1],fils[0])
        valeur_fils = self.alphabeta_valeur(graphe_fils, profondeur - 1, alpha, beta, False)
        valeur_noeud = max(valeur_noeud, valeur_fils)
        alpha = max(alpha, valeur_noeud)

        # si la valeur de ce noeud est superieure au minimum des autres noeuds de même profondeur, on s'arrête car l'ennemi n'ira pas sur ce noeud
        if beta <= alpha:
          break
      return valeur_noeud
        
    else:
      valeur_noeud = math.inf
      for fils in noeud.adj:
        graphe_fils =  self.graphe_jeu(fils[1],fils[0])
        valeur_fils = self.alphabeta_valeur(graphe_fils, profondeur - 1, alpha, beta, True)
        valeur_noeud = min(valeur_noeud, valeur_fils)

        # si la valeur de ce noeud est inferieure au maximum des autres noeuds de même profondeur, on s'arrête car l'ennemi n'ira pas sur ce noeud
        beta = min(beta, valeur_noeud)
        if beta <= alpha:
          break
      return valeur_noeud

  def joueur_alphabeta(self,etat):
    """Etant donne un etat de jeu calcule le meilleur mouvement en cherchant en profondeur tous les etats jusqu'à la profondeur 3

    Args:
        etat (EtatEchecs): état du jeu au moment où le joueur alphabeta doit jouer

    Returns:
        [position1,position2]: coup joué par le joueur alphabeta
    """
    j = etat.est_blanc
    alpha = (-math.inf)
    beta = math.inf
    valeurs = []
    # decision alphabeta #
    for s in self.suivants(etat,etat.est_blanc):
      gnoeud = self.graphe_jeu(s[1],s[0][1])
      valeurs.append(self.alphabeta_valeur(gnoeud, 3, alpha, beta, False))
      beta = min(beta, valeurs[-1])
    M = max(valeurs)
    mouvement , e = self.suivants(etat,etat.est_blanc)[valeurs.index(M)]
    return mouvement

e = Echecs()
etat = e.charger('Nouvelle_partie.txt')
mouv = e.joueur_alphabeta(etat)
'''

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
        return not self.mouvements_autorises(etat)
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
        return self.nom
    
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

        if est_premier_coups and not (x, y+2*dir) in etat.plateau:
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
          piece_en_prise = etat.plateau.get((x+a,y+b), None)
          if etat.est_case(x+b,y+a) and (piece_en_prise is None or piece_en_prise.est_blanc != self.est_blanc):
            if not verif_echec or not roi.met_en_echec(etat,tuple(self.position), (x+a,y+b)):
              coups.add((x+b,y+a))
    return coups

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

