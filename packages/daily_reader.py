from excel_manager import ExcelManager
from safe_round import NumberRounder


class Daily:
    def __init__(self, file_name):
        self.file_name = file_name
        self.date = None
        self.weather = None
        self.CO2_AVG = None
        self.tonage = None
        self.truck = None
        self.par_10_avg = None
        self.par_5_avg = None
        self.par_0_avg = None
        self.par_1060_avg = None
        self.par_70_avg = None

    def extract_avg(self, sheet_name):
        excel = ExcelManager(filename=self.file_name)
        excel.load_workbook()
        excel.set_active_sheet(sheet_name)
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
        cell_data = excel.read_cells(cell_list)  # Pass cell_list to read_cells

        # Don't forget to close the Excel file
        excel.close()
        return cell_data

    def avg_data(self, sheet):
        avg_data = self.extract_avg(sheet_name=sheet)
        rounder = NumberRounder()
        # Assign to instance attributes
        # (
        #     self.date,
        #     self.weather,
        #     self.tonage,
        #     self.truck,
        #     self.CO2_AVG,
        #     self.par_10_avg,
        #     self.par_5_avg,
        #     self.par_0_avg,
        #     self.par_1060_avg,
        #     self.par_70_avg,
        # ) = avg_data

        return [
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

    def extract_bulk_avg(self, start_index, end_index):
        excel = ExcelManager(self.file_name)
        excel.load_workbook()  # Load workbook to get sheet names
        sheet_names = excel.sheet_names()
        excel.close()

        bulk_data = []
        for i in range(start_index - 1, end_index + 1):
            if i < len(sheet_names):
                # Call extract_avg for each sheet and collect results
                sheet_data = self.avg_data(sheet_names[i])
                bulk_data.append(sheet_data)

        return bulk_data


# how to use
# if __name__ == "__main__":
#     d = Daily(file_name="daily.xlsx")
#     print(d.extract_bulk_avg(1, 3))
