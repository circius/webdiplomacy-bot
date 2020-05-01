[![Build Status](https://travis-ci.org/circius/webdiplomacy-bot.svg?branch=master)](https://travis-ci.org/circius/webdiplomacy-bot)
[![Coverage Status](https://coveralls.io/repos/github/circius/webdiplomacy-bot/badge.svg?branch=master)](https://coveralls.io/github/circius/webdiplomacy-bot?branch=master)

## summary

This is a discord bot which scrapes the current status of a game at
webdiplomacy and announces that information on discord.

It also incorporates a very rudimentary cli tool which does the same
thing on the host.

*Note that at the moment dipbot can only handle a single game*,
although the CLI functionality can fairly straightforwardly be
adjusted to parse different games (there's guidance on this below.)

## daemon functionality

The daemon, which is run as `dipbot daemon`, spawns a discord bot
based on discord.py. It depends on a couple of environment variables
described below.

Here is the bot's help dialogue, which describes the commands it
supports:

``` shell
Status:
  status   instructs me to report on the status of my webdip game.
  status!  same as `$status`, but mentioning @everyone
  status?  same as `$status`, but with additional information about the game
  status?! same as `$status?`, but mentioning @everyone
​No Category:
  help     Shows this message

Type $help command for more info on a command.
You can also type $help category for more info on a category.
```

A `$status` request produces output in the
following format:

``` shell
"It is the [game-phase] of the [season] of [year].

We are awaiting the orders of:
[list of non-ready players with their order statuses]
There are [N] days until the deadline, which is at [date]"
```

run as `dipbot report`, dipbot will produce the output of `$status`.

## configuration

both `dipbot daemon` and `dipbot report` receive their configuration
from environment variables. Both need to know which game to look at;
`dipbot daemon` also needs to know its discord API key.

### compulsory environment variables

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

these [environment
variables](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
can be set for a single session like this:

``` shell
$ export WEBDIP_GAME_ID=[game_id]
$ export DISCORD_API_KEY=[api_key]
```
that will let dipbot work in the current shell; to avoid having to run these commands, you can put the variable assignments in the config file for your shell (~/.bashrc, ~/.zshrc or whatever).

### handling multiple games

Both `dipbot daemon` and `dipbot report` will get whatever game has
the id specified by WEBDIP_GAME_ID. You could therefore make little
wrapper scripts for dipbot report and get reports on as many games as
you liked. In future an option to specify the game id on the
commandline will be added to eliminate this minor inconvenience.


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

which attempts to initialize a discord bot corresponding to the token stored in DISCORD_API_KEY.
