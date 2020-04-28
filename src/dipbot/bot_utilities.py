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


def message_mentions_botP(message: discord.message, BOT: commands.bot) -> bool:
    """consumes a discord.py message and a discord BOT and produces true if
it mentions the bot, false otherwise.

    """
    return mentions_includes_user(message.mentions, BOT.user)


def mentions_includes_user(mentions: list, user: discord.ClientUser) -> bool:
    """consumes a list of mentions from a discord.py message and produces
true if one of the users mentioned has the supplied ClientUser, false
otherwise.

    """
    return any(map(lambda x: x.name == user.name, mentions))

def message_is_pleadingP(message: discord.Message) -> bool:
    """consumes a discord.py message and returns 'true' if it's a
pleading message, false otherwise.

    """
    pleading_lexemes = ["help", "please", "?", "how"]
    return any(map(lambda x: x in message.content, pleading_lexemes))
