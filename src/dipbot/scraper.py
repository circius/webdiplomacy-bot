# -*- coding: utf-8 -*-
"""encapsulates functions which get DipGames from webdiplomacy.

"""
import requests
from dipbot.data_definitions import DipGame, Player, Turn, Phase
from bs4 import BeautifulSoup, Tag, ResultSet
from typing import List, Union

WEBDIP_GAMES_ROOT_URL = "https://webdiplomacy.net/board.php?gameID="


def get_dipgame_checked(id: int) -> Union[DipGame, bool]:
    """consumes an id and produces the corresponding dipgame, or False if
no corresponding dipgame is found.

    """
    response = get_webdiplomacy_game_response_checked(id)
    try:
        assert response != False
    except:
        return False
    soup = get_soup_of_requests_html(response.text)
    return soup_get_DipGame(soup)


def response_webdip_game_exists(response: requests.models.Response) -> bool:
    """consumes a response from webdiplomacy.com and produces true if the
response contains a game board, false otherwise.

    """
    return "Game not found" not in response.text


def get_webdiplomacy_game_response_checked(
    id: int,
) -> Union[requests.models.Response, bool]:
    """ gets the raw html of a public webdiplomacy board
"""
    response = requests.get(WEBDIP_GAMES_ROOT_URL + str(id))
    try:
        assert response_webdip_game_exists(response)
    except:
        print(f"Game with id {id} not found")
        return False
    return response


def get_soup_of_requests_html(s: str) -> BeautifulSoup:
    """ gets soup from the contents of a response
"""
    return BeautifulSoup(s, "lxml")


def soup_get_DipGame(soup: BeautifulSoup) -> DipGame:
    """parses a Soup representing a webdiplomacy game page, and
produces a DipGame representing the game state.

    """
    return {
        "name": soup_get_game_name(soup),
        "year": soup_get_game_year(soup),
        "season": soup_get_game_season(soup),
        "phase": soup_get_phase(soup),
        "players": soup_get_players(soup),
        "started": soup_get_started_epoch(soup),
        "deadline": soup_get_deadline_epoch(soup),
    }


def soup_get_deadline_epoch(soup: BeautifulSoup) -> Union[int, None]:
    """parses a soup representing a webdiplomacy game page, and produces
the epoch of the deadline, or None if the game is over.

    """
    timeremaining_span_or_none = soup.find("span", class_="timeremaining")
    if timeremaining_span_or_none == None:
        return None
    else:
        return int(timeremaining_span_or_none["unixtime"])


def soup_get_started_epoch(soup: BeautifulSoup) -> Union[int, None]:
    """parses a soup representing a webdiplomacy game page, and produces
the epoch of the beginning of the phase, or None if the game is over.

    """
    timeremaining_span_or_none = soup.find("span", class_="timeremaining")
    if timeremaining_span_or_none == None:
        return None
    else:
        return int(timeremaining_span_or_none["unixtimefrom"])


def soup_get_players(soup: BeautifulSoup) -> List[Player]:
    """parses a soup representing a webdiplomacy game page, and
produces a list of Players, representing each player's current state.

    """
    player_table = soup.find("div", class_="membersFullTable")
    player_rows = table_get_player_rows(player_table)
    return [row_get_player(row) for row in player_rows]


def row_get_player(player_row: Tag) -> Player:
    """Parses a BeautifulSoup Tag representing a row of the member table
and produces a Player representing the current state of the
corresponding player.

    """
    return {
        "name": player_row_get_name(player_row),
        "power": player_row_get_power(player_row),
        "turn status": player_row_get_status(player_row),
    }


def player_row_get_name(player_row: Tag) -> str:
    """Parses a BeautifulSoup Tag representing a row of the member table
and produces the name of the corresponding player.

    """
    tag = player_row.find("span", class_="memberName")
    raw_name = tag.a.text
    return raw_name.strip()


def player_row_get_power(player_row: Tag) -> str:
    """Parses a BeautifulSoup Tag representing a row of the member table
and produces the power of the corresponding player.

    """
    tag = player_row.find("span", class_="memberCountryName")
    raw_power = tag.text
    return raw_power.strip()


def player_row_get_status(player_row: Tag) -> Turn:
    """Parses a BeautifulSoup Tag representing a row of the member table
and produces the turn-status of the corresponding power.

    """
    tag = player_row.find("img")
    return tag.get("alt")


def table_get_player_rows(player_table: Tag) -> ResultSet:
    """Parses a BeautifulSoup Tag representing the member table and
produces a list of the tags representing each player for further
processing.

    """
    all_member_rows = player_table.find_all("tr", class_="member")
    rows_without_civil_disorder_notices = all_member_rows[:7]
    return rows_without_civil_disorder_notices


def soup_get_phase(soup: BeautifulSoup) -> Phase:
    """parses a soup representing a webdiplomacy game page, and produces a
Phase.

    """
    raw_gamephase = soup.find("span", class_="gamePhase").text
    return raw_gamephase.lower()


def soup_get_game_season(soup: BeautifulSoup) -> str:
    """parses a soup representing a webdiplomacy game page, and
produces a string representing the game's season.

    """
    gamedate = soup.find("span", class_="gameDate").text
    return gamedate.split(",")[0]


def soup_get_game_year(soup: BeautifulSoup) -> int:
    """parses a soup representing a webdiplomacy game page, and
produces a string representing the game's year.

    """
    gamedate = soup.find("span", class_="gameDate").text
    return int(gamedate.split(",")[1])


def soup_get_game_name(soup: BeautifulSoup) -> str:
    """parses a soup representing a webdiplomacy game page, and
produces a string representing the game's name.

    """
    return soup.find("span", class_="gameName").text
