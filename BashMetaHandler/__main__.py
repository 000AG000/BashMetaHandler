"""Command-line interface."""
import click

from BashMetaHandler import *


@click.command()
@click.version_option()
def main() -> int:
    print("BashMetaHandler tested")
    return 0


if __name__ == "__main__":
    main(prog_name="BashMetaHandler")  # pragma: no cover
