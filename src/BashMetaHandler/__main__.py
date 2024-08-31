"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> int:
    """main function for testing

    Returns:
        int: return 0 when properly finished
    """
    print("test")
    return 0


if __name__ == "__main__":
    main(prog_name="BashMetaHandler")  # pragma: no cover
