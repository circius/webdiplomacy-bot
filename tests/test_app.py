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
    assert "3.0" in announcement
    assert "04/04/20" in announcement
    assert "22:51:45" in announcement

    announcement_retreats = app.announce_overall_game_state(
        testdata.pop_the_bee_retreats_DipGame
    )
    assert type(announcement) == str
    assert "1905" in announcement_retreats
    assert "Autumn" in announcement_retreats
    assert "retreats" in announcement_retreats
    assert "161.6" in announcement_retreats
    assert "09/13/2020" in announcement_retreats
    assert "12:26:39" in announcement_retreats

    announcement_builds = app.announce_overall_game_state(
        testdata.pop_the_bee_builds_DipGame
    )
    assert type(announcement) == str
    assert "1905" in announcement_builds
    assert "Autumn" in announcement_builds
    assert "builds" in announcement_builds
    assert "0.1" in announcement_builds
    assert "09/13/2020" in announcement_builds
    assert "15:13:20" in announcement_builds

    announcement_finished = app.announce_overall_game_state(
        testdata.pop_the_bee_finished_DipGame
    )
    assert type(announcement) == str
    assert "1910" in announcement_finished
    assert "Autumn" in announcement_finished
    assert "finished" in announcement_finished
    assert "None" not in announcement_finished


def test_can_get_an_accurate_list_of_uncommitted_players():
    players = app.dipgame_get_uncommitted_players(testdata.pop_the_bee_DipGame)
    assert type(players) == list
    assert len(players) == 1
    assert players[0]["name"] == "MichiganMan"


def test_verbose_descriptions_are_longer():
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


def test_gets_time_left_as_days():
    pop_the_bee_timeleft_days = app.dipgame_get_time_left_as_days(
        testdata.pop_the_bee_DipGame
    )
    assert pop_the_bee_timeleft_days == 3.0


def test_gets_time_left_is_none_when_game_is_finished():
    pop_the_bee_timeleft_days = app.dipgame_get_time_left_as_days(
        testdata.pop_the_bee_finished_DipGame
    )
    assert pop_the_bee_timeleft_days == None


def test_gets_last_moment_correctly():
    pop_the_bee_last_moment = app.dipgame_get_last_moment(testdata.pop_the_bee_DipGame)
    assert "22:51:45" in pop_the_bee_last_moment
    assert "04/04/2020" in pop_the_bee_last_moment


def tests_gets_last_moment_when_game_is_finished():
    pop_the_bee_last_moment = app.dipgame_get_last_moment(
        testdata.pop_the_bee_finished_DipGame
    )
    assert pop_the_bee_last_moment == None
