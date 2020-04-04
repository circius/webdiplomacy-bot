import discord
import os
from dipbot import app, scraper


def main():

    api_token = app.get_env_var_checked("DISCORD_API_KEY")
    try:
        assert api_token != False
    except:
        exit(1)
    game_id = app.get_env_var_checked(app.WEBDIP_ID_ENV_VAR_NAME)
    try:
        assert game_id != False
    except:
        exit(1)
    dipgame = scraper.get_dipgame_checked(game_id)
    try:
        assert dipgame != False
    except:
        print(
            "Could not get status of game with id {game_id}. Are you sure it's valid? Exiting..."
        ).format(client)
        exit(1)

    client = discord.Client()

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == ("$status"):
            status_message = app.announce_overall_game_state(dipgame)
            await message.channel.send(status_message)

        if message.content == ("$status!"):

            urgent_message = f"{message.author.name} asked me to tell @everyone that:"
            status_message = app.announce_overall_game_state(dipgame)
            await message.channel.send(urgent_message + "\n" + status_message)

    client.run(api_token)


if __name__ == "__main__":
    main()
