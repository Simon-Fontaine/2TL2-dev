import sys
import os
import time
import json
import random
import datetime
import enum
from typing import List, Union

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.prompt import Confirm, IntPrompt, FloatPrompt
from rich.panel import Panel

YEAR = 365
MONTH = YEAR // 12
WEEK = MONTH // 4
SAVE_DIRECTORY = "saves"


class State(enum.Enum):
    ALIVE = 1
    DEAD = 0


class Job(enum.Enum):
    WORKER = 1
    NOT_WORKER = 0


class Settings:
    def __init__(
        self,
        simulation_speed: float = 1.0,
        initial_food_quantity: float = 30000,
        initial_ant_quantity: int = 100,
        ant_avg_age: int = 90,
        ant_avg_age_variation: int = 20,
        ant_worker_chance: float = 0.95,
        min_food_multiplier: float = 0.5,
        max_food_multiplier: float = 1.5,
        ant_hunger: float = 0.3,
        ant_random_death_chance: float = 0.01,
        queen_avg_age: int = 5 * YEAR,
        queen_avg_age_variation: int = 1 * YEAR,
        queen_hunger: float = 10,
        queen_laying_rate: int = 5,
        queen_avg_eggs: int = 500,
        queen_avg_egg_variation: int = 150,
        egg_avg_age: int = 2 * WEEK,
        egg_avg_age_variation: int = 1 * WEEK,
        egg_hunger: float = 0.1,
        egg_evolve_chance: float = 0.9,
        queen_avg_egg_age: int = 2 * MONTH,
        queen_avg_egg_age_variation: int = 2 * WEEK,
        queen_egg_hunger: float = 1,
        queen_egg_evolve_chance: float = 0.5,
    ):
        self.simulation_speed = simulation_speed
        self.initial_food_quantity = initial_food_quantity
        self.initial_ant_quantity = initial_ant_quantity
        self.ant_avg_age = ant_avg_age
        self.ant_avg_age_variation = ant_avg_age_variation
        self.ant_worker_chance = ant_worker_chance
        self.min_food_multiplier = min_food_multiplier
        self.max_food_multiplier = max_food_multiplier
        self.ant_hunger = ant_hunger
        self.ant_random_death_chance = ant_random_death_chance
        self.queen_avg_age = queen_avg_age
        self.queen_avg_age_variation = queen_avg_age_variation
        self.queen_hunger = queen_hunger
        self.queen_laying_rate = queen_laying_rate
        self.queen_avg_eggs = queen_avg_eggs
        self.queen_avg_egg_variation = queen_avg_egg_variation
        self.egg_avg_age = egg_avg_age
        self.egg_avg_age_variation = egg_avg_age_variation
        self.egg_hunger = egg_hunger
        self.egg_evolve_chance = egg_evolve_chance
        self.queen_avg_egg_age = queen_avg_egg_age
        self.queen_avg_egg_age_variation = queen_avg_egg_age_variation
        self.queen_egg_hunger = queen_egg_hunger
        self.queen_egg_evolve_chance = queen_egg_evolve_chance

    def to_dict(self):
        return vars(self)


class Food:
    def __init__(self, settings: Settings):
        self._quantity = settings.initial_food_quantity

    def remove(self, amount: (int, float) = 1):
        self._quantity = max(self._quantity - amount, 0)

    def add(self, amount: (int, float) = 1):
        self._quantity += amount

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value


class Ant:
    def __init__(self, settings: Settings, food: Food):
        self._age = 0
        self._max_age = random.randint(
            settings.ant_avg_age - settings.ant_avg_age_variation,
            settings.ant_avg_age + settings.ant_avg_age_variation,
        )
        self._state = State.ALIVE
        self._is_worker = (
            Job.WORKER
            if random.random() < settings.ant_worker_chance
            else Job.NOT_WORKER
        )

        self._settings = settings
        self._food = food

    @property
    def is_alive(self) -> bool:
        return self._state == State.ALIVE

    @property
    def is_worker(self) -> bool:
        return self._is_worker == Job.WORKER

    def evolve(self):
        if self.is_alive and self._food.quantity >= self._settings.ant_hunger:
            self._age += 1
            self._food.remove(self._settings.ant_hunger)
            if (
                self._age > self._max_age
                or random.random() < self._settings.ant_random_death_chance
            ):
                self._state = State.DEAD
        else:
            self._state = State.DEAD


