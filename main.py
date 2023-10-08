from Echecs import *

partie = Echecs()

etat = partie.charger('test.txt')

print(etat)

for i, j in etat.plateau.items():
    print(i,j, j.est_blanc)
    print(j.coups_possibles(etat))

c =etat.plateau[(4,7)].coups_adverses(etat)
i=0
for a in c:
    i+=1
print(c)


print(c)
a = partie.liste_coups_possibles(etat, True)
print(a)