from decimal import Decimal

import jdatetime
from rich import print


def convert_jdate(date: str):
    """تبدیل فرمت به تاریخ شمسی برای بررسی دقیق تر"""
    year, month, day = map(int, date.strip().split("/"))
    jdate = jdatetime.date(year, month, day)
    return jdate


def checker(data, first_date):

    # اگر تاریخ ندادیم اولین روز رو قرار بده به عنوان معیار
    if first_date == "":
        first_date = convert_jdate(date=data[0][0])
    else:
        first_date = convert_jdate(date=first_date)

    for i, record in enumerate(data):
        # اگر حتی یکی از مقادیر عددی نبود
        if any(
            value is None or (isinstance(value, str) and value.strip() == "")
            for value in record[1:]
        ):
            print(
                f"[bold red] Day {i+1}[/bold red] → [yellow]Data is empty[/yellow] — [italic]skipping...[/italic]"
            )
            continue

        # قسمت مربوط به تعیین صحت تاریخ
        excepted_date = first_date + jdatetime.timedelta(days=i)
        record_date = convert_jdate(date=f"{record[0].strip()}")

        if record_date != excepted_date:
            print(
                f"[bold magenta] Day {i+1}[/bold magenta] → [red]Date mismatch![/red] Expected: {excepted_date}, Got: {record_date}"
            )

        # قسمت مربوط به تعیین مشکلات دانه بندی
        if (record[2] + record[3] != record[1]) or (
            record[1] + record[4] + record[5] != Decimal("100.00")
        ):
            print(
                f"[bold yellow] Day {i+1}: Granulation calculation error[/bold yellow]"
            )
            if record[2] + record[3] != record[1]:
                print(
                    f"[cyan]   Sum of 0-5 ({record[2]}) and 5-10 ({record[3]})[/cyan]"
                )
                print(f"[cyan]   does not equal below 10 ({record[1]})[/cyan]")
                print("[dim]   ─────────────────────────[/dim]")
            if record[1] + record[4] + record[5] != Decimal("100.00"):
                print(f"[cyan]   Below 10: {record[1]}[/cyan]")
                print(f"[cyan]   10-60:    {record[4]}[/cyan]")
                print(f"[cyan]   Above 60: {record[5]}[/cyan]")
                print(f"[red]   does not equal 100%[/red]")
                print("[dim]   ─────────────────────────[/dim]")
            if record[6] != 0 and record[7] != 0:
                avg_tonnage = record[6] / record[7]
                if avg_tonnage < Decimal("24.2") or avg_tonnage > Decimal("26.8"):
                    print(
                        f"[bold yellow] Day {i+1}: Tonnage or number of truck is not correct![/bold yellow]"
                    )
                    print("[dim]   ─────────────────────────[/dim]")
        else:
            print(f"[bold green] Day {i+1}: Everything looks great![/bold green]")


# how to use
# checker(data=data, first_date="")
