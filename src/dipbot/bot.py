import discord
import os
from dipbot import app, scraper

api_token = os.getenv("DISCORD_API_KEY")
webdip_id = int(os.getenv("WEBDIP_GAME_ID"))

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ("$status"):
        dipgame = scraper.get_dipgame(webdip_id)
        status_message = app.announce_overall_game_state(dipgame)
        await message.channel.send(status_message)

    if message.content == ("$status!"):
        dipgame = scraper.get_dipgame(webdip_id)
        urgent_message = f"{message.author.name} asked me to tell @everyone that:"
        status_message = app.announce_overall_game_state(dipgame)
        await message.channel.send(urgent_message + "\n" + status_message)


client.run(api_token)
