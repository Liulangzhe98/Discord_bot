import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authorize():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds_2.json", scope)
    client = gspread.authorize(creds)
    return client


def sheet_to_value(sheet_name, data_range):
    client = authorize()
    sheet = client.open("ItemVault").worksheet(sheet_name)
    cell_list = sheet.range(data_range)
    first = True
    values = []
    row = []
    row_index = -1
    for cell in cell_list:
        if first:
            row_index = cell.row
            row.append(cell.value)
            first = False
        elif row_index == cell.row:
            row.append(cell.value)
        elif cell != cell_list[-1]:
            values.append(row)
            row = []
            row_index = cell.row
            row.append(cell.value)
        if cell == cell_list[-1]:
            values.append(row)
    return values


def icy_epi_test():
    values = sheet_to_value('Summary', "H3:K10")
    table = ""
    if not values:
        print('No data found.')
    else:
        for row in values:
            if "total" not in row[0].lower():
                table += "{0:50}|{1:^5}|{2:^5}|{3:^8} \n".format(row[0], row[1], row[2], row[3])
            else:
                title = "The love potion is done for {0}.".format(row[3])
                table += "{0:62}|{1:^8}".format(row[0], row[3])
    return title, table


def kunlun_deco_gs(table_selection):
    sheet_name = re.split('[!]', table_selection)[0]
    sheet_range = re.split('[!]', table_selection)[1]

    values = sheet_to_value(sheet_name, sheet_range)
    table = ""
    if not values:
        print('No data found.')
    else:
        for row in values:
            table += "{0:42}|{1:>5} \n".format(row[0], row[2])
    note = "NOTE: Feather of Pheonix, Horn of Sacred Blue Dragon, Shell of Sacred Black Tortoise" \
           " or Skin of Silver Tiger will influence the looks of the deco."
    return table, note


def book_request_func(args):
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")
    sheet.insert_row(args, 2, "RAW")


def book_list_viewer():
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")

    row_count = len(sheet.col_values(1))
    table = ""
    for i in reversed(range(2, row_count+1)):
        row = sheet.row_values(i)
        table += "Index:{0:2}| {1:<15}|{2:^10}|{3:^10}| {4:40}| {5:3} \n".format(row_count+1-i, row[1], row[2], row[3], row[4], row[5])
    if table == "":
        table = "There are no book requests at this moment."
    return table


def book_remover_func(index_list):
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")
    row_count = len(sheet.col_values(1))
    book = ""
    for index in index_list:
        row = sheet.row_values(row_count+1-index)
        book += "{0:<15}|{1:^10}|{2:^10}| {3:40}| {4:3} \n".format(row[1], row[2], row[3], row[4], row[5])
        sheet.delete_row(row_count+1-index)
    return book
