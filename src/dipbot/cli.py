# -*- coding: utf-8 -*-
"""basic cli interface for the functions of dipbot.

"""
from dipbot import scraper, app
import click


@click.command()
def cli():
    game_to_parse = click.prompt(
        "Type the id of the game you want to check: ", type=int
    )
    dipgame = scraper.get_dipgame(game_to_parse)
    click.echo(app.announce_overall_game_state(dipgame))
