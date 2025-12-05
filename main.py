import typer

# @click.group()
# def cli():
#     """✨ Welcome to Foolad Sang Automation app ✨"""
#     pass


# @cli.command(help="Validate the accuracy and consistency of IS daily reports")
def tester():
    print(
        """
        ⚠️ The 'tester' command is currently deprecated and no longer maintained.
        """
    )


# @cli.command(help="Interact seamlessly with the production database")
def sql():
    print(
        """
        📂 SQL module is under development. Database operations will be available soon.
        """
    )


# @cli.command(help="Generate insightful visualizations from SQL data")
def plotter():
    print(
        """📊 Plotter module is not yet implemented.
        Visualization features will be added later."""
    )


# @cli.command(help="Evaluate and monitor FSM production performance")
def analyzer():
    print(
        """
        📈 Analyzer module is currently inactive. Performance analysis tools will be
        integrated soon.
        """
    )


# @cli.command(
#     help="Scrape and analyze data from Eitta group and share insights automatically"
# )
def eitta():
    print(
        """
        💬 Eitta module is in progress. Automated scraping and reporting will be 
        enabled in future releases.
        """
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
