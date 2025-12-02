import datetime
import re

import click
import jdatetime
import pandas as pd


@click.group()
def cli():
    """Daily data extraction CLI tool."""
    pass


def normalize_time(val):
    """Convert time values to HH:MM format string."""
    if pd.isna(val):
        return None
    if isinstance(val, datetime.datetime):
        return val.strftime("%H:%M")
    elif isinstance(val, datetime.time):
        return val.strftime("%H:%M")
    elif isinstance(val, str):
        s = val.strip().replace(";", ":").replace("：", ":")
        s = re.sub(r'[AP]M$', '', s, flags=re.IGNORECASE).strip()
        match = re.search(r'(\d{1,2}):(\d{1,2})', s)
        if match:
            h, m = match.groups()
            return f"{int(h):02d}:{int(m):02d}"
    return None


def extract_date_from_sheet(df):
    """Find Shamsi date string in the sheet."""
    date_pattern = r'(\d{4}/\d{2}/\d{2})'
    for i in range(min(30, len(df))):
        for j in range(min(10, df.shape[1])):
            cell_value = str(df.iloc[i, j])
            match = re.search(date_pattern, cell_value)
            if match:
                return match.group(1)
    return None


def first_non_null(series):
    s = series.dropna()
    return s.iloc[0] if len(s) else None


def extract_daily_data_from_excel(file_path):
    """Core function to extract daily data from Excel."""
    xls = pd.ExcelFile(rf"{file_path}")
    all_data = []

    for sheet_name in xls.sheet_names:
        try:
            click.echo(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

            shamsi_date = extract_date_from_sheet(df)
            if not shamsi_date:
                click.secho(f"Warning: No date found in sheet {sheet_name}", fg="red")
                continue

            # Find header row
            start_idx = None
            for i in range(min(40, len(df))):
                if "Time" in str(df.iloc[i, 0]):
                    start_idx = i
                    break
            if start_idx is None:
                click.secho(
                    f"Warning: No 'Time' header row in sheet {sheet_name}", fg="red"
                )
                continue

            headers = df.iloc[start_idx].tolist()
            df_block = df.iloc[start_idx + 1 :].copy()
            df_block.columns = headers

            # Forward-fill Time
            df_block["Time"] = df_block["Time"].ffill()
            df_block = df_block[df_block["Time"].notna()]
            df_block["Time"] = df_block["Time"].apply(normalize_time)

            # Rename columns
            column_mapping = {}
            for col in df_block.columns:
                col_str = str(col).strip()
                if col_str == "Time":
                    column_mapping[col] = "Time"
                elif "CO2 Klin no.1" in col_str:
                    column_mapping[col] = "CO2_Klin1"
                elif "CO2 Klin no.2" in col_str:
                    column_mapping[col] = "CO2_Klin2"
                elif ">40mm" in col_str:
                    column_mapping[col] = "CO2_gt40mm"
                elif "0-5" in col_str:
                    column_mapping[col] = "pct_0_5"
                elif "5-10" in col_str:
                    column_mapping[col] = "pct_5_10"
                elif "10-60" in col_str:
                    column_mapping[col] = "pct_10_60"
                elif ">60" in col_str:
                    column_mapping[col] = "pct_gt60"
                elif "<10" in col_str:
                    column_mapping[col] = "pct_lt10"
            df_block = df_block.rename(columns=column_mapping)

            keep_cols = [
                "Time",
                "CO2_Klin1",
                "CO2_Klin2",
                "CO2_gt40mm",
                "pct_lt10",
                "pct_0_5",
                "pct_5_10",
                "pct_10_60",
                "pct_gt60",
            ]
            existing = [c for c in keep_cols if c in df_block.columns]
            df_data = df_block[existing].copy()

            # Add sheet info
            df_data["SheetName"] = sheet_name
            df_data["ShamsiDate"] = shamsi_date

            # Merge multiple rows per (ShamsiDate, Time)
            non_time_cols = [c for c in existing if c != "Time"]
            df_data = df_data.groupby(["ShamsiDate", "Time"], as_index=False).agg(
                {c: first_non_null for c in non_time_cols + ["SheetName"]}
            )

            # Build Shamsi datetime
            def build_shamsi_dt(row):
                try:
                    time_str = str(row["Time"])
                    year, month, day = map(int, row["ShamsiDate"].split("/"))
                    hour, minute = map(int, time_str.split(":")[:2])
                    jd = jdatetime.datetime(year, month, day, hour, minute)
                    if time_str in ["00:00", "04:00"]:
                        jd += jdatetime.timedelta(days=1)
                    return jd
                except Exception as e:
                    click.secho(
                        message=f"Error building datetime for {row.get('Time')}: {e}",
                        fg="red",
                    )
                    return None

            df_data["ShamsiDateTime"] = df_data.apply(build_shamsi_dt, axis=1)
            df_data = df_data[df_data["ShamsiDateTime"].notna()]

            # Gregorian conversion
            df_data["GregorianDateTime"] = df_data["ShamsiDateTime"].apply(
                lambda x: x.togregorian()
            )

            # Create timestamp (Unix timestamp in seconds)
            df_data["Timestamp"] = df_data["GregorianDateTime"].apply(
                lambda x: int(x.timestamp()) if x else None
            )

            all_data.append(df_data)
            click.secho(
                f"Sheet {sheet_name}: {len(df_data)} rows extracted", fg="green"
            )

        except Exception as e:
            click.secho(f"Error processing sheet {sheet_name}: {e}", fg="red")
            continue

    if not all_data:
        return pd.DataFrame()

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.sort_values("Timestamp").reset_index(drop=True)

    base_cols = ["Timestamp", "ShamsiDate", "Time"]
    data_cols = [
        "CO2_Klin1",
        "CO2_Klin2",
        "CO2_gt40mm",
        "pct_lt10",
        "pct_0_5",
        "pct_5_10",
        "pct_10_60",
        "pct_gt60",
    ]
    final_cols = base_cols + [c for c in data_cols if c in final_df.columns]
    return final_df[final_cols]


@cli.command()
@click.option(
    "--file-path",
    default="daily.xlsx",
    help="Path to the Excel file",
    show_default=True,
)
def daily_full_extractor(file_path: str):
    """
    Extract daily data from Excel and print a clear summary.
    Returns the extracted DataFrame for use in other programs.
    """
    click.secho("Starting data extraction from Excel file...", fg="blue")
    final_data = extract_daily_data_from_excel(file_path)

    if final_data.empty:
        click.secho("No data extracted.", fg="red")
        # اگر کاربر بخواهد، برنامه همین‌جا متوقف می‌شود
        click.confirm("Do you want to exit?", abort=True)
        return final_data

    # نمایش خلاصه
    click.secho(f"✅ Extracted {len(final_data)} total rows", fg="green")
    click.echo("📊 Columns summary:")
    for col in final_data.columns:
        non_null = final_data[col].notna().sum()
        dtype = final_data[col].dtype
        click.secho(f" • {col}: {non_null} non-null values ({dtype})", fg="yellow")

    # نمایش نمونه داده‌ها
    if click.confirm("Do you want to see sample rows of the dataframe?", default=True):
        click.echo(final_data.head(20).to_string())

    return final_data


if __name__ == "__main__":
    daily_full_extractor()
