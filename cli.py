#!/usr/bin/env python
import click
from main import ps_query as qry
from pprint import pformat


@click.command()
@click.option(
    '--all', '-a',
    count=True,
    help="All logs"
)
@click.option(
    '--latest', '-l',
    count=True,
    help="Latest logs"
)
@click.option(
    '--query', '-q',
    type=str,
)
@click.option(
    '--json', '-j',
    count=True
)
def ps_query(all, latest, query, json):
    l_arg = "l"
    a_arg = "a"
    arg = None

    if all < latest:
        arg = l_arg
    else:
        arg = a_arg

    if query is None:
        query = ""

    container_details = qry.get_container_details(
        arg,
        query
    )

    output_size = len(container_details)

    output_format = pformat(
        container_details
    )

    if json == 0:
        # print in table format
        # Probably use Pylsy for this
        click.echo("""
            Better looking output comingup!
            (Use -j option instead ;)
        """)
        pass
    else:
        click.echo(output_format)

    # Size info
    output_size_info = (
        "\n%s\n %d entries matched!\n%s\n"
        %
        ("-"*50 , output_size, "-"*50)
    )

    click.echo(output_size_info)

if __name__ == "__main__":
    ps_query()
