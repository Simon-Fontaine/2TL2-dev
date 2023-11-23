import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Settings

class TestSettings(unittest.TestCase):

    def test_default_initialization(self):
        """Test if Settings initializes with default values correctly."""
        settings = Settings()
        self.assertEqual(settings.simulation_speed, 1.0)
        self.assertEqual(settings.initial_food_quantity, 30000)
        self.assertEqual(settings.initial_ant_quantity, 100)
        self.assertEqual(settings.ant_avg_age, 90)
        # Add assertions for all other default values...

    def test_custom_initialization(self):
        """Test if Settings initializes with custom values correctly."""
        custom_values = {
            'simulation_speed': 2.0,
            'initial_food_quantity': 50000,
            'initial_ant_quantity': 200,
            # Add custom values for all other settings...
        }
        settings = Settings(**custom_values)
        for key, value in custom_values.items():
            self.assertEqual(getattr(settings, key), value)

    def test_to_dict_method(self):
        """Test if the to_dict method returns a dictionary representation of settings."""
        settings = Settings()
        settings_dict = settings.to_dict()
        self.assertIsInstance(settings_dict, dict)
        for key in vars(settings).keys():
            self.assertIn(key, settings_dict)
            self.assertEqual(settings_dict[key], getattr(settings, key))

if __name__ == '__main__':
    unittest.main()
