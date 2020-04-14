[![Build Status](https://travis-ci.org/circius/webdiplomacy-bot.svg?branch=master)](https://travis-ci.org/circius/webdiplomacy-bot)

## summary

This is a discord bot which scrapes the current status of games at
webdiplomacy and announces that information on discord.

It also incorporates a very rudimentary cli tool which does the same
thing on the host.

## functionality

When running as a discord bot, dipbot will produce output when it sees
the following messages:

 - `$status`, which produces a concise statement of the webdiplomacy game state,
 - `$status!`, which produces the output of `$status`, but also mentions @everyone,
 - `$status?`, which produces the output of `$status`, along with a
   verbose description of the game phase, and
 - `$status?!`, or `$status!?`, which produces the output of
   `$status?` but also mentions @everyone.

A `$status` request produces output in the following format:

``` shell
"It is the [season] of [year].
[phase].
We are awaiting the order of:
[list of non-ready players with their order statuses]"
```
run as `dipbot report`, dipbot will produce the output of `$status`.

## configuration

dipbot depends on two environment variables which must be correctly
set for it to function. There are also two environment variables which
it is highly advisable to set, since the bot is able to be more
informative in its verbose mode if they are.

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

### optional environment variables

Dipbot is able to provide verbose output in order to give new players
more support in understanding the significance of the various
phases. This verbose output varies according to the phase, and
includes an announcement of the amount of time the group has decided
to allow for each turn. For instance, a group might want to run a game
in which 7 days are allowed for the diplomacy phases, but the builds
and retreats phases should be completed within 2 days each.

In order to support this kind of adjustment of the verbose messages,
dipbot supports two further environment variables: MAIN_PHASE_LENGTH
(representing diplomacy phases) and AUXILIARY_PHASE_LENGTH
(representing builds and retreats.) They should be set to an english
phrase representing duration, for instance "7 days" or "24 hours".

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

which attempts to initialize a discord bot corresponding to the token stored in DISCORD_API_KEY, and which will respond with a report when addressed on discord with the messages "$status" and "$status!".
