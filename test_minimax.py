from Echecs import *
import time
from math import inf
partie = Echecs()
etat = partie.charger('test_minimax_check_mate.txt')
etat.est_blanc = True
start = time.time()
b = partie.joueur_alpha_beta(etat, 5)
print(etat)
end = time.time()
print(end-start, b)
