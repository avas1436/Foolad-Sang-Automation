import typer
from check_data import checker
from load_is_daily import load_is_daily
from rich import print
from rich.panel import Panel

app = typer.Typer(help="📊 Validate the accuracy and consistency of IS daily reports")


@app.command()
def tester():
    # نمایش راهنما در ابتدای اجرا
    help_text = """[bold cyan]📊 Daily Excel Report Checker CLI[/bold cyan]

    Usage:
        python tester_main.py

    Parameters (will be asked interactively):
        [yellow]-f, --file[/yellow]   Path to the Excel file (default: daily.xlsx)
        [yellow]-s, --start[/yellow]  Start day (default: 1)
        [yellow]-e, --end[/yellow]    End day (default: 31)
        [yellow]-d, --date[/yellow]   First date in Shamsi format (e.g. 1404/07/26)

    Description:
        This program loads daily Excel reports and checks data consistency.
        You will be prompted for each parameter step by step.
        """

    print(
        Panel.fit(
            help_text, title="[bold magenta]HELP[/bold magenta]", border_style="blue"
        )
    )
    # گرفتن ورودی‌ها به صورت تعاملی
    file_path = typer.prompt(text="📂 Enter Excel file path", default="daily.xlsx")
    start_day = typer.prompt(text="🔢 Enter start day", default=1)
    end_day = typer.prompt(text="🔢 Enter end day", default=31)
    date = typer.prompt(
        text="📅 Enter first date (Shamsi, e.g. 1404/07/26)", default=""
    )

    print(f"[cyan]📂 Loading file:[/cyan] {file_path}")
    data = load_is_daily(
        file_path=rf"{file_path}", start_day=int(start_day), end_day=int(end_day)
    )
    print("[yellow]🔎 Checking data...[/yellow]")
    checker(data=data, first_date=date)
    print("[bold green]🎉 Done![/bold green]")


def main_tester():
    app()


if __name__ == "__main__":
    app()
