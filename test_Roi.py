import pytest

from Roi import *
from EtatEchecs import *
from Echecs import *

def test_coups_possibles():
    etat = EtatEchecs()
    roi = Roi((1,2),True,False)
    assert Roi.coups_possibles(etat) == [(2,2),(2,3),(1,3),(0,3),(0,2),(0,1),(1,1),(2,1)]