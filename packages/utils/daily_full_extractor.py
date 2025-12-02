import datetime
import re

import jdatetime
import pandas as pd


def normalize_time(val):
    """Convert time values to HH:MM format string."""
    if pd.isna(val):
        return None

    # If it's already a string, process it
    if isinstance(val, str):
        s = val.strip().replace(";", ":").replace("：", ":")
        # Remove any AM/PM indicators
        s = re.sub(r'[AP]M$', '', s, flags=re.IGNORECASE).strip()

        if ":" in s:
            parts = s.split(":")
            if len(parts) >= 2:
                h, m = parts[0], parts[1]
                # Clean hour and minute
                h = h.strip()
                m = m.strip().split(".")[0]  # Remove decimal part if exists

                if h.isdigit() and m.isdigit():
                    h = int(h)
                    m = int(m)
                    return f"{h:02d}:{m:02d}"

        # Handle other formats like "1900-01-01 00:00:00"
        time_match = re.search(r'(\d{1,2}):(\d{1,2})', s)
        if time_match:
            h, m = time_match.groups()
            if h.isdigit() and m.isdigit():
                return f"{int(h):02d}:{int(m):02d}"

        return None

    # Handle datetime.time objects
    elif isinstance(val, datetime.time):
        return val.strftime("%H:%M")

    # Handle datetime.datetime objects
    elif isinstance(val, datetime.datetime):
        return val.strftime("%H:%M")

    return None


def extract_date_from_sheet(df):
    """Find Shamsi date string in the sheet."""
    date_pattern = r'(\d{4}/\d{2}/\d{2})'
    for i in range(min(20, len(df))):
        for j in range(min(10, len(df.columns))):
            cell_value = str(df.iloc[i, j])
            match = re.search(date_pattern, cell_value)
            if match:
                return match.group(1)
    return None


