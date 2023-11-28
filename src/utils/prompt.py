"""
Ce module contient les fonctions permettant de prompt l'utilisateur
"""

from rich.console import Console
from rich.prompt import IntPrompt, FloatPrompt, Prompt

from src.classes.settings import Settings

from src.utils.panel import create_panel


def prompt_initial_settings(console: Console) -> Settings:
    """
    Demande les paramètres initiaux
    """
    console.clear()
    default_settings = Settings()

    initial_simulation_speed = FloatPrompt.ask(
        "Initial simulation speed (in seconds)",
        default=default_settings.simulation_speed,
    )
    initial_ant_quantity = IntPrompt.ask(
        "Initial ant quantity", default=default_settings.initial_ant_quantity
    )
    initial_food_quantity = IntPrompt.ask(
        "Initial food quantity", default=default_settings.initial_food_quantity
    )

    return Settings(
        simulation_speed=initial_simulation_speed,
        initial_ant_quantity=initial_ant_quantity,
        initial_food_quantity=initial_food_quantity,
    )


def prompt_options(console: Console, no_saves: bool = False) -> str:
    """
    Demande les options
    """
    console.clear()

    console.print(
        create_panel(
            "[1] Start New Simulation\n[2] Load Existing Simulation\n[3] Exit",
            "cyan",
            "Options",
        )
    )

    if no_saves:
        console.print(
            create_panel(
                "No saves were found.",
                "red",
                "Error",
            )
        )

    return Prompt.ask("Please choose an option :", choices=["1", "2", "3"], default="1")


def prompt_files_to_load(console: Console, files: dict) -> str:
    """
    Affiche et demande le fichier à charger
    """
    console = Console()
    console.clear()

    console.print(
        create_panel(
            "Please choose a save file.",
            "cyan",
            "Options",
        )
    )

    console.print("[0] Go back")
    for index, file in files.items():
        console.print(f"[{index}] {file}")

    unique_id = Prompt.ask(
        "Please choose an option :",
        choices=[str(i) for i in range(len(files) + 1)],
        default="1",
    )

    return files[unique_id] if unique_id != "0" else "back"
