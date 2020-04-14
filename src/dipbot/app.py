# -*- coding: utf-8 -*-
"""encapsulates functions which generate strings reporting the state
of DipGames.

"""
from dipbot.data_definitions import DipGame, Player, Phase
from dipbot import utilities
from typing import List

WEBDIP_ID_ENV_VAR_NAME = "WEBDIP_GAME_ID"

MAIN_PHASE_LENGTH = utilities.get_env_var_checked( 
    "MAIN_PHASE_LENGTH", ""
)

AUXILIARY_PHASE_LENGTH = utilities.get_env_var_checked( 
    "AUXILIARY_PHASE_LENGTH", ""
)

GAME_PHASE_DESCRIPTIONS = {
    "diplomacy": [f"""This is a normal phase of diplomacy and manoeuvre.""", MAIN_PHASE_LENGTH],
    
    "retreats": [f"""Only those powers who have been defeated and forced to retreat from some province have any orders to give; everyone else is waiting.""", AUXILIARY_PHASE_LENGTH],
    
    "builds": [f"""In this phase:
  - those who have gained supply centres will be able to build new armies in their core provinces;
  - those who have lost supply centres will have to destroy armies.
Everyone else is waiting.""", AUXILIARY_PHASE_LENGTH],
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
    description = GAME_PHASE_DESCRIPTIONS[phase][0]
    allotted_time = GAME_PHASE_DESCRIPTIONS[phase][1]

    if allotted_time != "":
        time_description = f"We've agreed to submit turns within {allotted_time}."
        return " ".join([description, time_description])

    return description


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
