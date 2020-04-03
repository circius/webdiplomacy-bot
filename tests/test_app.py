from dipbot import app
import testdata


def test_can_accurately_report_overall_game_state():
    """ loosely test the report of overall game state
"""
    announcement = app.announce_overall_game_state(testdata.pop_the_bee_DipGame)
    assert type(announcement) == str
    assert "1904" in announcement
    assert "Spring" in announcement


def test_can_get_an_accurate_list_of_uncommitted_players():
    players = app.dipgame_get_uncommitted_players(testdata.pop_the_bee_DipGame)
    assert type(players) == list
    assert len(players) == 1
    assert players[0]["name"] == "MichiganMan"
