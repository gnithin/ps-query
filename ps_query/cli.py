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
    help="The actual query inside single quotes"
)
@click.option(
    '--json', '-j',
    count=True,
    help="JSON output is the default now. Will change to tabular format"
)
def ps_query(all, latest, query, json):
    '''
    Example usage -
    $ ps_query -q 'command = "/bin/bash" and image = "ubuntu"'
    [{'Config.Cmd': [u'/bin/bash'],
      'Config.Image': u'ubuntu',
        'Created': u'2015-09-13T11:02:00.462203807Z',
        ...
        ...
    --------------------------------------------------
     5 entries matched!
    --------------------------------------------------
    '''
    l_arg = "l"
    a_arg = "a"
    arg = None

    if all < latest:
        arg = l_arg
    else:
        arg = a_arg

    if query is None:
        query = ""

    container_details, status = qry.get_container_details(
        arg,
        query
    )

    if not status :
        click.echo(
            "%s\n%s\n%s" %
            (
                "-"*50,
                container_details,
                "-"*50
            )
        )

    else:
        output_size = len(container_details)

        output_format = pformat(
            container_details
        )

        # Right now forcing json output
        '''
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
        '''
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
