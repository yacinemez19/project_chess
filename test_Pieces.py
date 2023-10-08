import pytest

import Roi 
import EtatEchecs 
import Echecs 

def test_coups_possibles():
    etat = EtatEchecs()
    roi = Roi((1,2),True,False)
    assert Roi.coups_possibles(etat) == [(2,2),(2,3),(1,3),(0,3),(0,2),(0,1),(1,1),(2,1)]