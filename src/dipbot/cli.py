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
    dipgame = scraper.get_dipgame_checked(app.get_game_id())
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
