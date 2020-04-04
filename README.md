[![Build Status](https://travis-ci.org/circius/webdiplomacy-bot.svg?branch=master)](https://travis-ci.org/circius/webdiplomacy-bot)

## summary

This is a discord bot which scrapes the current status of games at
webdiplomacy and announces that information on discord.

It also incorporates a very rudimentary cli tool which does the same
thing on the host.

## functionality

For the moment it only produces one kind of announcement, in the
following format:

"It is the [season] of [year].
We are awaiting the order of:
[list of non-ready players with their order statuses]"

In a discord channel it will do this in response to the message "$status".

run as a cli app, it will simply output a similar message and terminate.

## configuration

dipbot depends on two environment variables which must be correctly
set for it to function. 

In order to know which game to parse, the environment variable
WEBDIP_GAME_ID must be set to the corresponding webdiplomacy.com game
id. This is the number at the end of the webdiplomacy url for the
game; for instance, in the following URL, the id is 111111

https://webdiplomacy.net/board.php?gameID=111111

In addition, to host the discord bot yourself it's necessary to create
a bot account as described
[here](https://discordpy.readthedocs.io/en/latest/discord.html), and
to set the environment variable DISCORD_API_KEY to the value of the
bot's token.

## installation

the most recent release is available from pip:

``` shell
$ pip install --user dipbot
```

after which, so long as your PATH is properly configured, you should be able to run dipbot directly from the shell:

``` shell
$ dipbot
```

## usage

there are two subcommands available:

``` shell
$ dipbot report
```

which parses the status of the game and reports it to the shell before quitting, and

``` shell
$ dipbot daemon
```

which attempts to initialize a discord bot corresponding to the token stored in DISCORD_API_KEY, and which will respond with a report when addressed on discord with the messages "$status" and "!status".
