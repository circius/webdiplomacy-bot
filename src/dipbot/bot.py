import discord
from discord.ext import commands
import os
from dipbot import app, scraper, utilities
from dipbot.data_definitions import DipGame

BOT = discord.Client()


@BOT.event
async def on_ready():
    print("We have logged in as {0.user}".format(BOT))


@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return

    if message_is_help_commandP(message, BOT):
        await message.channel.send(
            """I understand the following instructions:
            - `$status`
            - `$status!`
            - `$status?`
            - `$status!?`"""
        )

    if message.content[0] != "$":
        return

    dipgame = scraper.get_dipgame_checked(GAME_ID)

    if dipgame == False:
        await message.channel.send(f"Could not find game at {GAME_ID}.")
        return

    invoking_user = message.author.name

    request = message.content

    print(f"request: {request}")

    status_message = False

    if request == "$status":
        status_message = app.announce_overall_game_state(dipgame)

    if request == "$status!":
        status_message = create_urgent_message(
            app.announce_overall_game_state(dipgame), invoking_user
        )

    if request == "$status?":
        status_message = app.announce_overall_game_state(dipgame, verbose=True)

    if request == "$status!?" or request == "$status?!":
        status_message = create_urgent_message(
            app.announce_overall_game_state(dipgame, verbose=True), invoking_user
        )

    if status_message:
        print("served status")
        await message.channel.send(status_message)
    else:
        print(f"did not understand message `{request}`")


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


# class DipBot(commands.Bot):
#     def __init__(self):
#         command_prefix = "$"
#         help_command = None
#         help_message = """I understand the following instructions:
#  - `$status`
#  - `$status!`
#  - `$status?`
#  - `$status!?`
#  - `$?`"""
#         super().__init__(command_prefix, help_command, help_message)


def main():
    API_TOKEN = utilities.get_env_var_or_exit("DISCORD_API_KEY")
    GAME_ID = utilities.get_env_var_or_exit(app.WEBDIP_ID_ENV_VAR_NAME)
    BOT.run(API_TOKEN)