class Egg:
    def __init__(self, settings: Settings, food: Food, is_queen_egg=False):
        self._age = 0
        self._max_age = (
            random.randint(
                settings.queen_avg_egg_age - settings.queen_avg_egg_age_variation,
                settings.queen_avg_egg_age + settings.queen_avg_egg_age_variation,
            )
            if is_queen_egg
            else random.randint(
                settings.egg_avg_age - settings.egg_avg_age_variation,
                settings.egg_avg_age + settings.egg_avg_age_variation,
            )
        )
        self._state = State.ALIVE
        self._is_queen_egg = is_queen_egg

        self._settings = settings
        self._food = food

    @property
    def is_alive(self) -> bool:
        return self._state == State.ALIVE

    def evolve(self) -> Ant or None:
        if self.is_alive and self._food.quantity >= self._settings.egg_hunger:
            self._age += 1
            self._food.remove(
                self._settings.queen_egg_hunger
                if self._is_queen_egg
                else self._settings.egg_hunger
            )
            if self._age > self._max_age:
                self._state = State.DEAD
                if self._is_queen_egg:
                    if random.random() < self._settings.queen_egg_evolve_chance:
                        return Queen(self._settings, self._food)
                else:
                    if random.random() < self._settings.egg_evolve_chance:
                        return Ant(self._settings, self._food)
        else:
            self._state = State.DEAD
        return None


class Queen(Ant):
    def __init__(self, settings: Settings, food: Food):
        super().__init__(settings, food)
        self._max_age = random.randint(
            settings.queen_avg_age - settings.queen_avg_age_variation,
            settings.queen_avg_age + settings.queen_avg_age_variation,
        )
        self._is_worker = Job.NOT_WORKER

    def evolve(self):
        if self.is_alive and self._food.quantity >= self._settings.queen_hunger:
            self._age += 1
            self._food.remove(self._settings.queen_hunger)

            if self._age >= self._max_age - 1:
                self._state = State.DEAD
                return self.lay_successor_egg()

        else:
            self._state = State.DEAD
        return None

    def lay_eggs(self) -> [Egg]:
        new_eggs = []
        if self.is_alive and self._food.quantity >= self._settings.queen_hunger:
            self._food.remove(self._settings.queen_hunger)
            for _ in range(
                random.randint(
                    self._settings.queen_avg_eggs
                    - self._settings.queen_avg_egg_variation,
                    self._settings.queen_avg_eggs
                    + self._settings.queen_avg_egg_variation,
                )
            ):
                new_eggs.append(Egg(self._settings, self._food))
        return new_eggs

    def lay_successor_egg(self) -> Egg:
        return Egg(self._settings, self._food, is_queen_egg=True)


class Colony:
    def __init__(self, settings: Settings, food: Food):
        self._day = 0
        self._ants = [Ant(settings, food) for _ in range(settings.initial_ant_quantity)]
        self._born_ants = settings.initial_ant_quantity + 1
        self._queen = Queen(settings, food)
        self._eggs = []
        self._settings = settings
        self._food = food

    @property
    def day(self) -> int:
        return self._day

    @property
    def queen(self) -> Queen:
        return self._queen

    @property
    def food(self) -> Food:
        return self._food

    @property
    def ants(self) -> [Ant]:
        return self._ants

    @property
    def eggs(self) -> [Egg]:
        return self._eggs

    def ant_count(self) -> int:
        return len(self._ants) + int(self._queen.is_alive)

    def dead_ant_count(self) -> int:
        return self._born_ants - self.ant_count()

    def worker_count(self) -> int:
        return len([worker for worker in self._ants if worker.is_worker])

    def egg_count(self) -> int:
        return len(self._eggs)

    def _update_food(self):
        self._food.add(
            random.randint(
                round(self.worker_count() * self._settings.min_food_multiplier),
                round(self.worker_count() * self._settings.max_food_multiplier),
            )
        )

    def _update_ants(self):
        successor_egg = self._queen.evolve()
        if successor_egg:
            self._eggs.append(successor_egg)

        for ant in self._ants:
            ant.evolve()
        self._ants = [ant for ant in self._ants if ant.is_alive]

    def _lay_eggs(self):
        if self._day % self._settings.queen_laying_rate == 0:
            self._eggs.extend(self._queen.lay_eggs())

    def _update_eggs(self):
        new_queen = None
        for egg in self._eggs:
            new_ant = egg.evolve()
            if new_ant:
                if isinstance(new_ant, Queen):
                    new_queen = new_ant
                else:
                    self._ants.append(new_ant)
                    self._born_ants += 1
        self._eggs = [egg for egg in self._eggs if egg.is_alive]

        if new_queen and not self._queen.is_alive:
            self._queen = new_queen

    def evolve(self):
        self._update_food()
        self._update_ants()
        self._update_eggs()
        self._lay_eggs()
        self._day += 1


