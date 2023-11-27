"""
Ce module contient la classe Queen
"""

import random

from src.classes.food import Food
from src.classes.settings import Settings
from src.classes.enums import State, Job

from src.classes.ant import Ant
from src.classes.egg import Egg


class Queen(Ant):
    def __init__(self, settings: Settings, food: Food):
        super().__init__(settings, food)
        self.max_age = random.randint(
            settings.queen_avg_age - settings.queen_avg_age_variation,
            settings.queen_avg_age + settings.queen_avg_age_variation,
        )
        self.is_worker = Job.NOT_WORKER

    def evolve(self):
        if self.is_alive and self.food.quantity >= self.settings.queen_hunger:
            self.age += 1
            self.food.remove(self.settings.queen_hunger)

            if self.age >= self.max_age - 1:
                self.state = State.DEAD
                return self.lay_successor_egg()

        else:
            self.state = State.DEAD
        return None

    def lay_eggs(self) -> [Egg]:
        """
        Pond des oeufs
        """
        new_eggs = []
        if self.is_alive and self.food.quantity >= self.settings.queen_hunger:
            self.food.remove(self.settings.queen_hunger)
            for _ in range(
                random.randint(
                    self.settings.queen_avg_eggs
                    - self.settings.queen_avg_egg_variation,
                    self.settings.queen_avg_eggs
                    + self.settings.queen_avg_egg_variation,
                )
            ):
                new_eggs.append(Egg(self.settings, self.food))
        return new_eggs

    def lay_successor_egg(self) -> Egg:
        """
        Pond un oeuf de reine
        """
        return Egg(self.settings, self.food, is_queen_egg=True)
