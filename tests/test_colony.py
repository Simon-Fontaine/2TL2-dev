import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Colony, Settings, Food, Queen


class TestColony(unittest.TestCase):

    def setUp(self):
        """Set up la colonie, la nourriture et la reine pour les tests."""
        self.settings = Settings()
        self.food = Food(self.settings)
        self.colony = Colony(self.settings, self.food)

    def test_initial_state(self):
        """Test si la colonie est créée avec les bons attributs."""
        self.assertEqual(len(self.colony._ants), self.settings.initial_ant_quantity)
        self.assertIsInstance(self.colony._queen, Queen)
        self.assertEqual(len(self.colony._eggs), 0)
        self.assertEqual(self.colony._day, 0)

    def test_evolve_method(self):
        """Test si la méthode evolve incrémente le jour de 1."""
        initial_day = self.colony._day
        self.colony.evolve()
        self.assertEqual(self.colony._day, initial_day + 1)

    def test_ant_count_method(self):
        """Test si la méthode ant_count retourne le bon nombre de fourmis."""
        expected_count = len([ant for ant in self.colony._ants if ant.is_alive]) + int(self.colony._queen.is_alive)
        self.assertEqual(self.colony.ant_count(), expected_count)

    def test_egg_count_method(self):
        """Test si la méthode egg_count retourne le bon nombre d'oeufs."""
        self.assertEqual(self.colony.egg_count(), len(self.colony._eggs))

    def test_worker_count_method(self):
        """Test si la méthode worker_count retourne le bon nombre de fourmis travailleuses."""
        worker_count = len([ant for ant in self.colony._ants if ant.is_worker])
        self.assertEqual(self.colony.worker_count(), worker_count)


if __name__ == '__main__':
    unittest.main()
