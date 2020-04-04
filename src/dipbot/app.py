# -*- coding: utf-8 -*-
"""encapsulates functions which generate strings reporting the state
of DipGames.

"""
from dipbot.data_definitions import DipGame, Player
from typing import List, Union
import os

WEBDIP_ID_ENV_VAR_NAME = "WEBDIP_GAME_ID"


def get_env_var_checked(varname: str) -> Union[str, bool]:
    """gets the value of an environment variable. raises an exception and
returns False if the variable is not set.

    """
    value = os.getenv(varname)
    try:
        assert value != None and value != ""
    except AssertionError:
        print(f"{varname} unset! terminating...")
        return False
    return value


def announce_overall_game_state(state: DipGame) -> str:
    """Consumes a DipGame and produces a string summarising the game
state.

    """

    waiting_for = dipgame_get_uncommitted_players(state)

    return f"""It is the {state['season']} of {state['year']}.
We are awaiting the orders of:
{format_the_tardy_list(waiting_for)}"""


def format_the_tardy_list(lop: List[Player]) -> str:
    """ formats the list of players we're waiting for, façon HTDP
"""
    if len(lop) == 0:
        return ""
    else:
        player = lop[0]
        rest = lop[1:]
        return f"""  - {player['name']}, whose orders are {player['turn status'].lower()}
{format_the_tardy_list(rest)}"""


def player_is_not_ready(player: Player) -> bool:
    """consumes a player and produces true if the player hasn't yet
committed their orders.

    """
    status = player["turn status"]
    return not (status == "Ready" or status == "D")


def dipgame_get_uncommitted_players(state: DipGame) -> List[Player]:
    """ consumes a DipGame and produces a list of those players who haven't yet committed their turns.
"""
    return [player for player in state["players"] if player_is_not_ready(player)]
