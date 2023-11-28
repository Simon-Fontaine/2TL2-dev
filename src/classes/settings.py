"""
Ce module contient la classe Settings.
"""

YEAR = 365
MONTH = YEAR // 12
WEEK = MONTH // 4
SAVE_DIRECTORY = "saves"


class Settings:
    """
    Classe représentant les paramètres de la simulation.
    """

    def __init__(
        self,
        simulation_speed: float = 1.0,
        initial_food_quantity: float = 30000,
        initial_ant_quantity: int = 100,
        ant_avg_age: int = 90,
        ant_avg_age_variation: int = 20,
        ant_worker_chance: float = 0.95,
        min_food_multiplier: float = 0.5,
        max_food_multiplier: float = 1.5,
        ant_hunger: float = 0.3,
        ant_random_death_chance: float = 0.01,
        queen_avg_age: int = 5 * YEAR,
        queen_avg_age_variation: int = 1 * YEAR,
        queen_hunger: float = 10,
        queen_laying_rate: int = 5,
        queen_avg_eggs: int = 500,
        queen_avg_egg_variation: int = 150,
        egg_avg_age: int = 2 * WEEK,
        egg_avg_age_variation: int = 1 * WEEK,
        egg_hunger: float = 0.1,
        egg_evolve_chance: float = 0.9,
        queen_avg_egg_age: int = 2 * MONTH,
        queen_avg_egg_age_variation: int = 2 * WEEK,
        queen_egg_hunger: float = 1,
        queen_egg_evolve_chance: float = 0.5,
    ):
        self.__simulation_speed = simulation_speed
        self.__initial_food_quantity = initial_food_quantity
        self.__initial_ant_quantity = initial_ant_quantity
        self.__ant_avg_age = ant_avg_age
        self.__ant_avg_age_variation = ant_avg_age_variation
        self.__ant_worker_chance = ant_worker_chance
        self.__min_food_multiplier = min_food_multiplier
        self.__max_food_multiplier = max_food_multiplier
        self.__ant_hunger = ant_hunger
        self.__ant_random_death_chance = ant_random_death_chance
        self.__queen_avg_age = queen_avg_age
        self.__queen_avg_age_variation = queen_avg_age_variation
        self.__queen_hunger = queen_hunger
        self.__queen_laying_rate = queen_laying_rate
        self.__queen_avg_eggs = queen_avg_eggs
        self.__queen_avg_egg_variation = queen_avg_egg_variation
        self.__egg_avg_age = egg_avg_age
        self.__egg_avg_age_variation = egg_avg_age_variation
        self.__egg_hunger = egg_hunger
        self.__egg_evolve_chance = egg_evolve_chance
        self.__queen_avg_egg_age = queen_avg_egg_age
        self.__queen_avg_egg_age_variation = queen_avg_egg_age_variation
        self.__queen_egg_hunger = queen_egg_hunger
        self.__queen_egg_evolve_chance = queen_egg_evolve_chance

    def __check_positive(self, value: float, error_message: str):
        """
        Vérifie que la valeur est positive.
        """
        if value < 0:
            raise ValueError(error_message)

    def __check_between(
        self,
        value: float,
        error_message: str,
        min_value: float = 0,
        max_value: float = 0,
    ):
        """
        Vérifie que la valeur est entre deux valeurs.
        """
        if value < min_value or value > max_value:
            raise ValueError(error_message)

    @property
    def simulation_speed(self) -> float:
        """
        Vitesse de la simulation.
        """
        return self.__simulation_speed

    @simulation_speed.setter
    def simulation_speed(self, value: float):
        """
        Modifie la vitesse de la simulation.
        """
        self.__check_positive(value, "La vitesse de la simulation doit être positive.")
        self.__simulation_speed = value

    @property
    def initial_food_quantity(self) -> float:
        """
        Quantité de nourriture initiale.
        """
        return self.__initial_food_quantity

    @initial_food_quantity.setter
    def initial_food_quantity(self, value: float):
        """
        Modifie la quantité de nourriture initiale.
        """
        self.__check_positive(
            value, "La quantité de nourriture initiale doit être positive."
        )
        self.__initial_food_quantity = value

    @property
    def initial_ant_quantity(self) -> int:
        """
        Quantité de fourmis initiale.
        """
        return self.__initial_ant_quantity

    @initial_ant_quantity.setter
    def initial_ant_quantity(self, value: int):
        """
        Modifie la quantité de fourmis initiale.
        """
        self.__check_positive(
            value, "La quantité de fourmis initiale doit être positive."
        )
        self.__initial_ant_quantity = value

    @property
    def ant_avg_age(self) -> int:
        """
        Age moyen des fourmis.
        """
        return self.__ant_avg_age

    @ant_avg_age.setter
    def ant_avg_age(self, value: int):
        """
        Modifie l'age moyen des fourmis.
        """
        self.__check_positive(value, "L'age moyen des fourmis doit être positif.")
        self.__ant_avg_age = value

    @property
    def ant_avg_age_variation(self) -> int:
        """
        Variation de l'age moyen des fourmis.
        """
        return self.__ant_avg_age_variation

    @ant_avg_age_variation.setter
    def ant_avg_age_variation(self, value: int):
        """
        Modifie la variation de l'age moyen des fourmis.
        """
        self.__check_positive(
            value, "La variation de l'age moyen des fourmis doit être positive."
        )
        self.__ant_avg_age_variation = value

    @property
    def ant_worker_chance(self) -> float:
        """
        Chance qu'une fourmi soit une ouvrière.
        """
        return self.__ant_worker_chance

    @ant_worker_chance.setter
    def ant_worker_chance(self, value: float):
        """
        Modifie la chance qu'une fourmi soit une ouvrière.
        """
        self.__check_between(
            value,
            "La chance qu'une fourmi soit une ouvrière doit être comprise entre 0 et 1.",
        )
        self.__ant_worker_chance = value

    @property
    def min_food_multiplier(self) -> float:
        """
        Multiplicateur de la quantité de nourriture minimum.
        """
        return self.__min_food_multiplier

    @min_food_multiplier.setter
    def min_food_multiplier(self, value: float):
        """
        Modifie le multiplicateur de la quantité de nourriture minimum.
        """
        self.__check_positive(
            value,
            "Le multiplicateur de la quantité de nourriture minimum doit être positif.",
        )
        self.__min_food_multiplier = value

    @property
    def max_food_multiplier(self) -> float:
        """
        Multiplicateur de la quantité de nourriture maximum.
        """
        return self.__max_food_multiplier

    @max_food_multiplier.setter
    def max_food_multiplier(self, value: float):
        """
        Modifie le multiplicateur de la quantité de nourriture maximum.
        """
        self.__check_positive(
            value,
            "Le multiplicateur de la quantité de nourriture maximum doit être positif.",
        )
        self.__max_food_multiplier = value

    @property
    def ant_hunger(self) -> float:
        """
        Faim des fourmis.
        """
        return self.__ant_hunger

    @ant_hunger.setter
    def ant_hunger(self, value: float):
        """
        Modifie la faim des fourmis.
        """
        self.__check_positive(value, "La faim des fourmis doit être positive.")
        self.__ant_hunger = value

    @property
    def ant_random_death_chance(self) -> float:
        """
        Chance qu'une fourmi meurt aléatoirement.
        """
        return self.__ant_random_death_chance

    @ant_random_death_chance.setter
    def ant_random_death_chance(self, value: float):
        """
        Modifie la chance qu'une fourmi meurt aléatoirement.
        """
        self.__check_between(
            value,
            "La chance qu'une fourmi meurt aléatoirement doit être comprise entre 0 et 1.",
        )
        self.__ant_random_death_chance = value

    @property
    def queen_avg_age(self) -> int:
        """
        Age moyen de la reine.
        """
        return self.__queen_avg_age

    @queen_avg_age.setter
    def queen_avg_age(self, value: int):
        """
        Modifie l'age moyen de la reine.
        """
        self.__check_positive(value, "L'age moyen de la reine doit être positif.")
        self.__queen_avg_age = value

    @property
    def queen_avg_age_variation(self) -> int:
        """
        Variation de l'age moyen de la reine.
        """
        return self.__queen_avg_age_variation

    @queen_avg_age_variation.setter
    def queen_avg_age_variation(self, value: int):
        """
        Modifie la variation de l'age moyen de la reine.
        """
        self.__check_positive(
            value, "La variation de l'age moyen de la reine doit être positive."
        )
        self.__queen_avg_age_variation = value

    @property
    def queen_hunger(self) -> float:
        """
        Faim de la reine.
        """
        return self.__queen_hunger

    @queen_hunger.setter
    def queen_hunger(self, value: float):
        """
        Modifie la faim de la reine.
        """
        self.__check_positive(value, "La faim de la reine doit être positive.")
        self.__queen_hunger = value

    @property
    def queen_laying_rate(self) -> int:
        """
        Tout les combien de jours la reine pond des oeufs.
        """
        return self.__queen_laying_rate

    @queen_laying_rate.setter
    def queen_laying_rate(self, value: int):
        """
        Modifie le nombre de jours entre chaque ponte de la reine.
        """
        self.__check_positive(
            value,
            "Le nombre de jours entre chaque ponte de la reine doit être positif.",
        )
        self.__queen_laying_rate = value

    @property
    def queen_avg_eggs(self) -> int:
        """
        Nombre moyen d'oeufs pondus par la reine.
        """
        return self.__queen_avg_eggs

    @queen_avg_eggs.setter
    def queen_avg_eggs(self, value: int):
        """
        Modifie le nombre moyen d'oeufs pondus par la reine.
        """
        self.__check_positive(
            value, "Le nombre moyen d'oeufs pondus par la reine doit être positif."
        )
        self.__queen_avg_eggs = value

    @property
    def queen_avg_egg_variation(self) -> int:
        """
        Variation du nombre moyen d'oeufs pondus par la reine.
        """
        return self.__queen_avg_egg_variation

    @queen_avg_egg_variation.setter
    def queen_avg_egg_variation(self, value: int):
        """
        Modifie la variation du nombre moyen d'oeufs pondus par la reine.
        """
        self.__check_positive(
            value,
            "La variation du nombre moyen d'oeufs pondus par la reine doit être positive.",
        )
        self.__queen_avg_egg_variation = value

    @property
    def egg_avg_age(self) -> int:
        """
        Age moyen des oeufs.
        """
        return self.__egg_avg_age

    @egg_avg_age.setter
    def egg_avg_age(self, value: int):
        """
        Modifie l'age moyen des oeufs.
        """
        self.__check_positive(value, "L'age moyen des oeufs doit être positif.")
        self.__egg_avg_age = value

    @property
    def egg_avg_age_variation(self) -> int:
        """
        Variation de l'age moyen des oeufs.
        """
        return self.__egg_avg_age_variation

    @egg_avg_age_variation.setter
    def egg_avg_age_variation(self, value: int):
        """
        Modifie la variation de l'age moyen des oeufs.
        """
        self.__check_positive(
            value, "La variation de l'age moyen des oeufs doit être positive."
        )
        self.__egg_avg_age_variation = value

    @property
    def egg_hunger(self) -> float:
        """
        Faim des oeufs.
        """
        return self.__egg_hunger

    @egg_hunger.setter
    def egg_hunger(self, value: float):
        """
        Modifie la faim des oeufs.
        """
        self.__check_positive(value, "La faim des oeufs doit être positive.")
        self.__egg_hunger = value

    @property
    def egg_evolve_chance(self) -> float:
        """
        Chance qu'un oeuf évolue.
        """
        return self.__egg_evolve_chance

    @egg_evolve_chance.setter
    def egg_evolve_chance(self, value: float):
        """
        Modifie la chance qu'un oeuf évolue.
        """
        if value < 0 or value > 1:
            raise ValueError(
                "La chance qu'un oeuf évolue doit être comprise entre 0 et 1."
            )
        self.__egg_evolve_chance = value

    @property
    def queen_avg_egg_age(self) -> int:
        """
        Age moyen des oeufs de  reine.
        """
        return self.__queen_avg_egg_age

    @queen_avg_egg_age.setter
    def queen_avg_egg_age(self, value: int):
        """
        Modifie l'age moyen des oeufs de reine.
        """
        self.__check_positive(
            value, "L'age moyen des oeufs de reine doit être positif."
        )
        self.__queen_avg_egg_age = value

    @property
    def queen_avg_egg_age_variation(self) -> int:
        """
        Variation de l'age moyen des oeufs de reine.
        """
        return self.__queen_avg_egg_age_variation

    @queen_avg_egg_age_variation.setter
    def queen_avg_egg_age_variation(self, value: int):
        """
        Modifie la variation de l'age moyen des oeufs de reine.
        """
        self.__check_positive(
            value, "La variation de l'age moyen des oeufs de reine doit être positive."
        )
        self.__queen_avg_egg_age_variation = value

    @property
    def queen_egg_hunger(self) -> float:
        """
        Faim des oeufs de reine.
        """
        return self.__queen_egg_hunger

    @queen_egg_hunger.setter
    def queen_egg_hunger(self, value: float):
        """
        Modifie la faim des oeufs de reine.
        """
        self.__check_positive(value, "La faim des oeufs de reine doit être positive.")
        self.__queen_egg_hunger = value

    @property
    def queen_egg_evolve_chance(self) -> float:
        """
        Chance qu'un oeuf de reine évolue.
        """
        return self.__queen_egg_evolve_chance

    @queen_egg_evolve_chance.setter
    def queen_egg_evolve_chance(self, value: float):
        """
        Modifie la chance qu'un oeuf de reine évolue.
        """
        self.__check_between(
            value,
            "La chance qu'un oeuf de reine évolue doit être comprise entre 0 et 1.",
        )
        self.__queen_egg_evolve_chance = value

    def to_dict(self):
        """
        Convertit les paramètres en dictionnaire
        """
        return {
            "simulation_speed": self.simulation_speed,
            "initial_food_quantity": self.initial_food_quantity,
            "initial_ant_quantity": self.initial_ant_quantity,
            "ant_avg_age": self.ant_avg_age,
            "ant_avg_age_variation": self.ant_avg_age_variation,
            "ant_worker_chance": self.ant_worker_chance,
            "min_food_multiplier": self.min_food_multiplier,
            "max_food_multiplier": self.max_food_multiplier,
            "ant_hunger": self.ant_hunger,
            "ant_random_death_chance": self.ant_random_death_chance,
            "queen_avg_age": self.queen_avg_age,
            "queen_avg_age_variation": self.queen_avg_age_variation,
            "queen_hunger": self.queen_hunger,
            "queen_laying_rate": self.queen_laying_rate,
            "queen_avg_eggs": self.queen_avg_eggs,
            "queen_avg_egg_variation": self.queen_avg_egg_variation,
            "egg_avg_age": self.egg_avg_age,
            "egg_avg_age_variation": self.egg_avg_age_variation,
            "egg_hunger": self.egg_hunger,
            "egg_evolve_chance": self.egg_evolve_chance,
            "queen_avg_egg_age": self.queen_avg_egg_age,
            "queen_avg_egg_age_variation": self.queen_avg_egg_age_variation,
            "queen_egg_hunger": self.queen_egg_hunger,
            "queen_egg_evolve_chance": self.queen_egg_evolve_chance,
        }
