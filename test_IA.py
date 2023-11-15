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
    
    etat = e.charger('Btest_echec_et_mat_IA.txt')
    mouv = e.joueur_alpha_beta(etat, 3)
    assert mouv == [(1,3),(0,3)]
    
    etat2 = e.charger('Ntest_eviter_echec_IA.txt')
    mouv2 = e.joueur_alpha_beta(etat2, 3)
    assert mouv2 == [(0,6),(1,6)]
    

def capture_pion(e) : 
    
    etat = e.charger('Btest_capture_pion.txt')
    mouv = e.joueur_alpha_beta(etat,3)
    assert mouv == [(7,1),(7,6)]
    
    etat2 = e.charger('Ntest_eviter_capture_pion_2.txt')
    mouv2 = e.joueur_alpha_beta(etat2, 3)
    assert mouv2 == [(7,6),(7,5)]
    

    
def test_mat_2_coups(e) : 
    
    etat = e.charger('test_mat_en_2_coups.txt')
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(1,2),(0,0)]
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(1,1),(0,0)]
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(1,3),(2,2)]


def test_fourchette(e):
    
    etat = e.charger('test_fourchette.txt')
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(5,4),(4,2)]
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(4,2),(5,0)]



    