import discord
import os
from dipbot import app, scraper, utilities
from dipbot.data_definitions import DipGame


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


def message_is_help_commandP(message: discord.message, client: discord.Client) -> bool:
    """consumes a dusord.py message and a discord Client and produces true
if it should be interpreted as a request for help by the client, false
otherwise.

    """
    return mentions_includes_name(message.mentions, client.user)


def mentions_includes_name(mentions: list, name: str) -> bool:
    """consumes a list of mentions from a discord.py message and produces
true if one of the users mentioned has the supplied NAME, false
otherwise.

    """
    return any(map(lambda x: x.name == name, mentions))


def get_env_var_or_exit(env_var: str) -> str:
    """consumes a string corresponding to an environment variable. if the
environment variable is set, produces it as a string. if it's not,
sends the signal exit(1).

    """
    value = utilities.get_env_var_checked(env_var)
    try:
        assert value != False
    except:
        exit(1)
    return value


def main():

    api_token = get_env_var_or_exit("DISCORD_API_KEY")

    game_id = get_env_var_or_exit(app.WEBDIP_ID_ENV_VAR_NAME)

    client = discord.Client()

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message_is_help_commandP(message, client):
            await message.channel.send(
                """I understand the following instructions:
 - `$status`
 - `$status!`
 - `$status?`
 - `$status!?`"""
            )

        if message.content[0] != "$":
            return

        dipgame = scraper.get_dipgame_checked(game_id)

        if dipgame == False:
            await message.channel.send(f"Could not find game at {game_id}.")
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

    client.run(api_token)


if __name__ == "__main__":
    main()
