import click


@click.group()
def cli():
    """✨ Welcome to Foolad Sang Automation app ✨"""
    pass


@cli.command(help="Validate the accuracy and consistency of IS daily reports")
def tester():
    click.secho(
        message="""
        ⚠️ The 'tester' command is currently deprecated and no longer maintained.
        """,
        fg="red",
        bold=True,
    )


@cli.command(help="Interact seamlessly with the production database")
def sql():
    click.secho(
        message="""
        📂 SQL module is under development. Database operations will be available soon.
        """,
        fg="red",
        bold=True,
    )


@cli.command(help="Generate insightful visualizations from SQL data")
def plotter():
    click.secho(
        message="""📊 Plotter module is not yet implemented.
        Visualization features will be added later.""",
        fg="red",
        bold=True,
    )


@cli.command(help="Evaluate and monitor FSM production performance")
def analyzer():
    click.secho(
        message="""
        📈 Analyzer module is currently inactive. Performance analysis tools will be
        integrated soon.
        """,
        fg="red",
        bold=True,
    )


@cli.command(
    help="Scrape and analyze data from Eitta group and share insights automatically"
)
def eitta():
    click.secho(
        message="""
        💬 Eitta module is in progress. Automated scraping and reporting will be 
        enabled in future releases.
        """,
        fg="red",
        bold=True,
    )


if __name__ == "__main__":
    # نمایش راهنما در ابتدای اجرای برنامه
    cli.main(args=["--help"], standalone_mode=False)

    while True:
        try:
            # گرفتن دستور از کاربر
            command = (
                click.prompt(
                    text="✨ Please enter the command you want to run", type=str
                )
                .strip()
                .lower()
            )

            # اجرای دستور وارد شده
            cli.main(args=command.split(), standalone_mode=False)

            # پرسش برای ادامه یا خروج
            click.confirm(
                "🔄 Would you like to continue using Foolad Sang Automation?",
                default=True,
                abort=True,
            )

        except click.Abort:
            click.secho(
                message="🌙 Program closed successfully. Goodbye!", fg="blue", bold=True
            )
            break

        except Exception as e:
            click.secho(
                message=f"❌ An unexpected error occurred: {e}", fg="red", bold=True
            )
