import unittest
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Queen, Egg, Settings, Food, State, Job


class TestQueen(unittest.TestCase):

    def setUp(self):
        """Set up a Queen object with default settings before each test."""
        self.settings = Settings()
        self.food = Food(self.settings)
        self.queen = Queen(self.settings, self.food)

    def test_initial_state(self):
        """Test if the Queen initializes with the correct initial state."""
        self.assertEqual(self.queen._state, State.ALIVE)
        self.assertTrue(0 <= self.queen._age <= self.settings.queen_avg_age + self.settings.queen_avg_age_variation)
        self.assertEqual(self.queen._is_worker, Job.NOT_WORKER)

    def test_evolve_method_alive(self):
        """Test if the evolve method correctly ages the queen and consumes food when alive."""
        initial_food_quantity = self.food.quantity
        self.queen.evolve()
        self.assertEqual(self.queen._age, 1)
        self.assertEqual(self.food.quantity, initial_food_quantity - self.settings.queen_hunger)

    def test_evolve_method_death_by_age(self):
        """Test if the evolve method correctly sets the queen's state to DEAD due to age."""
        self.queen._age = self.queen._max_age + 1  # Set age beyond max age
        self.queen.evolve()
        self.assertEqual(self.queen._state, State.DEAD)

    def test_evolve_method_death_by_starvation(self):
        """Test if the evolve method correctly sets the queen's state to DEAD due to starvation."""
        self.food.quantity = 0  # No food available
        self.queen.evolve()
        self.assertEqual(self.queen._state, State.DEAD)

    def test_lay_eggs_method(self):
        """Test if the lay_eggs method correctly produces eggs."""
        self.queen._age = self.settings.queen_avg_age - 1  # Set age close to max age for laying eggs
        eggs = self.queen.lay_eggs()
        self.assertTrue(all(isinstance(egg, Egg) for egg in eggs))
        self.assertTrue(len(eggs) > 0)


if __name__ == '__main__':
    unittest.main()
