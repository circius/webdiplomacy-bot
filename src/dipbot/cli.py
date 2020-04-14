# -*- coding: utf-8 -*-
"""basic cli interface for the functions of dipbot.

"""
from dipbot import scraper, app
import click
from dipbot import app, bot, utilities
from dipbot.data_definitions import DipGame


@click.group()
def cli():
    pass


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="prints verbose output")
def report(verbose):
    game_id = utilities.get_env_var_checked(app.WEBDIP_ID_ENV_VAR_NAME)
    try:
        assert game_id != False
    except:
        exit(1)
    dipgame = scraper.get_dipgame_checked(game_id)
    try:
        assert dipgame != False
    except:
        click.echo("exiting...")
        exit(1)

    click.echo(app.announce_overall_game_state(dipgame, verbose))


@cli.command()
def daemon():
    click.echo("initialising daemon")
    bot.main()
