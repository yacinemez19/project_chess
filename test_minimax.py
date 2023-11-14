from Echecs import *
import time
from math import inf
from EtatEchecs import *

partie = Echecs()
etat = partie.charger('test_eval_statique.txt')
print(etat)
print(partie.eval_statique(etat))
piece = etat.plateau.get((5,2))
print(piece)
print(piece.coups_possibles(etat))
'''
cache = {}
etat.est_blanc = True
etat = partie.deplacer([(1,1), (1,2)], etat)
start = time.time()
b = partie.alpha_beta(etat, 4, -4000, 4000, etat.est_blanc)
print(etat)
end = time.time()
print(start-end)
start = time.time()
b = partie.alpha_beta_cache(etat, 4, -4000, 4000, etat.est_blanc,cache)
print(etat)
end = time.time()
print(end-start, b)
'''
