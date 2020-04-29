import discord
from discord.ext import commands
from dipbot.cogs import status
import os
from dipbot import app, scraper, utilities, bot_utilities
from dipbot.data_definitions import DipGame

COMMAND_PREFIX = "$"


class DipBot(commands.Bot):
    def __init__(self):
        super().__init__(COMMAND_PREFIX)


BOT = DipBot()


@BOT.event
async def on_ready():
    print("We have logged in as {0.user}".format(BOT))


async def on_message(message):
    if bot_utilities.message_is_pleading_with_clientuserP(message, BOT.user):
        await message.channel.send(
            f"""I would love to help but I only understand a few messages, always prefixed by `{COMMAND_PREFIX}`. If you ask for `{COMMAND_PREFIX}help` I'll tell you about them."""
        )


def main():
    API_TOKEN = utilities.get_env_var_or_exit("DISCORD_API_KEY")
    BOT.add_cog(status.Status(BOT))
    BOT.add_listener(on_message)
    BOT.run(API_TOKEN)
