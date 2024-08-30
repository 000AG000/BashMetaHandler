"""Command-line interface."""
from BashMetaHandler import *
import click


@click.command()
@click.version_option()
def main():
    print("BashMetaHandler tested")


if __name__ == "__main__":
    main(prog_name="BashMetaHandler")  # pragma: no cover
