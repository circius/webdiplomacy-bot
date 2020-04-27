import discord
from discord.ext import commands
import os
from dipbot import app, scraper, utilities
from dipbot.data_definitions import DipGame
from dipbot.cogs import status

class DipBot(commands.Bot):
    def __init__(self):
        command_prefix = "$"
        help_command = None
        help_message = """I understand the following instructions:
 - `$status`
 - `$status!`
 - `$status?`
 - `$status!?`
 - `$?`"""
        super().__init__(command_prefix, help_command, help_message)

BOT = DipBot()

@BOT.event
async def on_ready():
    print("We have logged in as {0.user}".format(BOT))

def main():
    API_TOKEN = utilities.get_env_var_or_exit("DISCORD_API_KEY")
    BOT.add_cog(status.Status(BOT))
    BOT.run(API_TOKEN)
