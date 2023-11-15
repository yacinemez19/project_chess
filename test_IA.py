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
    
    return (fin1-depart1,fin2-depart2)

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
    
    return (fin1-depart1,fin2-depart2)
    
def test__debut_partie_IAs(e) : 
    
    etat = e.charger('BNouvelle_partie.txt')
    durees = []
    
    for i in range(3) :
        depart = time.time()
        
        mouv2 = e.joueur_alpha_beta(etat, 3)
        
        mouv, etat = e.jouer_coup("IA", "IA", etat)
        etat.roi_blanc = e.recherche_roi(etat, True)
        etat.roi_noir = e.recherche_roi(etat, False)
        etat.Valeur = e.eval_statique(etat)
        
        fin = time.time()
        
        assert mouv == mouv2
    
        durees.append(fin-depart)
    
    return durees


    