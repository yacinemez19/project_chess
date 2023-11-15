import pytest

from Echecs import Echecs
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *

def test_coups_possibles():
    partie = Echecs()
    etat = partie.charger('test.txt')
    #Roi
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Roi:
            roi = piece
    assert roi.position == (4,0) and roi.est_blanc is True
    assert roi.coups_possibles(etat, True) == {(3,1),(5,1)}
    #Fou
    fou = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Fou:
            fou = piece
    assert fou.position == (5,0)
    assert fou.coups_possibles(etat, True) == set()
    #Pion
    pion = etat.plateau[(5,2)]
    assert pion.position == (5,2)
    assert pion.coups_possibles(etat, True) == {(5,3),(4,3)}
    #Tour
    for piece in etat.plateau.values():
        if not piece.est_blanc and type(piece) == Tour:
            tour = piece
    assert tour.position == (7, 7)
    assert tour.coups_possibles(etat, True) == {(6,7)}
    #Cavalier
    cavalier = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Cavalier:
            cavalier = piece
    assert cavalier.position == (5, 7)
    assert cavalier.coups_possibles(etat, True) == {(4, 5), (6, 5), (7, 6), (7, 8)}
    #Dame
    dame = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Dame:
            dame = piece
    assert dame.position == (4, 7)
    assert dame.coups_possibles(etat, True) == {(3, 6), (5, 6), (3, 7), (5, 7), (3, 8), (4, 6), (5, 8), (4, 8)}

def test_est_echec():
    partie = Echecs()
    etat = partie.charger('testechec.txt')
    roi = None
    for piece in etat.plateau.values():
        if piece.est_blanc and isinstance(piece,Roi):
            roi = piece
    assert roi.position == [3,1] and roi.est_blanc is True
    assert roi.est_echec(etat) is True

def test_coup_echec():
    partie = Echecs()
    etat = partie.charger('test_coup_echec.txt')
    roi = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Roi:
            roi = piece
    assert roi.position == [4,0] and roi.est_blanc is True
    assert (3, 1) in etat.plateau[(4,2)].coups_possibles(etat) 
    assert roi.met_en_echec(etat, tuple(roi.position), (3,1))
    assert roi.coups_possibles(etat, True) == set()

def test_coups_adverses():
    partie = Echecs()
    etat = partie.charger('testechec.txt')
    c = etat.plateau[(4,7)].coups_adverses(etat)
    assert c == {(1, 2), (4,0), (2,0), (3, 4), (4, 3), (7, 3), (0, 2), (2, 2), (3, 2), (1, 3), (5, 2), (6, 2), (0, 3), (4, 2), (2, 3), (7, 2), (6, 3)}


def test_pat():
    partie = Echecs()
    etat = partie.charger('test_pat.txt')
    etat.est_blanc = False
    roi = etat.plateau[(6,7)]
    assert roi.position == [6,7] and not roi.est_blanc
    assert not roi.est_echec(etat) 
    assert roi.coups_possibles(etat, True) == set()
    assert partie.etat_final(etat, []) == (True, 'Match nul')

def test_cloue():
    partie = Echecs()
    etat = partie.charger('test_cloue.txt')
    cavalier = etat.plateau[(4,6)]
    roi = etat.plateau[(4,7)]
    assert cavalier.coups_possibles(etat,True) == set()