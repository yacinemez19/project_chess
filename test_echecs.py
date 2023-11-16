import pytest
from io import StringIO
from Echecs import Echecs, PieceNotExistError, MovementImpossibleError, WrongFileError, KingNotFoundError
from EtatEchecs import EtatEchecs

@pytest.fixture
def exemple_jeu():
    jeu = Echecs()
    return jeu

@pytest.fixture
def exemple_etat(exemple_jeu):
    etat = exemple_jeu.charger('/tests_echecs/test.txt')
    return etat

def test_traduire(exemple_jeu):
    mouvement_valide = "a2-b3"
    assert exemple_jeu.traduire(mouvement_valide) == [(0, 1), (1, 2)]
    mouvement_invalide = "z4-i9"
    assert exemple_jeu.traduire(mouvement_invalide) == "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"
    mouvement_vide = ""
    assert exemple_jeu.traduire(mouvement_vide) == "Votre mouvement n'est pas valide. Veuillez respecter le format : type a6-b3 pour un mouvement et type Ca6-b3 pour une capture, en respectant la taille 8x8 du plateau. Pour plus d'informations sur le format, appeler help"
    
def test_deplacer_valide(exemple_jeu, exemple_etat):
    mouvement_valide = [(0,1),(0,2)]
    nouvel_etat = exemple_jeu.deplacer(mouvement_valide, exemple_etat)
    with pytest.raises(KeyError): # S'assure qu'aucune pièce ne se situe dans la position initiale du plateau
        nouvel_etat.plateau[mouvement_valide[0]]
    piece = nouvel_etat.plateau[mouvement_valide[1]]
    assert piece.position == mouvement_valide[1]
    
def test_deplacer_invalide(exemple_jeu, exemple_etat):
    mouvement_invalide = [(0,2),(0,3)] # Invalide car aucune pièce n'est présente en (0,2)
    with pytest.raises(PieceNotExistError):
        exemple_etat = exemple_jeu.deplacer(mouvement_invalide, exemple_etat)
        
def test_deplacer_impossible(exemple_jeu, exemple_etat):
    mouvement_impossible = [(0,1),(1,1)] # Impossible car il y a déjà une pièce en 1,1 et le pion ne se déplace pas latéralement
    with pytest.raises(MovementImpossibleError):
        exemple_etat = exemple_jeu.deplacer(mouvement_impossible, exemple_etat)

def test_charger(exemple_jeu):
    '''Teste si un fichier corrompu renvoie bien une erreur WrongFileError'''
    with pytest.raises(WrongFileError):
        exemple_jeu.charger('tests_echecs/test_chargercolonne.txt')
    with pytest.raises(WrongFileError):
        exemple_jeu.charger('tests_echecs/test_chargerligne.txt')
    with pytest.raises(KingNotFoundError):
        exemple_jeu.charger('tests_echecs/test_pasderoi.txt')
        
def test_afficher(capfd,exemple_jeu,exemple_etat):
    exemple_jeu.afficher(exemple_etat)
    captured = capfd.readouterr()
    expected_output = (
        " | ♜ | ♞ | ♝ | ♛ | . | ♝ | . | ♜ |\n"
       + " +-------------------------------+\n "
       + "| ♟︎ | ♟︎ | ♟︎ | . | ♟︎ | ♟︎ | ♟︎ | ♟︎ |\n "
       + "+-------------------------------+\n "
       + "| . | . | . | ♟︎ | . | . | . | . |\n "
       + "+-------------------------------+\n "
       + "| . | . | . | . | . | . | . | . |\n "
       + "+-------------------------------+\n "
       + "| . | . | . | ♙ | ♚ | . | . | . |\n "
       + "+-------------------------------+\n "
       + "| . | . | . | . | . | ♙ | . | . |\n "
       + "+-------------------------------+\n "
       + "| ♙ | ♙ | ♙ | . | ♙ | . | ♙ | ♙ |\n "
       + "+-------------------------------+\n "
       + "| ♖ | . | ♗ | ♕ | ♔ | ♗ | ♘ | ♖ |"
       + "\n +-------------------------------+"
       + "\n a | b | c | d | e | f | g | h |\n"
    )
    assert captured[0] == expected_output

    