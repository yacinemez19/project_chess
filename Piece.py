from __future__ import annotations
from abc import ABC, abstractmethod

class Piece(ABC):

    def __init__(self, position : tuple, est_blanc) -> None:
        self.position = position #prend None si la piece n'est pas sur le plateau
        self.est_blanc = est_blanc
        self.nom = None

    @abstractmethod
    def coups_possibles(self, etat) -> set:
        pass

    def coup_est_possible(self, etat, position) -> bool : 
        return position in self.coups_possibles(self,etat)
    
    def __str__(self):
        pass
    
    def __repr__(self):
        return self.nom
    
    def __eq__(self, other : Piece) -> bool:
        return self.position == other.position and self.est_blanc == other.est_blanc
    
    def __hash__(self):
        # Utilisez une combinaison de valeurs immuables qui résume l'état de l'objet
        return hash((self.est_blanc, self.position, self.nom))