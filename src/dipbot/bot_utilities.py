import discord

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


def message_is_help_commandP(message: discord.message, BOT: discord.Client) -> bool:
    """consumes a dusord.py message and a discord BOT and produces true
if it should be interpreted as a request for help by the BOT, false
otherwise.

    """
    return mentions_includes_name(message.mentions, BOT.user)


def mentions_includes_name(mentions: list, name: str) -> bool:
    """consumes a list of mentions from a discord.py message and produces
true if one of the users mentioned has the supplied NAME, false
otherwise.

    """
    return any(map(lambda x: x.name == name, mentions))
