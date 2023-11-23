import unittest
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Egg, Ant, Queen, Settings, Food, State


class TestEgg(unittest.TestCase):

    def setUp(self):
        """Set up an Egg object with default settings before each test."""
        self.settings = Settings()
        self.food = Food(self.settings)
        self.egg = Egg(self.settings, self.food)

    def test_initial_state(self):
        """Test if the Egg initializes with the correct initial state."""
        self.assertEqual(self.egg._state, State.ALIVE)
        self.assertTrue(0 <= self.egg._age <= self.settings.egg_avg_age + self.settings.egg_avg_age_variation)

    def test_evolve_method_alive(self):
        """Test if the evolve method correctly ages the egg and consumes food when alive."""
        initial_food_quantity = self.food.quantity
        self.egg.evolve()
        self.assertEqual(self.egg._age, 1)
        self.assertEqual(self.food.quantity, initial_food_quantity - self.settings.egg_hunger)

    def test_evolve_method_death_by_age(self):
        """Test if the evolve method correctly sets the egg's state to DEAD due to age."""
        self.egg._age = self.egg._max_age + 1  # Set age beyond max age
        self.egg.evolve()
        self.assertEqual(self.egg._state, State.DEAD)

    def test_evolve_method_death_by_starvation(self):
        """Test if the evolve method correctly sets the egg's state to DEAD due to starvation."""
        self.food.quantity = 0  # No food available
        self.egg.evolve()
        self.assertEqual(self.egg._state, State.DEAD)

    def test_evolve_method_hatching(self):
        """Test if the evolve method correctly hatches the egg into an Ant or Queen."""
        self.egg._age = self.egg._max_age  # Set age at max age for hatching
        random.seed(0)  # Seed random number generator for predictability in tests
        hatched_ant = self.egg.evolve()
        self.assertIsInstance(hatched_ant, (Ant, Queen))
        self.assertEqual(self.egg._state, State.DEAD)


if __name__ == '__main__':
    unittest.main()
