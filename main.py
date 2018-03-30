from xlrd import open_workbook

# Two arrays, deliveries and trucks
# Sort deliveries by decreasing deadline and weight
# Sort trucks by decreasing weight

exportFile = './data/EXP Feb 2018.xlsx'
importFile = './data/IMP POD List Feb 2018.xlsx'
export_items = []
import_items = []

def fetch_data():
    # Get export items
    wb = open_workbook(exportFile)
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):
            values = []
            for col in range(number_of_columns):
                value = (sheet.cell(row, col).value)
                values.append(value)
                export_items.append(values)

    # Get import items
    wb = open_workbook(importFile)
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):
            values = []
            for col in range(number_of_columns):
                value = (sheet.cell(row, col).value)
                values.append(value)
                import_items.append(values)

    print(export_items)
    print(import_items)

def parse_data():
    fetch_data()

# Data Pre-processing
parse_data()


# deliveries =
# n = len(s)
# a = []
# k = 0
# for m in range(1, n):
#     if s[m] >= f[k]:
#         a.append(m)
#         k = m
# return a