# beeminder-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/beeminder-to-sqlite.svg)](https://pypi.org/project/beeminder-to-sqlite/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/bcongdon/beeminder-to-sqlite/blob/master/LICENSE)

TODO: Add brief description

## How to install

    $ pip install beeminder-to-sqlite

## Authentication

Run the following command and enter your beeminder personal auth token:

    $ beeminder-to-sqlite auth

This will create a file called `auth.json` in your current directory containing
the required value. To save the file at a different path or filename, use the
`--auth=myauth.json` option.

## Usage

TODO: Add usage instructions

## Attribution

This package is heavily inspired by
[goodreads-to-sqlite](https://github.com/rixx/goodreads-to-sqlite/) by
[Tobias Kunze ](https://github.com/rixx) and
[github-to-sqlite](https://github.com/dogsheep/github-to-sqlite/) by
[Simon Willison](https://simonwillison.net/2019/Oct/7/dogsheep/).

This package was designed to fit nicely in the
[dogsheep](https://dogsheep.github.io/) /
[datasette](https://github.com/simonw/datasette) ecosystems.
