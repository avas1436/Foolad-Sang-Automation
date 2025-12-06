import typer
from rich import print
from rich.panel import Panel

app = typer.Typer(help="✨ Welcome to Foolad Sang Automation app ✨")


def tester():
    print(
        """
        ⚠️ The 'tester' command is currently deprecated and no longer maintained.
        """
    )
    from tester.tester_main import main_tester

    main_tester()


def sql():
    print(
        """
        📂 SQL module is under development. Database operations will be available soon.
        """
    )


def plotter():
    print(
        """📊 Plotter module is not yet implemented.
        Visualization features will be added later."""
    )


def analyzer():
    print(
        """
        📈 Analyzer module is currently inactive. Performance analysis tools will be
        integrated soon.
        """
    )


def eitta():
    print(
        """
        💬 Eitta module is in progress. Automated scraping and reporting will be 
        enabled in future releases.
        """
    )


if __name__ == "__main__":
    # نمایش راهنما در ابتدای اجرای برنامه
    help_text = """[bold cyan]✨ Welcome to Foolad Sang Automation app ✨[/bold cyan]

    Usage:
        python main.py

    Parameters (will be asked interactively):
        [yellow]-T, --tester[/yellow]     Validate the accuracy and consistency of IS daily reports
        [yellow]-S, --sql[/yellow]        Interact seamlessly with the production database
        [yellow]-P, --plotter[/yellow]    Generate insightful visualizations from SQL data
        [yellow]-A, --analyzer[/yellow]   Evaluate and monitor FSM production performance
        [yellow]-E, --eitta[/yellow]      Scrape and analyze data from Eitta group and share insights automatically

    Description:
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        """

    print(
        Panel.fit(
            help_text, title="[bold magenta]HELP[/bold magenta]", border_style="blue"
        )
    )

    # while True:
    #     try:
    #         # گرفتن دستور از کاربر
    #         command = (
    #             click.prompt(
    #                 text="✨ Please enter the command you want to run", type=str
    #             )
    #             .strip()
    #             .lower()
    #         )

    #         # اجرای دستور وارد شده
    #         cli.main(args=command.split(), standalone_mode=False)

    #         # پرسش برای ادامه یا خروج
    #         click.confirm(
    #             "🔄 Would you like to continue using Foolad Sang Automation?",
    #             default=True,
    #             abort=True,
    #         )

    #     except click.Abort:
    #         click.secho(
    #             message="🌙 Program closed successfully. Goodbye!", fg="blue", bold=True
    #         )
    #         break

    #     except Exception as e:
    #         click.secho(
    #             message=f"❌ An unexpected error occurred: {e}", fg="red", bold=True
    #         )