def create_table(
    header_style="bold cyan", column_styles=("bold blue", "yellow")
) -> Table:
    """
    Crée un tableau avec les styles donnés
    """
    table = Table(
        show_header=True,
        header_style=header_style,
        title_style="bold magenta",
        min_width=60,
    )
    table.add_column("Metric", style=column_styles[0], max_width=20)
    table.add_column("Value", style=column_styles[1], max_width=40)
    return table


def print_parameters(settings: Settings) -> Table:
    """
    Affiche les paramètres de la simulation dans un tableau
    """
    table = create_table()

    for attr, value in settings.__dict__.items():
        table.add_row(attr.replace("_", " ").title(), str(value))

    return table


def days_to_string(days: int) -> str:
    """
    Convertit le nombre de jours en une chaîne de caractères
    """
    years = days // YEAR
    remaining_days = days % YEAR
    months = remaining_days // MONTH
    remaining_days = remaining_days % MONTH
    weeks = remaining_days // WEEK
    remaining_days = remaining_days % WEEK

    return f"~ {years} years, {months} months, {weeks} weeks, {remaining_days} days"


def print_simulation_results(colony: Colony) -> Table:
    """
    Affiche les résultats de la simulation dans un tableau
    """
    table = create_table()
    table.add_row("Total Time", days_to_string(colony.day))
    table.add_row("Days", str(colony.day))
    table.add_row("Eggs", str(colony.egg_count()))
    table.add_row("Ants", str(colony.ant_count()))
    table.add_row("Workers", str(colony.worker_count()))
    table.add_row("Food", str(colony.food.quantity.__round__(2)))
    table.add_row("Queen", "Alive" if colony.queen.is_alive else "Deceased")
    table.add_row("Dead Ants", str(colony.dead_ant_count()))
    return table


def ensure_save_directory_exists():
    """
    Vérifie que le dossier de sauvegarde existe
    """
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)


def list_save_files() -> List[str]:
    """
    Liste les fichiers de sauvegarde disponibles
    """
    files = os.listdir(SAVE_DIRECTORY)
    return [f for f in files if f.startswith("simulation_") and f.endswith(".json")]


def display_save_files(console: Console) -> dict:
    """
    Affiche les fichiers de sauvegarde disponibles et retourne un mapping
    """
    save_files = list_save_files()
    save_mapping = {}
    for i, file in enumerate(save_files, start=1):
        unique_id = file.replace("simulation_", "").replace(".json", "")
        save_mapping[str(i)] = unique_id
        console.print(f"{i}. Simulation ID: {unique_id}")
    return save_mapping


def generate_file_name() -> str:
    """
    Génère un nom de fichier unique pour la sauvegarde de la simulation
    """
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    simulation_count = len(list_save_files()) + 1
    return f"saves/simulation_{simulation_count}_{date_str}.json"


def save_simulation_results(settings: Settings, colony: Colony) -> str:
    """
    Sauvegarde les résultats de la simulation dans un fichier JSON
    """
    filename = generate_file_name()
    data = {
        "settings": settings.to_dict(),
        "results": {
            "total_time": days_to_string(colony.day),
            "days": colony.day,
            "eggs": colony.egg_count(),
            "ants": colony.ant_count(),
            "workers": colony.worker_count(),
            "food": colony.food.quantity.__round__(2),
            "queen": colony.queen.is_alive,
            "dead_ants": colony.dead_ant_count(),
        },
    }
    with open(filename, "w", encoding="utf8") as file:
        json.dump(data, file, indent=2)
    return filename


