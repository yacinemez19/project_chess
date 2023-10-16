import pytest

from Echecs import Echecs
from EtatEchecs import EtatEchecs
from Roi import Roi
from Fou import Fou
from Pion import Pion

def test_coups_possibles():
    partie = Echecs()
    etat = partie.charger('test.txt')
    
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Roi:
            roi = piece
    assert roi.position == [4,0] and roi.est_blanc is True
    assert roi.coups_possibles(etat) == {(3,1),(5,1)}
    
    fou = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Fou:
            fou = piece
    assert fou.position == [5,0]
    assert fou.coups_possibles(etat) == set()
    
    pion = None
    pion = etat.plateau[(5,2)]
    assert pion.position == [5,2]
    assert pion.coups_possibles(etat) == {(5,3),(4,3)}
    
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
    assert roi.coups_possibles_echec(etat) == set()

def test_coups_adverses():
    partie = Echecs()
    etat = partie.charger('testechec.txt')
    c = etat.plateau[(4,7)].coups_adverses(etat)
    assert c == {(1, 2), (3, 4), (4, 3), (3, 1), (7, 3), (0, 2), (2, 2), (3, 2), (1, 3), (5, 2), (6, 2), (0, 3), (4, 2), (2, 3), (7, 2), (5, 3), (6, 3)}


def test_pat():
    partie = Echecs()
    etat = partie.charger('test_pat.txt')
    roi = etat.plateau[(6,7)]
    assert roi.position == [6,7] and roi.est_blanc is False
    assert roi.est_echec(etat) is None
    assert roi.coups_possibles_echec(etat) == set()