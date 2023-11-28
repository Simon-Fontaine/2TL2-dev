"""
Ce module contient la classe Food
"""

from src.classes.settings import Settings


class Food:
    """
    Classe représentant la nourritures
    """

    def __init__(self, settings: Settings):
        self.__quantity = settings.initial_food_quantity

    @property
    def quantity(self):
        """
        Quantité de nourriture
        """
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        """
        Modifie la quantité de nourriture
        """
        self.__quantity = value

    def remove(self, amount: (int, float) = 1):
        """
        Retire de la nourriture
        """
        self.__quantity = max(self.__quantity - amount, 0)

    def add(self, amount: (int, float) = 1):
        """
        Ajoute de la nourriture
        """
        self.__quantity += amount

    def to_dict(self):
        """
        Convertit la nourriture en dictionnaire
        """
        return {"quantity": self.quantity}
