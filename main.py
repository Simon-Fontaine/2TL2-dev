"""
Fichier principal du projet.
"""
from src.utils.files import create_save_file

from src.classes.colony import Colony
from src.classes.settings import Settings
from src.classes.food import Food

if __name__ == "__main__":
    settings = Settings()
    food = Food(settings)
    colony = Colony(settings, food)
    create_save_file(settings, colony)
