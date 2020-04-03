# -*- coding: utf-8 -*-
"""basic cli interface for the functions of dipbot.

"""
from dipbot import scraper, app
import click
from dipbot import app
from dipbot.data_definitions import DipGame


@click.command()
def cli():
    game_id = app.get_env_var_checked(app.WEBDIP_ID_ENV_VAR_NAME)
    dipgame = scraper.get_dipgame_checked(game_id)
    try:
        assert dipgame != False
    except:
        click.echo("exiting...")
        exit()

    click.echo(app.announce_overall_game_state(dipgame))
