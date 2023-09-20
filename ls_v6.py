import datetime
from pathlib import Path

import click


@click.command(help="List the content of one or more directories")
@click.option("-l", "--long", is_flag=True, help="Displays the directory content in long format")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def cli(paths, long):
    # For documenting arguments in click add docstring to the underlying function.
    # Also remove the help parameter within click.command()
    # E.g. """List the content of one or more directory
    #
    # PATHS is one or more directory paths whose content will be listed
    # """
    for i, path in enumerate(paths):
        if len(paths) > 1:
            click.echo(f"/{path}/:")
        for entry in path.iterdir():
            entry_output = build_output(entry, long)
            click.echo(f"{entry_output:{len(entry_output) + 5}}", nl=long)
        if i < len(paths) - 1:
            click.echo(f"" if long else "\n")
        elif not long:
            click.echo()


def build_output(entry, long=False):
    if long:
        size = entry.stat().st_size
        date = datetime.date.fromtimestamp(entry.stat().st_mtime)
        return f"{size:>6d} {date:%b %d %H:%M:%S} {entry.name}"
    return entry.name


if __name__ == "__main__":
    cli()
