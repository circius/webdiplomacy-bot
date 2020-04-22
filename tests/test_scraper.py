import dipbot.scraper as scraper
from bs4 import BeautifulSoup
import testdata


# def test_can_get_DipGame_111111():
#     response = scraper.get_webdiplomacy_game_response_checked(111111)
#     assert response.status_code == 200
#     assert "Power From the Barrel of a Gun" in response.text
#     soup = scraper.get_soup_of_requests_html(response.text)
#     dipgame = scraper.soup_get_DipGame(soup)
#     assert len(dipgame["players"]) == 7
#     assert dipgame["name"] == "Power From the Barrel of a Gun"


def test_can_get_players_from_html():
    soup = scraper.get_soup_of_requests_html(testdata.pop_the_bee_html)
    assert type(soup) == BeautifulSoup
    players = scraper.soup_get_players(soup)
    assert len(players) == 7
    assert players == testdata.pop_the_bee_players


def test_can_get_DipGame_state_from_html():
    soup = scraper.get_soup_of_requests_html(testdata.pop_the_bee_html)
    DipGame = scraper.soup_get_DipGame(soup)
    assert DipGame == testdata.pop_the_bee_DipGame
