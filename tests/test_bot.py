from dipbot import bot, scraper
import testdata
import pytest


def test_can_create_urgent_message():
    message = "nothing important"
    anonymous_urgent_message = bot.create_urgent_message(message)
    assert "@everyone" in anonymous_urgent_message
    assert len(anonymous_urgent_message.split("\n")) == 2
    nonymous_urgent_message = bot.create_urgent_message(message, "Jack")
    assert "@everyone" in nonymous_urgent_message
    assert len(nonymous_urgent_message.split("\n")) == 2
    assert "Jack" in nonymous_urgent_message


class MockClient:
    def __init__(self, user):
        self.user = user


class MockMessage:
    def __init__(self, content, mentions):
        self.content = content
        self.mentions = mentions


class MockMention:
    def __init__(self, name):
        self.name = name


@pytest.mark.parametrize("client", [MockClient("@webdiplomacy"), MockClient("@dipbot")])
def test_message_is_help_commandP(client):
    mentions = [MockMention(client.user)]
    mentions_deformed_client = [MockMention(client.user[1:])]
    valid_help_messages_for_client = [
        MockMessage(f"{client.user}", mentions),
        MockMessage(f"{client.user} how do you work?", mentions),
        MockMessage("{client.user} how do you work?", mentions),
    ]
    invalid_help_messages_for_client = [
        MockMessage("how do you work {client.user[1:]}?", mentions_deformed_client),
        MockMessage("how do you work anotonin?", []),
    ]

    for message in valid_help_messages_for_client:
        assert bot.message_is_help_commandP(message, client) == True

    for message in invalid_help_messages_for_client:
        assert bot.message_is_help_commandP(message, client) == False


def test_gets_env_variable_or_exits(monkeypatch):
    monkeypatch.setenv("DISCORD_API_KEY", "nonsense")
    value = bot.get_env_var_or_exit("DISCORD_API_KEY")
    assert value == "nonsense"

    nokey = "NO_SUCH_KEY_WILL_EVER_BE_SET"
    monkeypatch.delenv(nokey, raising=False)
    
    # code for testing exits from https://medium.com/python-pandemonium/testing-sys-exit-with-pytest-10c6e5f7726f
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        bot.get_env_var_or_exit(nokey)
    assert pytest_wrapped_e.type == SystemExit
