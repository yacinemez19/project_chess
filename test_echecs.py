import pytest

from Echecs import Echecs
from EtatEchecs import EtatEchecs
from Echecs import MovementImpossibleError

def test_traduire():
    jeu = Echecs()
    mouvement_valide = "a2-b3"
    assert jeu.traduire(mouvement_valide) == [(0, 1), (1, 2)]
    mouvement_invalide = "z4-i9"
    assert jeu.traduire(mouvement_invalide) == "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"
    
