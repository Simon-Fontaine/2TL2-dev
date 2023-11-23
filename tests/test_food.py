import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Food, Settings


class TestFood(unittest.TestCase):

    def setUp(self):
        """Set up a Food object with default settings before each test."""
        self.settings = Settings()
        self.food = Food(self.settings)

    def test_initial_quantity(self):
        """Test if Food initializes with the correct initial quantity."""
        self.assertEqual(self.food.quantity, self.settings.initial_food_quantity)

    def test_add_method(self):
        """Test if the add method correctly increases the food quantity."""
        initial_quantity = self.food.quantity
        self.food.add(100)
        self.assertEqual(self.food.quantity, initial_quantity + 100)

    def test_remove_method(self):
        """Test if the remove method correctly decreases the food quantity."""
        initial_quantity = self.food.quantity
        self.food.remove(50)
        self.assertEqual(self.food.quantity, initial_quantity - 50)

    def test_remove_method_no_negative(self):
        """Test if the remove method does not allow the quantity to go negative."""
        self.food.remove(1e6)  # Remove a large amount to ensure quantity would go negative
        self.assertEqual(self.food.quantity, 0)


if __name__ == '__main__':
    unittest.main()
