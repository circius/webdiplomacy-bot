# -*- coding: utf-8 -*-
"""encapsulates functions which generate strings reporting the state
of DipGames.

"""
from dipbot.data_definitions import DipGame, Player
from typing import List


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


def dipgame_get_uncommitted_players(state: DipGame) -> List[Player]:
    """ consumes a DipGame and produces a list of those players who haven't yet committed their turns.
"""
    return [player for player in state["players"] if player["turn status"] != "Ready"]
