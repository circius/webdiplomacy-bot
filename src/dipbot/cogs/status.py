from discord.ext import commands
from dipbot import scraper, app, bot_utilities

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_id = GAME_ID

    @commands.command()
    async def status(self, ctx):
        dipgame = scraper.get_dipgame_checked(self.game_id)
        status_message = app.announce_overall_game_state(dipgame)
        await ctx.message.channel.send(status_message)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if bot_utilities.message_is_help_commandP(message, self.bot):
            await message.channel.send(
                """I understand the following instructions:
                - `$status`
                - `$status!`
                - `$status?`
                - `$status!?`"""
            )

        if message.content[0] != "$":
            return

        dipgame = scraper.get_dipgame_checked(app.GAME_ID)

        if dipgame == False:
            await message.channel.send(f"Could not find game at {app.GAME_ID}.")
            return

        invoking_user = message.author.name

        request = message.content

        print(f"request: {request}")

        status_message = False

        if request == "$status":
            pass

        if request == "$status!":
            status_message = bot_utilities.create_urgent_message(
                app.announce_overall_game_state(dipgame), invoking_user
            )

        if request == "$status?":
            status_message = app.announce_overall_game_state(dipgame, verbose=True)

        if request == "$status!?" or request == "$status?!":
            status_message = bot_utilities.create_urgent_message(
                app.announce_overall_game_state(dipgame, verbose=True), invoking_user
            )

        if status_message:
            print("served status")
            await message.channel.send(status_message)
        else:
            print(f"did not understand message `{request}`")
