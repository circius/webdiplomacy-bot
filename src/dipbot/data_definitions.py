""" data definitions for dipbot
"""
from typing import NewType, Dict

""" A DipGame is a Dictionary with the following compulsory entries:
        'name' -> str
        'year' -> int
        'season' -> str
        'retreats?' -> bool
        'players' -> [list of Player]
"""

DipGame = NewType("DipGame", Dict)

""" A Player is a Dictionary with the following compulsory entries:
        'name' -> str
        'power' -> str
        'turn status' -> Turn
"""

Player = NewType("Player", Dict)

""" A Turn is one of:
 - "Not received"
 - "Completed"
 - "Ready"
"""

Turn = NewType("Turn", str)
