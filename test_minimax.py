from Echecs import *
import time
from math import inf
from EtatEchecs import *

partie = Echecs()
etat = partie.charger('Nouvelle_partie.txt')
cache = {}
etat.est_blanc = True
etat = partie.deplacer([(1,1), (1,2)], etat)
start = time.time()
b = partie.alpha_beta(etat, 3, -4000, 4000, etat.est_blanc)
print(etat)
end = time.time()
print(start-end)
start = time.time()
b = partie.alpha_beta_cache(etat, 3, -4000, 4000, etat.est_blanc,cache)
print(etat)
end = time.time()
print(end-start, b)
