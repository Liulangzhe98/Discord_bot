import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def main():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds_2.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("ItemVault").worksheet("Book Requests Discord")

    # Textual day, month and year
    args = "[Tyr] Shaolin CK Spirit of the Bright King C11"
    date = datetime.today().strftime("%d %B, %Y")

    name = args.split(" ")[0]
    clan = args.split(" ")[1]
    group = args.split(" ")[2]
    cheng = args[-3:]
    book = " ".join(args.split(" ")[3:][:len(cheng) + 1])

    # Check if filled in correctly
    if clan in ["Wu-Tang", "Beggar", "Shaolin"]:
        if group in ["Warrior", "Healer", "Hybrid", "CK"]:
            if len(book) != 0:
                if "C1" in cheng:

                    request_list = [date, name, clan, group, book, cheng]
                    #book_request("'Book Requests Discord'", request_list)

                    # sheet.insert_row(request_list, 2)

                    print(f"{request_list}")
                else:
                    print("WRONG LEVEL")
            else:
                print("YOU FORGOT YOUR BOOK")
        else:
            print("Use the right version of the classes")
    else:
        print("WRONG CLAN")


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
                title = "Nuria's love potion {0} completed.".format(row[3])
                table += "{0:62}|{1:^8}".format(row[0], row[3])
    return title, table


def kunlun_deco(table_selection):
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
    print(table)
    return table, note


def book_request(args):
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")
    sheet.insert_row(args, 2, "RAW")


def book_list_viewer():
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")

    row_count = len(sheet.col_values(1))
    table = ""
    for i in range(2, row_count+1):
        row = sheet.row_values(i)
        table += "Index:{0:2}| {1:<15}|{2:^10}|{3:^10}| {4:45}| {5:3} \n".format(i-1, row[1], row[2], row[3], row[4], row[5])
    if table == "":
        table = "There are no book requests at this moment."
    print(table)
    return table

def book_remover_func(index):
    client = authorize()
    sheet = client.open("ItemVault").worksheet("Book Requests Discord")
    sheet.delete_row(index+1)

    print("removed")





if __name__ == "__main__":
    main()
