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
