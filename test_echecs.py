import pytest

from Echecs import Echecs
from EtatEchecs import EtatEchecs

def test_traduire():
    jeu = Echecs()
    mouvement_valide = "a2-b3"
    assert jeu.traduire(mouvement) == [(0, 1), (1, 2)]
    mouvement_invalide = "f4-i5"
    assert jeu.traduire(mouvement_invalide) == "Votre mouvement n'est pas valide. Veuillez respecter le format..."

def test_deplacer():
    