from abc import ABC, abstractmethod

class Piece(ABC):

    def __init__(self, position, est_blanc) -> None:
        self.position = position #prend None si la piece n'est pas sur le plateau
        self.est_blanc = est_blanc

    @abstractmethod
    def recuperer_nom(self):
        pass

    @abstractmethod
    def coups_possibles(self) -> list:
        pass

    def coup_est_possible(self, etat , position) -> bool : 
        return position in self.coups_possibles(self,etat)