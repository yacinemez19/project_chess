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
    #Roi
    etat = partie.charger('tests_pieces/test_roi.txt')
    roi = etat.plateau[(4,4)]
    assert roi.coups_possibles(etat, True) == {(5, 5), (3, 4), (4, 3), (5, 4), (4, 5), (3, 3), (5, 3), (3, 5)}
    #Fou
    etat = partie.charger('tests_pieces/test_fou.txt')
    fou = etat.plateau[(4,4)]
    assert fou.coups_possibles(etat, True) == {(6, 2), (5, 5), (7, 1), (7, 7), (0, 0), (1, 1), (5, 3), (1, 7), (3, 3), (2, 6), (2, 2), (6, 6), (3, 5)}
    #Pion
    etat = partie.charger('tests_pieces/test_pion.txt')
    pion = etat.plateau[(4,4)]
    assert pion.coups_possibles(etat, True) == {(4, 3)}
    #Tour
    etat = partie.charger('tests_pieces/test_tour.txt')
    tour = etat.plateau[(4,4)]
    assert tour.coups_possibles(etat, True) == {(7, 4), (2, 4), (4, 0), (0, 4), (3, 4), (4, 3), (5, 4), (4, 6), (6, 4), (1, 4), (4, 2), (4, 5), (4, 1), (4, 7)}
    #Cavalier
    etat = partie.charger('tests_pieces/test_cavalier.txt')
    cavalier = etat.plateau[(4,4)]
    assert cavalier.coups_possibles(etat, True) == {(6, 5), (2, 3), (2, 5), (5, 6), (3, 6), (3, 2), (6, 3), (5, 2)}
    #Dame
    etat = partie.charger('tests_pieces/test_dame.txt')
    reine = etat.plateau[(4,4)]
    print(reine.coups_possibles(etat, True))
    assert reine.coups_possibles(etat, True) == {(4, 0), (3, 4), (4, 3), (5, 4), (4, 6), (2, 2), (7, 4), (6, 2), (7, 1), (7, 7), (4, 2), (4, 5), (3, 3), (5, 3), (2, 4), (0, 4), (6, 4), (4, 1), (4, 7), (3, 5), (5, 5), (0, 0), (1, 1), (1, 4), (1, 7), (2, 6), (6, 6)}


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