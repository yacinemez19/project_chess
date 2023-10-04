from Echecs import *

Partie = Echecs()

etat = Partie.charger('test.txt')

print(etat)

for i, j in etat.plateau.items():
    print(i,j, j.est_blanc)
    print(j.coups_possibles(etat))