def prompt_simulation_settings(console: Console) -> Settings:
    """
    Demande à l'utilisateur les paramètres de la simulation
    """
    console.clear()
    default_settings = Settings()

    console.print(
        Panel(
            "Simulation Settings",
            safe_box=True,
            border_style="cyan",
            title="Options",
            title_align="left",
            width=60,
            highlight=True,
        ),
    )

    sim_initial_ants = IntPrompt.ask(
        "Initial number of ants", default=default_settings.initial_ant_quantity
    )
    sim_initial_food = IntPrompt.ask(
        "Initial amount of food", default=default_settings.initial_food_quantity
    )
    sim_initial_speed = FloatPrompt.ask(
        "Simulation speed in seconds per day", default=default_settings.simulation_speed
    )

    return Settings(
        simulation_speed=sim_initial_speed,
        initial_food_quantity=sim_initial_food,
        initial_ant_quantity=sim_initial_ants,
    )


def load_simulation_settings(file_id: str) -> Union[Settings, None]:
    """
    Charge les paramètres d'une simulation à partir d'un fichier
    """
    filename = f"{SAVE_DIRECTORY}/simulation_{file_id}.json"
    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf8") as file:
        data = json.load(file)
        settings_data = data["settings"]
        return Settings(**settings_data)


def run_simulation(console: Console, new_simulation: bool = True, file_id: str = None):
    """
    Lance une simulation avec les paramètres donnés
    """
    console.clear()

    if new_simulation:
        settings = prompt_simulation_settings(console)
    else:
        settings = load_simulation_settings(file_id)

    if not settings:
        return main()

    console.print(print_parameters(settings))
    if not Confirm.ask("Do you want to use these settings ?"):
        return main()

    sim_food = Food(settings)
    sim_colony = Colony(settings, sim_food)

    with Live(auto_refresh=False) as live:
        while sim_colony.ants or sim_colony.queen.is_alive or sim_colony.eggs:
            sim_colony.evolve()
            live.update(print_simulation_results(sim_colony))
            live.refresh()
            time.sleep(settings.simulation_speed)

    console.print(
        Panel(
            "Simulation completed. The results are displayed above.",
            safe_box=True,
            border_style="green",
            title="Simulation Completed",
            title_align="left",
            width=60,
            highlight=True,
        ),
    )

    saved_file_path = save_simulation_results(settings, sim_colony)
    console.print(
        Panel(
            f"Simulation saved to {saved_file_path}",
            safe_box=True,
            border_style="yellow",
            title="Simulation Saved",
            title_align="left",
            width=60,
            highlight=True,
        ),
    )

    if Confirm.ask("Do you want to start a new simulation ?"):
        return main()

    sys.exit()


def show_options(
    console: Console, no_saves: bool = False, invalid_choice: bool = False
):
    """
    Montre les options disponibles à l'utilisateur
    """
    console.clear()
    console.print(
        Panel(
            "[1] Start New Simulation\n[2] Load Existing Simulation\n[3] Exit",
            safe_box=True,
            border_style="cyan",
            title="Options",
            title_align="left",
            width=60,
            highlight=True,
        ),
    )
    if no_saves:
        console.print(
            Panel(
                "No Saves Found",
                safe_box=True,
                border_style="red",
                title="Error",
                title_align="left",
                width=60,
                highlight=True,
            ),
        )
    if invalid_choice:
        console.print(
            Panel(
                "Invalid Choice",
                safe_box=True,
                border_style="red",
                title="Error",
                title_align="left",
                width=60,
                highlight=True,
            ),
        )


def main(no_saves: bool = False, invalid_choice: bool = False):
    console = Console()
    ensure_save_directory_exists()
    show_options(console, no_saves, invalid_choice)
    choice = console.input("[bold blue]Please choose an option: [/bold blue]")

    if choice == "1":
        run_simulation(console)
    elif choice == "2":
        save_files = list_save_files()
        if not save_files:
            return main(no_saves=True)

        save_mapping = display_save_files(console)
        file_choice = console.input(
            "[bold blue]Enter the number or Save ID to load: [/bold blue]"
        )
        chosen_id = save_mapping.get(file_choice, file_choice)

        if chosen_id not in save_mapping.values():
            return main(invalid_choice=True)

        run_simulation(console, new_simulation=False, file_id=chosen_id)
    elif choice == "3":
        sys.exit()
    else:
        return main(invalid_choice=True)


if __name__ == "__main__":
    main()
