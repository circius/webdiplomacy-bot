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
    assert len(verbose_announcement.split()) > len(announcement.split())

    announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame
    )
    verbose_announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame, True
    )

    assert len(verbose_announcement.split()) > len(announcement_retreats.split())

    announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame
    )
    verbose_announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame, True
    )
    assert len(verbose_announcement.split()) > len(announcement_builds.split())


def test_verbose_report_will_show_timing_info_when_env_is_set():
    app.GAME_PHASE_DESCRIPTIONS["diplomacy"][1] = "7 days"
    verbose_announcement = app.announce_overall_game_state(
        testdata.pop_the_bee_DipGame, True
    )
    assert "7 days" in verbose_announcement

    verbose_announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame, True
    )
    assert "7 days" not in verbose_announcement_retreats

    app.GAME_PHASE_DESCRIPTIONS["retreats"][1] = "48 hours"
    verbose_announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame, True
    )
    assert "48 hours" in verbose_announcement_retreats
