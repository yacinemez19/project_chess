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
    e1 = Echecs()
    etat = e1.charger('Btest_echec_et_mat_IA.txt')
    mouv = e1.joueur_alpha_beta(etat, 3)
    print(etat)
    assert mouv == [(1,3),(0,3)]
    
    etat2 = e1.charger('Ntest_eviter_echec_IA.txt')
    mouv2 = e1.joueur_alpha_beta(etat2, 3)
    assert mouv2 == [(0,6),(1,6)]
    
    etat = e1.charger('Btest_capture_pion.txt')
    mouv = e1.joueur_alpha_beta(etat,3)
    assert mouv == [(7,1),(7,6)]
    
    etat2 = e1.charger('Ntest_eviter_capture_pion_2.txt')
    mouv2 = e1.joueur_alpha_beta(etat2, 3)
    assert mouv2 == [(7,6),(7,5)]

    
def test_mat_2_coups(e) : 
    e1 = Echecs()
    etat = e1.charger('test_mat_en_2_coups.txt')
    
<<<<<<< Updated upstream
    etat = e.charger('test_mat_en_2_coups.txt')
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(1,5),(2,5)]
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(3,6),(3,7)]
    
    mouv, etat = e.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e.recherche_roi(etat, True)
    etat.roi_noir = e.recherche_roi(etat, False)
    etat.valeur = e.eval_statique(etat)
    assert mouv == [(5,5),(3,5)]
=======
    mouv, etat = e1.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e1.recherche_roi(etat, True)
    etat.roi_noir = e1.recherche_roi(etat, False)
    etat.valeur = e1.eval_statique(etat)
    assert mouv == [(4,3),(7,0)]
    
    mouv, etat = e1.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e1.recherche_roi(etat, True)
    etat.roi_noir = e1.recherche_roi(etat, False)
    etat.valeur = e1.eval_statique(etat)
    #assert mouv == [(0,6),(0,5)]
    
    mouv, etat = e1.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = e1.recherche_roi(etat, True)
    etat.roi_noir = e1.recherche_roi(etat, False)
    etat.valeur = e1.eval_statique(etat)
    assert mouv == [(0,0),(0,5)]
>>>>>>> Stashed changes

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
    assert mouv == [(4,2),(3,0)]



    