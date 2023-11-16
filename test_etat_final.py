import pytest
from Jeu import *
from EtatEchecs import *
from Pion import *
from Tour import *
from Fou import *
from Dame import *
from Roi import *
from Cavalier import *
from Echecs import *
import math
import copy
import sys

@pytest.fixture
def e() :
    return Echecs()

def test_insuffisances_materielles(e) :
    etat = e.charger("tests_etat_final\R+CvsR+C.txt")
    assert(e.etat_final(etat,[])[0])==True
           
    etat = e.charger("tests_etat_final\R+FvsR+F.txt")
    assert(e.etat_final(etat,[])[0])==True
           
    etat = e.charger("tests_etat_final\RvsR.txt")
    assert(e.etat_final(etat,[])[0])==True
           
    etat = e.charger("tests_etat_final\RvsR+C.txt")
    assert(e.etat_final(etat,[])[0])==True
           
    etat = e.charger("tests_etat_final\RvsR+F.txt")
    assert(e.etat_final(etat,[])[0])==True
           
def test_3_repetitions(e) :
    etat = e.charger("tests_etat_final\test_3_repetitions.txt")
    historique = []
    for i in range(3) : 
        mouv = [(1,5),(0,6)]
        e.deplacer(etat, mouv)
        piece_jouee = etat.plateau[mouv[1]]
        historique.append(mouv, piece_jouee)
        
        mouv = [(1,7),(0,7)]
        e.deplacer(etat, mouv)
        piece_jouee = etat.plateau[mouv[1]]
        historique.append(mouv, piece_jouee)
        
        mouv = [(0,6),(1,5)]
        e.deplacer(etat, mouv)
        piece_jouee = etat.plateau[mouv[1]]
        historique.append(mouv, piece_jouee)
        
    assert e.etat_final(etat, historique)[0] ==  True