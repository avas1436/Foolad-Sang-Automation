import click

from packages.IS_Tester import check_daily


@click.group()
def cli():
    """
    ✨ Foolad Sang Automation App ✨

    Features:
      • tester    : Verify the accuracy and consistency of the daily production report
      • analyze   : Analyze text data and provide insights
      • calculate : Perform numeric calculations
    """
    pass


@cli.command(help="Check the accuracy of the daily production report")
def tester():
    try:
        check_daily.main(standalone_mode=False)
    except Exception as e:
        click.secho("⚠️  Error in Tester feature.", fg="red")
        click.echo(f"   Details: {e}")


@cli.command(help="Analyze text data")
@click.argument("text")
def analyze(text):
    click.echo(f"Analyzing text: {text}")


@cli.command(help="Square a number")
@click.option("--number", type=int, required=True)
def calculate(number):
    click.echo(f"Result: {number ** 2}")


if __name__ == "__main__":
    # نمایش راهنما در ابتدای برنامه
    cli.main(["--help"], standalone_mode=False)

    while True:
        try:
            # گرفتن دستور از کاربر
            command = click.prompt(
                text="✨ Enter the command you want to run", type=str
            ).strip()
            cli.main(command.split(), standalone_mode=False)

            # فقط با confirm تصمیم به ادامه یا خروج گرفته می‌شود
            click.confirm(
                "Would you like to continue using the app?", default=True, abort=True
            )

        except click.Abort:
            click.echo("Program closed successfully. Goodbye! 🌙")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")
