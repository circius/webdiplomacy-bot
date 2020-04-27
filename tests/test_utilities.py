from dipbot import utilities
import pytest


@pytest.mark.parametrize("var_name", "expected_value")
def test_get_env_var_checked_can_get_arbitrary_env_var(monkeypatch):
    monkeypatch.setenv("DISCORD_API_KEY", "nonsense")
    key = utilities.get_env_var_checked("DISCORD_API_KEY")
    assert key == "nonsense"

    monkeypatch.setenv("DISCORD_API_KEY", "bleh")
    key = utilities.get_env_var_checked("DISCORD_API_KEY")
    assert key == "bleh"


def test_get_env_var_checked_can_get_arbitrary_env_var(monkeypatch):
    monkeypatch.setenv("DISCORD_API_KEY", "nonsense")
    key = utilities.get_env_var_checked("DISCORD_API_KEY")
    assert key == "nonsense"


def test_gets_env_variable_or_exits(monkeypatch):
    monkeypatch.setenv("DISCORD_API_KEY", "nonsense")
    value = utilities.get_env_var_or_exit("DISCORD_API_KEY")
    assert value == "nonsense"

    nokey = "NO_SUCH_KEY_WILL_EVER_BE_SET"
    monkeypatch.delenv(nokey, raising=False)

    # code for testing exits from https://medium.com/python-pandemonium/testing-sys-exit-with-pytest-10c6e5f7726f
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        utilities.get_env_var_or_exit(nokey)
    assert pytest_wrapped_e.type == SystemExit
