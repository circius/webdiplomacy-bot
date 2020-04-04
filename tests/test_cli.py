from dipbot import cli, app
import click
from click.testing import CliRunner

GAME_ID_ENVVAR = app.WEBDIP_ID_ENV_VAR_NAME
DISCORD_API_KEY_ENVVAR = "DISCORD_API_KEY"


def test_running_report_with_unset_game_id_exits_gracefully(monkeypatch):
    monkeypatch.delenv(GAME_ID_ENVVAR, raising=False)
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["report"])
    assert result.exit_code == 1
    assert "unset! terminating..." in result.output


def test_running_report_with_invalid_game_id_exits_gracefully(monkeypatch):
    monkeypatch.setenv(GAME_ID_ENVVAR, str(1))
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["report"])
    assert result.exit_code == 1
    assert "Game with id" in result.output
    assert "not found" in result.output


# TODO stripping this out. I should implement some kind of token
# validation, but that seems not to be straightforward, so this test
# has to wait (if I'm not just to hit the discord API with floods of
# failed logins)

# def test_running_daemon_with_invalid_discord_token_exits_gracefully(monkeypatch):
#     monkeypatch.setenv(DISCORD_API_KEY_ENVVAR, str(1))
#     runner = CliRunner()
#     result = runner.invoke(cli.cli, ["daemon"])
#     assert result.exit_code == 1
#     assert "Improper token has been passed." in result.output


def test_running_daemon_with_unset_discord_token_exits_gracefully(monkeypatch):
    monkeypatch.delenv(DISCORD_API_KEY_ENVVAR, raising=False)
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["daemon"])
    assert result.exit_code == 1
    assert f"{DISCORD_API_KEY_ENVVAR} unset!" in result.output
