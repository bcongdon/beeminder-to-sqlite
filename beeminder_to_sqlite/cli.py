import time
from datetime import timedelta, date
import click
import pathlib
import json
import sqlite_utils
import requests
from tqdm import tqdm
from dateutil.parser import parse as dtparse
from beeminder_to_sqlite import utils

BEEMINDER_API_URL = "https://www.beeminder.com/api/v1/"


@click.group()
@click.version_option()
def cli():
    "Save data from Beeminder to a SQLite database"


@cli.command()
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save tokens to, defaults to ./auth.json.",
)
def auth(auth):
    "Save authentication credentials to a JSON file"
    auth_data = {}
    if pathlib.Path(auth).exists():
        auth_data = json.load(open(auth))

    username = click.prompt("beeminder username")
    click.echo(
        "Visit the following link and find your personal `auth_token`: https://www.beeminder.com/api/v1/auth_token.json"
    )
    auth_token = click.prompt("beeminder auth_token")

    auth_data["beeminder_username"] = username
    auth_data["beeminder_auth_token"] = auth_token
    open(auth, "w").write(json.dumps(auth_data, indent=4) + "\n")
    click.echo()
    click.echo(
        "Your credentials have been saved to {}. You can now import beeminder goals by running".format(
            auth
        )
    )
    click.echo()
    click.echo("    beeminder-to-sqlite goals beeminder.db")
    click.echo()


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save tokens to, defaults to auth.json",
)
def goals(db_path, auth):
    """Download Beeminder goals for the authenticated user"""
    db = sqlite_utils.Database(db_path)

    try:
        data = json.load(open(auth))
        username = data["beeminder_username"]
        auth_token = data["beeminder_auth_token"]
    except (KeyError, FileNotFoundError):
        utils.error(
            "Cannot find authentication data, please run `beeminder_to_sqlite auth`!"
        )

    click.echo("Downloading goals")
    r = requests.get(
        BEEMINDER_API_URL + "users/{}.json".format(username),
        params=dict(auth_token=auth_token),
    )
    goals = r.json().get("goals")
    click.echo("Found goals: {}".format(goals))

    progress_bar = tqdm(total=len(goals))
    progress_bar.set_description("Downloading goal data")

    for goal in goals:
        progress_bar.set_description("Downloading " + goal)

        goal_data = requests.get(
            BEEMINDER_API_URL + "users/{}/goals/{}.json".format(username, goal),
            params=dict(auth_token=auth_token),
        ).json()

        goal_id = "{}/{}".format(username, goal)
        db["goals"].upsert({"name": goal_id, **goal_data}, pk="name")

        datapoints = requests.get(
            BEEMINDER_API_URL
            + "users/{}/goals/{}/datapoints.json".format(username, goal),
            params=dict(auth_token=auth_token),
        ).json()

        for dp in datapoints:
            db["datapoints"].upsert({"goal": goal_id, **dp}, pk="id")

        progress_bar.update(1)
    progress_bar.close()
    utils.add_foreign_keys(db)


if __name__ == "__main__":
    cli()
