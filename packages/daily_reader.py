from excel_manager import ExcelManager
from jalali_convertor import Jalali
from safe_round import NumberRounder


def extract_avg(sheetname: str, filename="daily.xlsx"):
    excel = ExcelManager(filename)
    try:
        excel.load_workbook()
        excel.set_active_sheet(sheetname)
        cell_list = [
            "E4",  # date
            "H4",  # weather
            "A9",  # tonage
            "B9",  # truck
            "D9",  # CO2_avg
            "F9",  # par_10_avg
            "F10",  # par_5_avg
            "G10",  # par_0_avg
            "H9",  # par_1060_avg
            "K9",  # par_70_avg
        ]
        avg_data = excel.read_cells(cell_list)
        rounder = NumberRounder()
        jalal = Jalali()
        avg_data_clean = [
            jalal(date=str(avg_data[0]), time="8:00"),
            avg_data[0],  # date
            avg_data[1],  # weather
            rounder(avg_data[2]),  # tonage
            avg_data[3],  # truck
            rounder(avg_data[4]),  # CO2_avg
            rounder(avg_data[5]),  # par_10_avg
            rounder(avg_data[6]),  # par_5_avg
            rounder(avg_data[7]),  # par_0_avg
            rounder(avg_data[8]),  # par_1060_avg
            rounder(avg_data[9]),  # par_70_avg
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
#     d = extract_avg(filename="daily.xlsx", sheetname="04")
#     print(d)


# extract bulk mode
# if __name__ == "__main__":
#     print(extract_bulk_avg(start_index=1, end_index=3))
