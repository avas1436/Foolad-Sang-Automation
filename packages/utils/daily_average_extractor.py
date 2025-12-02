from safe_round import NumberRounder

from packages.utils.excel_manager import ExcelManager
from packages.utils.jalali_convertor import Jalali


def extract_avg(sheetname: str, filename="daily.xlsx"):
    excel = ExcelManager(filename)
    try:
        excel.load_workbook()
        excel.set_active_sheet(sheetname)
        cell_list = [
            "E4",  # date   0
            "H4",  # weather  1
            "A9",  # tonage  2
            "B9",  # truck   3
            "D9",  # CO2_avg  4
            "F13",  # CO2_8_up40  5
            "F15",  # CO2_10_up40  6
            "F17",  # CO2_12_up40  7
            "F19",  # CO2_14_up40g  8
            "F9",  # par_10_avg   9
            "F10",  # par_0_avg  10
            "G10",  # par_5_avg  11
            "H9",  # par_1060_avg  12
            "K9",  # par_70_avg  13
        ]
        avg_data = excel.read_cells(cell_list)
        rounder = NumberRounder()
        jalal = Jalali()
        up40 = [avg_data[5], avg_data[6], avg_data[7], avg_data[8]]
        total = 0
        count = 0
        for i in up40:
            if isinstance(i, (int, float)):
                total += i
                count += 1

        avg = str(total / count) if count > 0 else None

        avg_data_clean = [
            jalal(date=str(avg_data[0]), time="8:00"),  # timestamp
            avg_data[0],  # date
            avg_data[1],  # weather
            rounder(avg_data[2]),  # tonage
            avg_data[3],  # truck
            rounder(avg_data[4]),  # CO2_avg
            rounder(avg),  # CO2_Upper40
            rounder(avg_data[9]),  # par_10_avg
            rounder(avg_data[10]),  # par_0_avg
            rounder(avg_data[11]),  # par_5_avg
            rounder(avg_data[12]),  # par_60_avg
            rounder(avg_data[13]),  # par_70_avg
        ]

        return avg_data_clean

    finally:
        excel.close()


def extract_bulk_avg(start_index: int, end_index: int, filename="daily.xlsx"):
    excel = ExcelManager(filename)
    try:
        excel.load_workbook()  # Load workbook to get sheet names
        sheet_names = excel.sheet_names()
    finally:
        excel.close()

    bulk_data = []
    for i in range(start_index - 1, end_index):
        if i < len(sheet_names):
            # Call extract_avg for each sheet and collect results
            sheet_data = extract_avg(sheet_names[i])
            bulk_data.append(sheet_data)

    return bulk_data


# how to use
## extract one day
# if __name__ == "__main__":
#     d = extract_avg(sheetname="27")
#     print(d)


# extract bulk mode
# if __name__ == "__main__":
#     print(extract_bulk_avg(start_index=1, end_index=3))
