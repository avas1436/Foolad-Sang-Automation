import datetime
import re

import jdatetime
import numpy as np
import pandas as pd


def normalize_time(val):
    """تبدیل زمان به فرمت استاندارد HH:MM"""
    if pd.isna(val):
        return None

    if isinstance(val, datetime.datetime):
        return val.strftime("%H:%M")
    elif isinstance(val, datetime.time):
        return val.strftime("%H:%M")
    elif isinstance(val, str):
        # حذف ثانیه‌ها اگر وجود دارند
        val = str(val).strip()
        if ':' in val:
            parts = val.split(':')
            if len(parts) >= 2:
                return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
    return str(val)


def extract_date_from_sheet(df):
    """استخراج تاریخ از شیت با جستجوی الگوی تاریخ شمسی"""
    # جستجو در کل DataFrame برای الگوی تاریخ شمسی (مثل 1404/07/01)
    date_pattern = r'(\d{4}/\d{2}/\d{2})'

    # جستجو در سطرهای مختلف
    for i in range(min(20, len(df))):  # فقط 20 سطر اول را بررسی کن
        for j in range(min(10, len(df.columns))):  # فقط 10 ستون اول
            cell_value = str(df.iloc[i, j])
            match = re.search(date_pattern, cell_value)
            if match:
                date_str = match.group(1)
                try:
                    year, month, day = map(int, date_str.split('/'))
                    return jdatetime.date(year, month, day)
                except:
                    continue

    # اگر الگوی تاریخ پیدا نشد، سعی کن از نام شیت استفاده کنی
    return None


def extract_daily_data_from_excel(file_path):
    """استخراج داده‌های روزانه از اکسل"""
    xls = pd.ExcelFile(file_path)
    all_data = []

    for sheet_name in xls.sheet_names:
        try:
            # خواندن شیت
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

            # استخراج تاریخ از شیت
            shamsi_date = extract_date_from_sheet(df)
            if not shamsi_date:
                print(f"هشدار: تاریخ در شیت {sheet_name} یافت نشد")
                continue

            # پیدا کردن ردیف شروع داده‌ها (ردیفی که شامل "Time" است)
            start_idx = None
            for i in range(min(20, len(df))):  # فقط 20 سطر اول را بررسی کن
                cell_value = str(df.iloc[i, 0]) if pd.notna(df.iloc[i, 0]) else ""
                if "Time" in cell_value:
                    start_idx = i
                    break

            if start_idx is None:
                print(f"هشدار: ردیف 'Time' در شیت {sheet_name} یافت نشد")
                continue

            # استخراج هدرها و داده‌ها
            headers = df.iloc[start_idx].tolist()
            data_rows = []

            # جمع‌آوری داده‌ها از ردیف start_idx+1 به بعد
            for i in range(start_idx + 1, len(df)):
                row = df.iloc[i].tolist()

                # اگر زمان وجود دارد
                time_val = row[0]
                if pd.notna(time_val) and str(time_val).strip():
                    # ساخت دیکشنری از داده‌های این ردیف
                    row_dict = {}
                    for j, header in enumerate(headers):
                        if pd.notna(header) and str(header).strip():
                            row_dict[header] = row[j]
                    data_rows.append(row_dict)

            if not data_rows:
                print(f"هشدار: هیچ داده‌ای در شیت {sheet_name} یافت نشد")
                continue

            # تبدیل به DataFrame
            df_data = pd.DataFrame(data_rows)

            # نرمال‌سازی ستون زمان
            if "Time" in df_data.columns:
                df_data["Time"] = df_data["Time"].apply(normalize_time)
                # حذف ردیف‌هایی که زمان ندارند
                df_data = df_data[df_data["Time"].notna()]

            # نامگذاری مجدد ستون‌ها به فرمت استاندارد
            column_mapping = {}
            for col in df_data.columns:
                if "CO2 Klin no.1" in str(col):
                    column_mapping[col] = "CO2_Klin1"
                elif "CO2 Klin no.2" in str(col):
                    column_mapping[col] = "CO2_Klin2"
                elif "CO2 >40mm K1K2" in str(col):
                    column_mapping[col] = "CO2_gt40mm"
                elif (
                    "<10" in str(col)
                    and "0-5" not in str(col)
                    and "5-10" not in str(col)
                ):
                    column_mapping[col] = "lt10_pct"
                elif "0-5" in str(col):
                    column_mapping[col] = "pct_0_5"
                elif "5-10" in str(col):
                    column_mapping[col] = "pct_5_10"
                elif "10-60" in str(col):
                    column_mapping[col] = "pct_10_60"
                elif ">60" in str(col):
                    column_mapping[col] = "pct_gt60"

            df_data = df_data.rename(columns=column_mapping)

            # اضافه کردن ستون‌های تاریخ
            df_data["SheetName"] = sheet_name
            df_data["ShamsiDate"] = shamsi_date.strftime("%Y/%m/%d")

            # تنظیم تاریخ برای ساعات 00:00 و 04:00 (روز بعد)
            def adjust_datetime(row):
                try:
                    time_str = str(row["Time"])
                    if not time_str or pd.isna(time_str):
                        return None

                    # ساخت datetime از تاریخ و زمان
                    hour, minute = map(int, time_str.split(':')[:2])

                    # ایجاد datetime شمسی
                    shamsi_dt = jdatetime.datetime(
                        shamsi_date.year,
                        shamsi_date.month,
                        shamsi_date.day,
                        hour,
                        minute,
                    )

                    # اگر زمان 00:00 یا 04:00 است، یک روز اضافه کنیم
                    if time_str in ["00:00", "00:00:00", "04:00", "04:00:00"]:
                        shamsi_dt += jdatetime.timedelta(days=1)

                    return shamsi_dt
                except Exception as e:
                    print(f"خطا در تنظیم تاریخ برای زمان {row.get('Time')}: {e}")
                    return None

            if "Time" in df_data.columns:
                df_data["ShamsiDateTime"] = df_data.apply(adjust_datetime, axis=1)
                # حذف ردیف‌هایی که تاریخ-زمان معتبر ندارند
                df_data = df_data[df_data["ShamsiDateTime"].notna()]
            else:
                df_data["ShamsiDateTime"] = None

            # تبدیل به تاریخ میلادی و تایم‌استمپ
            df_data["GregorianDateTime"] = df_data["ShamsiDateTime"].apply(
                lambda x: x.togregorian() if x else None
            )
            df_data["Timestamp"] = df_data["GregorianDateTime"].apply(
                lambda x: x.timestamp() if x else None
            )

            # فرمت‌دهی ستون‌های تاریخ
            df_data["ShamsiDateTime_Str"] = df_data["ShamsiDateTime"].apply(
                lambda x: x.strftime("%Y/%m/%d %H:%M") if x else None
            )
            df_data["GregorianDateTime_Str"] = df_data["GregorianDateTime"].apply(
                lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if x else None
            )

            # مرتب‌سازی بر اساس زمان
            if "Time" in df_data.columns:
                df_data = df_data.sort_values("Time")

            all_data.append(df_data)
            print(f"شیت {sheet_name}: {len(df_data)} ردیف استخراج شد")

        except Exception as e:
            print(f"خطا در پردازش شیت {sheet_name}: {e}")
            import traceback

            traceback.print_exc()
            continue

    # ترکیب داده‌های همه شیت‌ها
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # مرتب‌سازی بر اساس تایم‌استمپ
        if "Timestamp" in final_df.columns:
            final_df = final_df.sort_values("Timestamp").reset_index(drop=True)

        # انتخاب و مرتب‌سازی ستون‌های نهایی
        base_columns = [
            "SheetName",
            "ShamsiDate",
            "Time",
            "Timestamp",
            "ShamsiDateTime_Str",
            "GregorianDateTime_Str",
        ]

        data_columns = [
            "CO2_Klin1",
            "CO2_Klin2",
            "CO2_gt40mm",
            "lt10_pct",
            "pct_0_5",
            "pct_5_10",
            "pct_10_60",
            "pct_gt60",
        ]

        # فقط ستون‌های موجود را انتخاب کن
        final_columns = base_columns + [
            col for col in data_columns if col in final_df.columns
        ]
        final_df = final_df[final_columns]

        return final_df
    else:
        return pd.DataFrame()


