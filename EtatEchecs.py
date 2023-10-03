from EtatJeu import *
from Pion import *

class Etatchess(EtatJeu):
    def __init__(self, Joueur, Valeur, Plateau, Mouvements):
        super().__init__(Joueur, Valeur, Plateau, Mouvements)


    
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
    
def strEnPiece(c : str, pos : [int, int]) -> Piece:
    '''
    Prend en argument le nom d'une piece et sa position et renvoie la piece
    '''
    est_blanc = c.isupper() #les pieces blanches sont ecrites en majuscule
    c = c.lower()

    if c == 'p':
        return Pion(pos, est_blanc)
    if c == 't':
        pass
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
