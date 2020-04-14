# -*- coding: utf-8 -*-
"""encapsulates functions which generate strings reporting the state
of DipGames.

"""
from dipbot.data_definitions import DipGame, Player, Phase
from dipbot import utilities
from typing import List

WEBDIP_ID_ENV_VAR_NAME = "WEBDIP_GAME_ID"

MAIN_PHASE_LENGTH = utilities.get_env_var_checked(
    "MAIN_PHASE_LENGTH", "an unknown number of days"
)

AUXILIARY_PHASE_LENGTH = utilities.get_env_var_checked(
    "AUXILIARY_PHASE_LENGTH", "an unknown number of hours"
)

GAME_PHASE_DESCRIPTIONS = {
    "diplomacy": f"""This is a normal turn devoted to diplomacy, intrigue, and manoeuvre. In order to complete your turn you have to assign orders to all of your units, then click 'ready'; but you should expect to spend a good deal of time negotiating with enemies and friends about how to proceed. We have agreed to apply orders in this phase within {MAIN_PHASE_LENGTH}; the game will proceed automatically after that time has elapsed. IMPORTANT NOTE: provinces will only change hands if they are occupied *at the end of the year* by an invading power; if I move into an enemy province in the spring, then move out again in the autumn leaving it unoccupied, that province will not change hands.
""",
    "retreats": f"""This is the 'retreats' phase, one of the two auxiliary phases which occur at the end of each year. Only those powers who have been defeated and forced to retreat from some province have any orders to give; everyone else is waiting. We have agreed that these auxiliary phases should be completed within {AUXILIARY_PHASE_LENGTH}.
""",
    "builds": f"""This is the 'builds' phase, one of the two auxiliary phases which occur at the end of each year. Only those powers who have gained or lost supply centers in the course of the last year will have any orders to give; those who have gained supply centres will be able to build new armies in their core provinces; those who have lost supply centres will have to destroy armies. Everyone else is waiting. We have agreed that these auxiliary phases should be completed within {AUXILIARY_PHASE_LENGTH}.
""",
}


def announce_overall_game_state(state: DipGame, verbose: bool = False) -> str:
    """Consumes a DipGame and produces a string summarising the game
state. If verbose is set to True, interpolates a string describing the
purpose of the game state.

    """

    date_announcement = f"It is the {state['season']} of {state['year']}.\n"

    phase = state["phase"]

    if verbose:
        phase_announcement = phase_get_verbose_description(phase)
    else:
        phase_announcement = f"Phase: {phase}.\n"

    waiting_for = dipgame_get_uncommitted_players(state)

    awaiting_announcement = f"""We are awaiting the orders of:
{format_the_tardy_list(waiting_for)}
"""
    return date_announcement + phase_announcement + awaiting_announcement


def phase_get_verbose_description(phase: Phase) -> str:
    """Consumes a Phase and produces its corresponding verbose
description.

    """

    return GAME_PHASE_DESCRIPTIONS[phase]


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
