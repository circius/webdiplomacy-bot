import discord
from discord.ext import commands


def create_urgent_message(normal_message: str, invoking_user: str = "") -> str:
    """consumes a string representing a message to be posted to a discord
channel and produces an urgent version by prepending a string
mentioning @everyone. optionally consumes a string representing the
name of the user that invoked this urgent message; if invoking_user is
set, the urgent message will blame that user.

    """
    if invoking_user:
        urgent_prefix = f"{invoking_user} asked me to tell @everyone that:"
    else:
        urgent_prefix = f"@everyone should know that"

    return "\n".join([urgent_prefix, normal_message])


def message_is_pleadingP(message: discord.Message) -> bool:
    """consumes a discord.py message and returns 'true' if it's a
pleading message, false otherwise.

    """
    pleading_lexemes = ["help", "please", "?", "how"]
    return any(map(lambda x: x in message.content.lower(), pleading_lexemes))


def message_is_pleading_with_clientuserP(
    message: discord.Message, clientuser: discord.ClientUser
) -> bool:
    """consumes a discord message and a discord ClientUser and produces
true if the message is both "pleading" and mentions the user.

    """
    return clientuser.mentioned_in(message) and message_is_pleadingP(message)
