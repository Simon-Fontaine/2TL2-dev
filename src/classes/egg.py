"""
Ce module contient la classe Egg
"""

import random

from src.classes.food import Food
from src.classes.settings import Settings
from src.classes.enums import State

from src.classes.ant import Ant
from src.classes.queen import Queen


class Egg:
    """
    Classe représentant un oeuf
    """

    def __init__(self, settings: Settings, food: Food, is_queen_egg=False):
        self.__age = 0
        self.__max_age = (
            random.randint(
                settings.queen_avg_egg_age - settings.queen_avg_egg_age_variation,
                settings.queen_avg_egg_age + settings.queen_avg_egg_age_variation,
            )
            if is_queen_egg
            else random.randint(
                settings.egg_avg_age - settings.egg_avg_age_variation,
                settings.egg_avg_age + settings.egg_avg_age_variation,
            )
        )
        self.__state = State.ALIVE
        self.__is_queen_egg = is_queen_egg

        self.__settings = settings
        self.__food = food

    def __check_positive(self, value: float, error_message: str):
        """
        Vérifie que la valeur est positive.
        """
        if value < 0:
            raise ValueError(error_message)

    def __check_type(self, value: float, value_type: type, error_message: str):
        """
        Vérifie que la valeur est du bon type.
        """
        if not isinstance(value, value_type):
            raise TypeError(error_message)

    @property
    def age(self) -> int:
        """
        Age de l'oeuf
        """
        return self.__age

    @age.setter
    def age(self, value: int):
        """
        Modifie l'age de l'oeuf
        """
        self.__check_type(value, int, "L'age doit être un entier")
        self.__check_positive(value, "L'age ne peut pas être négatif")
        self.__age = value

    @property
    def max_age(self) -> int:
        """
        Age maximum de l'oeuf
        """
        return self.__max_age

    @max_age.setter
    def max_age(self, value: int):
        """
        Modifie l'age maximum de l'oeuf
        """
        self.__check_type(value, int, "L'age maximum doit être un entier")
        self.__check_positive(value, "L'age maximum ne peut pas être négatif")
        self.__max_age = value

    @property
    def state(self) -> State:
        """
        Etat de l'oeuf
        """
        return self.__state

    @state.setter
    def state(self, value: State):
        """
        Modifie l'etat de l'oeuf
        """
        self.__check_type(value, State, "L'etat doit être une valeur de l'enum State")
        self.__state = value

    @property
    def is_queen_egg(self) -> bool:
        """
        Si l'oeuf est une reine ou non
        """
        return self.__is_queen_egg

    @is_queen_egg.setter
    def is_queen_egg(self, value: bool):
        """
        Modifie si l'oeuf est une reine ou non
        """
        self.__check_type(value, bool, "L'oeuf doit être une reine ou non")
        self.__is_queen_egg = value

    @property
    def is_alive(self) -> bool:
        """
        Si l'oeuf est vivant ou non
        """
        return self.__state == State.ALIVE

    def evolve(self) -> Ant or None:
        """
        Fait évoluer l'oeuf
        """
        if self.is_alive and self.__food.quantity >= self.__settings.egg_hunger:
            self.__age += 1
            self.__food.remove(
                self.__settings.queen_egg_hunger
                if self.__is_queen_egg
                else self.__settings.egg_hunger
            )
            if self.__age > self.__max_age:
                self.__state = State.DEAD
                if self.__is_queen_egg:
                    if random.random() < self.__settings.queen_egg_evolve_chance:
                        return Queen(self.__settings, self.__food)
                else:
                    if random.random() < self.__settings.egg_evolve_chance:
                        return Ant(self.__settings, self.__food)
        else:
            self.__state = State.DEAD
        return None

    def to_dict(self):
        """
        Convertit l'oeuf en dictionnaire
        """
        return {
            "age": self.age,
            "max_age": self.max_age,
            "state": self.state.value,
            "is_queen_egg": self.is_queen_egg,
        }
