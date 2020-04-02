# -*- coding: utf-8 -*-
"""encapsulates functions which get structured data from webdiplomacy.

"""
import requests
from dipbot.data_definitions import DipGame, Player, Turn
from bs4 import BeautifulSoup, Tag, ResultSet
from typing import List

WEBDIP_GAMES_ROOT_URL = "https://webdiplomacy.net/board.php?gameID="


def get_webdiplomacy_game_response(id: int) -> requests.models.Response:
    """ gets the raw html of a public webdiplomacy board
"""
    return requests.get(WEBDIP_GAMES_ROOT_URL + str(id))


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
        "retreats?": soup_retreatsP(soup),
        "players": soup_get_players(soup),
    }


def soup_get_players(soup: BeautifulSoup) -> List[Player]:
    """parses a soup representing a webdiplomacy game page, and
produces a list of Players, representing each player's current state.

    """
    player_table = soup.find("div", class_="membersFullTable")
    player_rows = table_get_player_rows(player_table)
    # print("player rows is a {}".format(type(player_rows)))
    # print("its content is {}".format(player_rows))
    # print("its length is {}".format(len(player_rows)))
    # print("its first element is {}".format(player_rows[0]))
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
    # print(player_table)
    # print(player_table.find_all("tr", class_="member"))
    return player_table.find_all("tr", class_="member")


def soup_retreatsP(soup: BeautifulSoup) -> bool:
    """parses a soup representing a webdiplomacy game page, and
produces a boolean indicating whether or not the game is in a retreats
phase.

    """
    return False


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
