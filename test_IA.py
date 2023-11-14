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

# attention pas compris comment charger le joueur voulu dans charger donc faux pour l'instant

def test_echec_et_mat():
    
    depart1 = time.time()
    etat = e.charger('Btest_echec_et_mat.txt')
    mouv = e.joueur_alphabeta(etat)
    fin1 = time.time()
    assert mouv == [(1,4),(0,4)]
    
    depart2 = time.time()
    etat2 = e.charger('Ntest_eviter_echec_et_mat.txt')
    mouv2 = e.joueur_alphabeta(etat2)
    fin2 = time.time()
    assert mouv2 == [(0,1),(1,1)]
    
    return (fin1-debut1,fin2-debut2)

def capture_pion() : 
    
    depart1 = time.time()
    etat = e.charger('Btest_capture_pion.txt')
    mouv = e.joueur_alphabeta(etat)
    fin1 = time.time()
    assert mouv = [(7,6),(7,1)]
    
    depart2 = time.time()
    etat2 = e.charger('Ntest_eviter_capture_pion_2.txt')
    mouv2 = e.joueur_alphabeta(etat2)
    fin2 = time.time()
    assert mouv2 = [(7,1),(7,2)]
    
    return (fin1-debut1,fin2-debut2)
    
def test_partie_IAs() : # pas fini
    
    etat = e.charger('BNouvelle_partie.txt')
    
    durees = []
    
    depart = time.time()
    mouv1, etat = self.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = self.recherche_roi(etat, True)
    etat.roi_noir = self.recherche_roi(etat, False)
    etat.valeur = self.eval_statique(etat)
    fin = timre.time()
    assert mouv1 = []
    
    durees.append(fin-depart)
    
    depart = time.time()
    mouv2, etat = self.jouer_coup("IA", "IA", etat)
    etat.roi_blanc = self.recherche_roi(etat, True)
    etat.roi_noir = self.recherche_roi(etat, False)
    etat.valeur = self.eval_statique(etat)
    fin = timre.time()
    assert mouv2 = []
    
    durees.append(fin-depart)
    
    return durees


    