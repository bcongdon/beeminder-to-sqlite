import sys

import click

FOREIGN_KEYS = [("datapoints", "goal", "goals", "name")]


def error(message):
    click.secho(message, bold=True, fg="red")
    sys.exit(-1)


def add_foreign_keys(db, tables=None):
    for fk in FOREIGN_KEYS:
        if tables and fk[0] not in tables:
            continue
        db.add_foreign_keys([fk])
