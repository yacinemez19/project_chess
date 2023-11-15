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
import time

@pytest.fixture
def e() :
    return Echecs()

def test_echec_et_mat(e):
    
    depart1 = time.time()
    etat = e.charger('Btest_echec_et_mat_IA.txt')
    mouv = e.joueur_alpha_beta(etat, 3)
    fin1 = time.time()
    assert mouv == [(1,3),(0,3)]
    
    depart2 = time.time()
    etat2 = e.charger('Ntest_eviter_echec_IA.txt')
    mouv2 = e.joueur_alpha_beta(etat2, 3)
    fin2 = time.time()
    assert mouv2 == [(0,6),(1,6)]
    

def capture_pion(e) : 
    
    depart1 = time.time()
    etat = e.charger('Btest_capture_pion.txt')
    mouv = e.joueur_alpha_beta(etat,3)
    fin1 = time.time()
    assert mouv == [(7,1),(7,6)]
    
    depart2 = time.time()
    etat2 = e.charger('Ntest_eviter_capture_pion_2.txt')
    mouv2 = e.joueur_alpha_beta(etat2, 3)
    fin2 = time.time()
    assert mouv2 == [(7,6),(7,5)]
    

    
def test_mat_2_coups(e) : 
    pass

def test_capture_2_coups(e) :
    pass

def test_fourchette(e):
    pass



    