def extract_daily_data_from_excel(file_path):
    xls = pd.ExcelFile(file_path)
    all_data = []

    for sheet_name in xls.sheet_names:
        try:
            print(f"\nProcessing sheet: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

            # Find date
            shamsi_date = extract_date_from_sheet(df)
            if not shamsi_date:
                print(f"Warning: No date found in sheet {sheet_name}")
                continue

            print(f"Found date: {shamsi_date}")

            # Find header row - look for 'Time' in any column
            start_idx = None
            for i in range(min(30, len(df))):
                for j in range(min(5, len(df.columns))):
                    cell_val = str(df.iloc[i, j])
                    if "Time" in cell_val and not cell_val.startswith("=AVERAGE"):
                        start_idx = i
                        print(f"Found header at row {start_idx}")
                        break
                if start_idx is not None:
                    break

            if start_idx is None:
                print(f"Warning: No 'Time' row found in sheet {sheet_name}")
                continue

            # Read two rows as headers
            main_headers = df.iloc[start_idx].tolist()
            sub_headers = []
            if start_idx + 1 < len(df):
                sub_headers = df.iloc[start_idx + 1].tolist()
            else:
                sub_headers = [None] * len(main_headers)

            # Combine headers
            headers = []
            for main, sub in zip(main_headers, sub_headers):
                main_str = str(main) if pd.notna(main) else ""
                sub_str = str(sub) if pd.notna(sub) else ""

                # Clean header strings
                main_str = main_str.strip()
                sub_str = sub_str.strip()

                # Use sub-header if it's meaningful
                if (
                    sub_str
                    and sub_str not in ["nan", "None", ""]
                    and "Unnamed" not in sub_str
                ):
                    headers.append(sub_str)
                elif (
                    main_str
                    and main_str not in ["nan", "None", ""]
                    and "Unnamed" not in main_str
                ):
                    headers.append(main_str)
                else:
                    headers.append("")

            # Debug: print headers
            print(f"Headers: {headers}")

            # Process data rows
            data_rows = []
            i = start_idx + 2

            while i < len(df):
                row1 = df.iloc[i].tolist() if i < len(df) else [None] * len(headers)

                # Check if this row has time data
                time_val = None
                if len(row1) > 0 and pd.notna(row1[0]):
                    time_val = normalize_time(row1[0])

                if time_val:
                    # Create dictionary for this time entry
                    row_dict = {"Time": time_val}

                    # Add data from first row
                    for j, header in enumerate(headers):
                        if j < len(row1) and header and pd.notna(row1[j]):
                            # Skip if it's a formula
                            if isinstance(row1[j], str) and row1[j].startswith("="):
                                continue
                            row_dict[header] = row1[j]

                    # Check for second row with additional data
                    if i + 1 < len(df):
                        row2 = df.iloc[i + 1].tolist()
                        # Check if row2 has data in the particle size columns (typically columns I, J)
                        has_particle_data = False
                        for j in range(min(12, len(row2))):
                            if pd.notna(row2[j]) and str(row2[j]).strip():
                                has_particle_data = True
                                break

                        if has_particle_data:
                            # Add data from second row
                            for j, header in enumerate(headers):
                                if j < len(row2) and header and pd.notna(row2[j]):
                                    # Skip if it's a formula
                                    if isinstance(row2[j], str) and row2[j].startswith(
                                        "="
                                    ):
                                        continue
                                    row_dict[header] = row2[j]
                            i += 2  # Skip both rows
                        else:
                            i += 1  # Only skip first row
                    else:
                        i += 1

                    data_rows.append(row_dict)
                else:
                    i += 1

            if not data_rows:
                print(f"Warning: No data rows in sheet {sheet_name}")
                continue

            df_data = pd.DataFrame(data_rows)
            print(f"Raw data shape: {df_data.shape}")
            print(f"Raw columns: {list(df_data.columns)}")

            # Rename columns
            column_mapping = {}
            for col in df_data.columns:
                col_str = str(col).strip()

                if col_str == "Time":
                    continue
                elif any(x in col_str for x in ["CO2 Klin no.1", "CO2 Klin no.1 (%)"]):
                    column_mapping[col] = "CO2_Klin1"
                elif any(x in col_str for x in ["CO2 Klin no.2", "CO2 Klin no.2 (%)"]):
                    column_mapping[col] = "CO2_Klin2"
                elif any(x in col_str for x in [">40mm", "CO2 >40mm"]):
                    column_mapping[col] = "CO2_gt40mm"
                elif any(x in col_str for x in ["0-5", "0-5 (%)"]):
                    column_mapping[col] = "pct_0_5"
                elif any(x in col_str for x in ["5-10", "5-10 (%)"]):
                    column_mapping[col] = "pct_5_10"
                elif any(x in col_str for x in ["10-60", "10-60 (%)"]):
                    column_mapping[col] = "pct_10_60"
                elif any(x in col_str for x in [">60", ">60 (%)"]):
                    column_mapping[col] = "pct_gt60"
                elif any(x in col_str for x in ["<10", "<10 (%)"]):
                    column_mapping[col] = "pct_lt10"
                elif col_str and col_str != "nan":
                    # Keep original name for other columns
                    column_mapping[col] = col_str

            df_data = df_data.rename(columns=column_mapping)

            # Add sheet info
            df_data["SheetName"] = sheet_name
            df_data["ShamsiDate"] = shamsi_date

            # Build ShamsiDateTime - fix for datetime.time objects
            def adjust_datetime(row):
                try:
                    time_val = row["Time"]

                    # Ensure time_val is string
                    if isinstance(time_val, datetime.time):
                        time_str = time_val.strftime("%H:%M")
                    elif isinstance(time_val, datetime.datetime):
                        time_str = time_val.strftime("%H:%M")
                    else:
                        time_str = str(time_val)

                    if not time_str or pd.isna(time_str):
                        return None

                    # Extract hour and minute
                    hour, minute = 0, 0
                    if ":" in time_str:
                        parts = time_str.split(":")
                        hour = int(parts[0])
                        minute = int(parts[1])

                    year, month, day = map(int, row["ShamsiDate"].split("/"))
                    jd = jdatetime.datetime(year, month, day, hour, minute)

                    # Adjust for next day if time is 00:00 or 04:00
                    if time_str in ["00:00", "04:00"]:
                        jd += jdatetime.timedelta(days=1)

                    return jd
                except Exception as e:
                    print(f"Error building datetime for {time_val}: {e}")
                    return None

            df_data["ShamsiDateTime"] = df_data.apply(adjust_datetime, axis=1)

            # Remove rows with invalid datetime
            initial_rows = len(df_data)
            df_data = df_data[df_data["ShamsiDateTime"].notna()]
            removed_rows = initial_rows - len(df_data)
            if removed_rows > 0:
                print(f"Removed {removed_rows} rows with invalid datetime")

            # Convert to Gregorian
            df_data["GregorianDateTime"] = df_data["ShamsiDateTime"].apply(
                lambda x: x.togregorian() if x else None
            )
            df_data["Timestamp"] = df_data["GregorianDateTime"].apply(
                lambda x: x.isoformat(sep=" ") if x else None
            )

            all_data.append(df_data)
            print(f"Sheet {sheet_name}: {len(df_data)} rows extracted")

        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")
            import traceback

            traceback.print_exc()
            continue

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # Sort by datetime
        if "GregorianDateTime" in final_df.columns:
            final_df = final_df.sort_values("GregorianDateTime").reset_index(drop=True)

        # Define column order
        base_cols = ["SheetName", "ShamsiDate", "Time", "Timestamp"]
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

        # Filter to existing columns
        final_cols = base_cols + [c for c in data_cols if c in final_df.columns]

        # Reorder and return
        return final_df[final_cols]
    else:
        return pd.DataFrame()


if __name__ == "__main__":
    input_file = "daily.xlsx"
    output_file = "extracted_data_clean.csv"

    print("Extracting data from Excel file...")
    final_data = extract_daily_data_from_excel(input_file)

    if not final_data.empty:
        print(f"\nExtracted {len(final_data)} total rows")
        # print("\nFirst 30 rows:")
        # print(final_data.head(30).to_string())

        # Column summary
        print("\nColumns extracted:")
        for col in final_data.columns:
            non_null = final_data[col].notna().sum()
            print(f"  {col}: {non_null} non-null values")

        # Check for particle size columns
        particle_cols = ["pct_0_5", "pct_5_10", "pct_10_60", "pct_gt60", "pct_lt10"]
        for col in particle_cols:
            if col in final_data.columns:
                print(f"\n{col} sample values:")
                sample = final_data[col].dropna().head(5)
                if len(sample) > 0:
                    for val in sample:
                        print(f"  {val}")

        # Save to CSV
        final_data.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"\nData saved to {output_file}")
    else:
        print("No data extracted.")
