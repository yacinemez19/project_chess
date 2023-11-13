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

e = Echecs()

def test_echec_et_mat():
    
    depart1 = time.time()
    etat = e.charger('test_echec_et_mat.txt')
    mouv = e.joueur_alphabeta(etat)
    fin1 = time.time()
    assert mouv == [(1,4),(0,4)]
    
    depart2 = time.time()
    etat2 = e.charger('test_eviter_echec_et_mat.txt')
    mouv2 = e.joueur_alphabeta(etat2)
    fin2 = time.time()
    assert mouv2 == [(0,1),(1,1)]
    
    return (fin1-debut1,fin2-debut2)

def capture_pion() : 
    
    depart1 = time.time()
    etat = e.charger('test_capture_pion.txt')
    mouv = e.joueur_alphabeta(etat)
    fin1 = time.time()
    assert mouv = [(7,6),(7,1)]
    
    depart2 = time.time()
    etat2 = e.charger('test_eviter_capture_pion_2.txt')
    mouv2 = e.joueur_alphabeta(etat2)
    fin2 = time.time()
    assert mouv2 = [(7,1),(7,2)]
    
    return (fin1-debut1,fin2-debut2)
    
def capture_pion_2_etapes() : # pas fini
    
    depart1 = time.time()
    etat = e.charger('test_capture_pion_2.txt')
    mouv = e.joueur_alphabeta(etat)
    fin1 = time.time()
    assert mouv = [(7,6),(7,1)]
    
    depart2 = time.time()
    etat2 = e.charger('test_eviter_capture_pion_2.txt')
    mouv2 = e.joueur_alphabeta(etat2)
    fin2 = time.time()
    assert mouv2 = [(7,1),(7,2)]
    
    return (fin1-debut1,fin2-debut2)


    