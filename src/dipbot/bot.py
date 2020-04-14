import discord
import os
from dipbot import app, scraper, utilities
from dipbot.data_definitions import DipGame


def client_get_dipgame_checked(client: discord.Client, game_id: int) -> DipGame:
    """consumes a discord.py Client and a webdiplomacy game_id and
produces the corresponding DipGame.

    """
    dipgame = scraper.get_dipgame_checked(game_id)
    try:
        assert dipgame != False
    except:
        print(
            "Could not get status of game with id {game_id}. Are you sure it's valid? Exiting..."
        ).format(client)
        exit(1)
    return dipgame


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


def main():

    api_token = utilities.get_env_var_checked("DISCORD_API_KEY")
    try:
        assert api_token != False
    except:
        exit(1)
    game_id = utilities.get_env_var_checked(app.WEBDIP_ID_ENV_VAR_NAME)
    try:
        assert game_id != False
    except:
        exit(1)
    client = discord.Client()

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content[0] != "$":
            return

        dipgame = client_get_dipgame_checked(client, game_id)

        invoking_user = message.author.name

        if message.content == ("$status"):
            status_message = app.announce_overall_game_state(dipgame)

        elif message.content == ("$status!"):
            status_message = create_urgent_message(
                app.announce_overall_game_state(dipgame), invoking_user
            )

        elif message.content == ("$status?"):
            status_message = app.announce_overall_game_state(dipgame, verbose=True)

        elif (message.content == ("$status?!")) or (message.content == ("status!?")):
            status_message = create_urgent_message(
                app.announce_overall_game_state(dipgame, verbose=True), invoking_user
            )

        if status_message:
            await message.channel.send(status_message)

    client.run(api_token)


if __name__ == "__main__":
    main()
