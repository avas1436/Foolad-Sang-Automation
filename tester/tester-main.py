import click


@click.group()
def cli():
    """
    Validate the accuracy and consistency of IS daily reports
    """
    pass


@cli.command(name="load-data")
@click.option(
    '--start_day', prompt='Enter start day', default=1, type=int, show_default=True
)
@click.option(
    '--end_day', prompt='Enter end day', default=31, type=int, show_default=True
)
@click.option(
    '--file_path', prompt='Enter file path', default='daily.xlsx', show_default=True
)
def tester(file_path, start_day, end_day):
    print(f"{file_path}{start_day}{end_day}")