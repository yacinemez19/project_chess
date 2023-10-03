from EtatJeu import *
from Pieces import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *

class EtatEchecs(EtatJeu):
    def __init__(self, Joueur: bool, Valeur: int, Plateau: dict, Mouvements: list):
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

def charger(chemin):
    fichier = open(chemin, 'r')
    etatTxt = fichier.read()
    etatTxt = etatTxt.split()
    plateau = dict()
    for i, ligne in enumerate(etatTxt):
        print(i)
        plateau.append([])
        for j, p in enumerate(ligne):
            print(j)
            if p != '.':
                plateau[j, i] = strEnPiece(p, [j, i])
    return plateau

print(charger('test.txt'))


