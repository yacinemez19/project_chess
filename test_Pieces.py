import pytest

from Echecs import Echecs
from EtatEchecs import EtatEchecs
from Roi import Roi
from Fou import Fou


def test_coups_possibles():
    partie = Echecs()
    etat = partie.charger('test.txt')
    roi = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Roi:
            roi = piece
    assert roi.coups_possibles(etat) == {(3,1)}
    
    fou = None
    for piece in etat.plateau.values():
        if piece.est_blanc and type(piece) == Fou:
            fou = piece
    assert fou.coups_possibles(etat) == {}
