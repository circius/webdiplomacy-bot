# -*- coding: utf-8 -*-
"""encapsulates functions which generate strings reporting the state
of DipGames.

"""
from dipbot.data_definitions import DipGame, Player, Phase
from dipbot import utilities
from typing import List, Union
import datetime
import pytz

WEBDIP_ID_ENV_VAR_NAME = "WEBDIP_GAME_ID"

AUXILIARY_PHASE_LENGTH = utilities.get_env_var_checked("AUXILIARY_PHASE_LENGTH", "")

GAME_PHASE_DESCRIPTIONS = {
    "diplomacy": f"""This is a normal phase of diplomacy and manoeuvre.""",
    "retreats": f"""Only those powers who have been defeated and forced to retreat from some province have any orders to give; everyone else is waiting.""",
    "builds": f"""In this phase:
  - those who have gained supply centres will be able to build new armies in their core provinces;
  - those who have lost supply centres will have to destroy armies.
Everyone else is waiting.""",
}


def get_game_id():
    return utilities.get_env_var_or_exit(WEBDIP_ID_ENV_VAR_NAME)


def announce_overall_game_state(state: DipGame, verbose: bool = False) -> str:
    """Consumes a DipGame and produces a string summarising the game
state. If verbose is set to True, interpolates a string describing the
purpose of the game state.

    """
    season, year, phase = (state["season"], state["year"], state["phase"])

    date_announcement = f"It is the **{phase} phase** of the {season} of {year}."

    waiting_for = dipgame_get_uncommitted_players(state)

    awaiting_announcement = f"""We are awaiting the orders of:
{format_the_tardy_list(waiting_for)}
"""

    announcement = [date_announcement, awaiting_announcement]

    if phase != "finished":
        time_left = dipgame_get_time_left_as_days(state)

        last_moment = dipgame_get_last_moment(state)

        time_left_announcement = f"""There are **{time_left}** days until the deadline, which is at {last_moment} UTC.
"""
        announcement.append(time_left_announcement)

    if verbose:
        phase_long_description = f"{phase_get_verbose_description(phase)}"
        announcement.append(phase_long_description)

    return "\n".join(announcement)


def dipgame_get_last_moment(state: DipGame) -> Union[str, None]:
    """consumes a DipGame and produces a string representing the time and
date of the end of the turn.

    """
    posix_or_none = state["deadline"]
    if posix_or_none == None:
        return None
    else:
        moment = datetime.datetime.fromtimestamp(
            state["deadline"], pytz.timezone("UTC")
        )
        return moment.strftime("%m/%d/%Y, %H:%M:%S")


def dipgame_get_time_left_as_days(state: DipGame) -> Union[float, None]:
    """Consumes a DipGame and produces an integer representing the time
before the deadline denominated by days, rounded to one decimal place,
or None if either `deadline` or `started` are None.

    """
    [deadline, started] = [state["deadline"], state["started"]]
    if deadline == None or started == None:
        return None
    else:
        time_left_as_seconds = deadline - started
        time_left_as_days = time_left_as_seconds / 86400
        return round(time_left_as_days, 1)


def phase_get_verbose_description(phase: Phase) -> str:
    """Consumes a Phase and produces its corresponding verbose
description.

    """

    description = GAME_PHASE_DESCRIPTIONS[phase]
    return description


def format_the_tardy_list(lop: List[Player]) -> str:
    """ formats the list of players we're waiting for.
"""
    return "\n".join([format_tardy_player(player) for player in lop])


def format_tardy_player(player: Player) -> str:
    """ formats a notice that a player's tardy.
"""
    return f"  - {player['name']}, whose orders are {player['turn status'].lower()}"


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
