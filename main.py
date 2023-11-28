"""
Fichier principal du projet.
"""
import sys

from rich.console import Console

from src.classes.settings import Settings

from src.utils.prompt import (
    prompt_initial_settings,
    prompt_options,
    prompt_files_to_load,
)
from src.utils.files import list_save_files, load_save_file
from src.utils.run_simulation import run_simulation


def main(no_saves=False):
    """
    Fonction principale
    """
    console = Console()

    user_choice = prompt_options(console, no_saves)

    if user_choice == "1":
        settings = prompt_initial_settings(console)

        if run_simulation(console, settings):
            return main()
        return sys.exit()
    if user_choice == "2":
        save_files = list_save_files()
        if not save_files:
            return main(no_saves=True)

        file = prompt_files_to_load(console, save_files)

        if file == "back":
            return main()

        settings = load_save_file(file)
        if run_simulation(console, Settings(**settings)):
            return main()
        return sys.exit()
    if user_choice == "3":
        return sys.exit()


if __name__ == "__main__":
    main()
