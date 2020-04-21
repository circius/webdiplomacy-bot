""" data definitions for dipbot
"""
from typing import NewType, Dict

""" A DipGame is a Dictionary with the following compulsory entries:
        'name' -> str
        'year' -> int
        'season' -> str
        'phase' -> Phase
        'players' -> [list of Player]
        'started' -> Union[int, None]
        'deadline' -> Union[int, None] 
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

""" A Phase is one of:
 - "diplomacy"
 - "retreats"
 - "builds"
 - "finished"
"""

Phase = NewType("Phase", str)
