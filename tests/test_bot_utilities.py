from dipbot import bot_utilities
import discord
import testdata
import pytest


def test_can_create_urgent_message():
    message = "nothing important"
    anonymous_urgent_message = bot_utilities.create_urgent_message(message)
    assert "@everyone" in anonymous_urgent_message
    assert len(anonymous_urgent_message.split("\n")) == 2
    nonymous_urgent_message = bot_utilities.create_urgent_message(message, "Jack")
    assert "@everyone" in nonymous_urgent_message
    assert len(nonymous_urgent_message.split("\n")) == 2
    assert "Jack" in nonymous_urgent_message


class MockMessage:
    def __init__(self, content):
        self.content = content


def test_message_is_pleadingP():
    pleading_message_1 = "Please help me with this."
    pleading_message_2 = "How do I lift myself out of this hole?"
    pleading_message_3 = "Can I tell you what to do?"
    pleading_message_4 = "how can you live with yourself"
    not_pleading = "you're a disgrace and I never want to speak with you again."
    for message in [
        pleading_message_1,
        pleading_message_2,
        pleading_message_3,
        pleading_message_4,
    ]:
        assert bot_utilities.message_is_pleadingP(MockMessage(message)) == True
    assert bot_utilities.message_is_pleadingP(MockMessage(not_pleading)) == False
