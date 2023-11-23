import unittest
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Ant, Settings, Food, State, Job


class TestAnt(unittest.TestCase):

    def setUp(self):
        """Set up la fourmi et la nourriture pour les tests."""
        self.settings = Settings()
        self.food = Food(self.settings)
        self.ant = Ant(self.settings, self.food)

    def test_initial_state(self):
        """Test si la fourmi est créée avec les bons attributs."""
        self.assertEqual(self.ant._state, State.ALIVE)
        self.assertTrue(0 <= self.ant._age <= self.settings.ant_avg_age + self.settings.ant_avg_age_variation)
        self.assertIn(self.ant._is_worker, [Job.WORKER, Job.NOT_WORKER])

    def test_evolve_method_alive(self):
        """Test si la méthode evolve fonctionne correctement pour une fourmi vivante."""
        initial_food_quantity = self.food.quantity
        self.ant.evolve()
        self.assertEqual(self.ant._age, 1)
        self.assertEqual(self.food.quantity, initial_food_quantity - self.settings.ant_hunger)

    def test_evolve_method_death_by_age(self):
        """Test si la méthode evolve met la fourmi à l'état DEAD si elle est trop vieille."""
        self.ant._age = self.ant._max_age + 1  # Met l'âge de la fourmi à 1 jour de sa mort
        self.ant.evolve()
        self.assertEqual(self.ant._state, State.DEAD)

    def test_evolve_method_death_by_starvation(self):
        """Test si la methode evolve met la fourmi à l'état DEAD si elle n'a pas assez de nourriture."""
        self.food.quantity = 0  # Met la quantité de nourriture à 0
        self.ant.evolve()
        self.assertEqual(self.ant._state, State.DEAD)

    def test_evolve_method_death_by_random_chance(self):
        """Test si la méthode evolve met la fourmi à l'état DEAD si elle meurt au hasard."""
        random.seed(0)  # Fixe la seed aléatoire pour que le test soit reproductible
        self.ant._age = self.ant._max_age - 1
        self.ant.evolve()
        expected_state = State.DEAD if random.random() < self.settings.ant_random_death_chance else State.ALIVE
        self.assertEqual(self.ant._state, expected_state)


if __name__ == '__main__':
    unittest.main()
