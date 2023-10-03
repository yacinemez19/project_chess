from EtatJeu import *
from Pieces import *

class Etatchess(EtatJeu):
    def __init__(self, Joueur, Valeur, Plateau, Mouvements):
        self.est_blanc = Joueur
        self.Valeur = Valeur
        self.plateau = Plateau
        Mouvements = self.mouvements = [(x,y) for x in range(8) for y in range (8)]

    
    def __str__(self) -> str:
        txt = ''
        i = 8
        for lignes in self.plateau:
            txt += str(i)
            i-=1
            for piece in lignes:
                txtPiece = '.' if piece is None else piece.nom
            txt += '\n'
        txt += '  abcdefgh'
        return txt

def liste_coups_possibles(self) : 
    pass

def strEnPiece(c : str, pos : [int, int]) -> Piece:
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
        pass
    if c == 'f':
        pass
    if c == 'd':
        pass
    if c == 'r':
        pass

def charger(chemin):
    etatTxt = open(chemin, 'r')
    etatTxt = etatTxt.split()
    plateau = []
    for i, ligne in enumerate(etatTxt):
        plateau.append([])
        for j, p in enumerate(ligne):
            plateau[i].append(strEnPiece(p, [j, i]))