# اجرای کد
if __name__ == "__main__":
    # مسیر فایل اکسل
    input_file = "daily.xlsx"
    output_file = "extracted_data_detailed.csv"

    print("در حال استخراج داده‌ها...")
    final_data = extract_daily_data_from_excel(input_file)

    if not final_data.empty:
        print(f"\nداده‌های استخراج شده ({len(final_data)} ردیف):")
        print("=" * 100)
        print(final_data.head(20).to_string())

        # ذخیره در فایل CSV
        final_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nداده‌ها در فایل '{output_file}' ذخیره شدند.")

        # نمایش آمار
        print("\nآمار داده‌های استخراج شده:")
        print("=" * 50)
        print(f"تعداد کل ردیف‌ها: {len(final_data)}")
        print(f"تعداد روزهای مختلف: {final_data['ShamsiDate'].nunique()}")

        if 'ShamsiDateTime_Str' in final_data.columns:
            print(
                f"بازه زمانی: از {final_data['ShamsiDateTime_Str'].min()} تا {final_data['ShamsiDateTime_Str'].max()}"
            )

        # نمایش ستون‌های موجود
        print("\nستون‌های موجود در خروجی:")
        for col in final_data.columns:
            non_null = final_data[col].count()
            dtype = final_data[col].dtype
            print(f"  {col}: {non_null} مقدار غیر خالی ({dtype})")

        # نمایش نمونه‌ای از زمان‌ها
        if 'Time' in final_data.columns:
            print(f"\nمقادیر منحصر به فرد Time: {final_data['Time'].unique()[:10]}")

    else:
        print("هیچ داده‌ای استخراج نشد.")
