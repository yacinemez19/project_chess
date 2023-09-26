class EtatJeu:
    def __init__(self,Joueur,Valeur,Plateau,Mouvements):
        self.joueur = Joueur # joueur qui doit jouer
        self.valeur = Valeur # valeur du jeu
        self.plateau = Plateau # dictionnaire qui représente le plateau du jeu
        self.mouvements = Mouvements # liste des mouvements autorisés à partir de la position courante
    def __str__(self) -> str:
        pass

