import pytest

from Echecs import Echecs
from EtatEchecs import EtatEchecs
from Roi import Roi
from Fou import Fou


def test_coups_possibles():
<<<<<<< Updated upstream
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
=======
    etat = EtatEchecs()
    roi = Roi((1,2),True,False)
    assert Roi.coups_possibles(etat) == [(2,2),(2,3),(1,3),(0,3),(0,2),(0,1),(1,1),(2,1)]

test_coups_possibles()
>>>>>>> Stashed changes
