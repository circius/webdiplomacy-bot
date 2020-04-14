"""data for use in testing the various modules. should only be parsed
by pytest

"""
import os
from dipbot.data_definitions import Player, DipGame

THISDIR = os.path.dirname(__file__)

# this is a copy of a guest-accessible status-page for a public game at webdiplomacy.
pop_the_bee_html_filepath = os.path.join(THISDIR, "pop_the_bee.html")
with open(pop_the_bee_html_filepath, "r") as f:
    pop_the_bee_html = f.read()

# this is a hand-crafted [List of Players] corresponding the the
# current state of each of the pop_the_bee players
pop_the_bee_players = [
    {"name": "MichiganMan", "power": "France", "turn status": "Not received"},
    {"name": "Kestas Bot", "power": "Austria", "turn status": "Ready"},
    {"name": "Zultar Bot", "power": "England", "turn status": "Ready"},
    {"name": "Skynet", "power": "Germany", "turn status": "Ready"},
    {"name": "Data", "power": "Italy", "turn status": "Ready"},
    {"name": "Jane", "power": "Turkey", "turn status": "Ready"},
    {"name": "Cortana", "power": "Russia", "turn status": "Ready"},
]

# this is a hand-crafted DipGame representing the current state of the
# game pop_the_bee
pop_the_bee_DipGame = {
    "name": "Pop the Bee",
    "year": 1904,
    "season": "Spring",
    "phase": "diplomacy",
    "players": pop_the_bee_players,
}

pop_the_bee_retreats_DipGame = {
    "name": "Pop the Bee",
    "year": 1905,
    "season": "Autumn",
    "phase": "retreats",
    "players": pop_the_bee_players,
}

pop_the_bee_builds_DipGame = {
    "name": "Pop the Bee",
    "year": 1905,
    "season": "Autumn",
    "phase": "builds",
    "players": pop_the_bee_players,
}
