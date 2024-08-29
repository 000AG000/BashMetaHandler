"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """bmh."""


if __name__ == "__main__":
    main(prog_name="BashMetaHandler")  # pragma: no cover
