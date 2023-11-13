from Echecs import *
import time
from math import inf
partie = Echecs()
etat = partie.charger('test_coup_echec.txt')
etat.est_blanc = False
start = time.time()
b = partie.alpha_beta_cache(etat, 4, -inf, inf, True, {})
print(etat)
end = time.time()
print(end-start, b)
