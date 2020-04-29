from discord.ext import commands
from dipbot import scraper, app, bot_utilities


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_id = app.get_game_id()

    @commands.command()
    async def status(self, ctx):
        """instructs me to report on the status of my webdip game.

        """
        dipgame = scraper.get_dipgame_checked(self.game_id)
        status_message = app.announce_overall_game_state(dipgame)
        await ctx.message.channel.send(status_message)

    @commands.command(name="status!")
    async def status_shouted(self, ctx):
        """same as `$status`, but mentioning @everyone
"""
        dipgame = scraper.get_dipgame_checked(self.game_id)
        status_message = bot_utilities.create_urgent_message(
            app.announce_overall_game_state(dipgame), ctx.message.author.name
        )
        await ctx.message.channel.send(status_message)

    @commands.command(name="status?")
    async def status_verbose(self, ctx):
        """same as `$status`, but with additional information about the game
state. useful for beginners.

        """
        dipgame = scraper.get_dipgame_checked(self.game_id)
        status_message = app.announce_overall_game_state(dipgame, verbose=True)
        await ctx.message.channel.send(status_message)

    @commands.command(name="status?!", aliases=["status!?"])
    async def status_verbose_shouted(self, ctx):
        """same as `$status?`, but mentioning @everyone
"""
        dipgame = scraper.get_dipgame_checked(self.game_id)
        status_message = bot_utilities.create_urgent_message(
            app.announce_overall_game_state(dipgame, verbose=True),
            ctx.message.author.name,
        )
        await ctx.message.channel.send(status_message)
