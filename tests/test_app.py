from dipbot import app
import testdata


def test_can_accurately_report_overall_game_state():
    """ loosely test the report of overall game state
"""
    announcement = app.announce_overall_game_state(testdata.pop_the_bee_DipGame)
    assert type(announcement) == str
    assert "1904" in announcement
    assert "Spring" in announcement
    assert "diplomacy" in announcement

    announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame
    )
    assert type(announcement) == str
    assert "1905" in announcement_retreats
    assert "Autumn" in announcement_retreats
    assert "retreats" in announcement_retreats

    announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame
    )
    assert type(announcement) == str
    assert "1905" in announcement_builds
    assert "Autumn" in announcement_builds
    assert "builds" in announcement_builds


def test_can_get_an_accurate_list_of_uncommitted_players():
    players = app.dipgame_get_uncommitted_players(testdata.pop_the_bee_DipGame)
    assert type(players) == list
    assert len(players) == 1
    assert players[0]["name"] == "MichiganMan"


def test_produces_verbose_descriptions_on_request():
    announcement = app.announce_overall_game_state(testdata.pop_the_bee_DipGame)
    verbose_announcement = app.announce_overall_game_state(
        testdata.pop_the_bee_DipGame, True
    )
    assert len(verbose_announcement.split()) > len(announcement)

    announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame
    )
    verbose_announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame, True
    )

    assert len(verbose_announcement.split()) > len(announcement_retreats)

    announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame
    )
    verbose_announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame, True
    )
    assert len(verbose_announcement.split()) > len(announcement_builds)
