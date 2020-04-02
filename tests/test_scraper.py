import dipbot.scraper as scraper
from bs4 import BeautifulSoup
import testdata


def test_can_get_webdiplomacy_game_111111():
    response = scraper.get_webdiplomacy_game_response(111111)
    assert response.status_code == 200
    assert "Power From the Barrel of a Gun" in response.text


def test_can_get_players_from_html():
    soup = scraper.get_soup_of_requests_html(testdata.pop_the_bee_html)
    assert type(soup) == BeautifulSoup
    players = scraper.soup_get_players(soup)
    assert len(players) == 7
    assert players == testdata.pop_the_bee_players
