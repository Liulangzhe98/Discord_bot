from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1XrDVjvpsRsCMRwoelZAyqkuaVqS0z2S9Zz-bnsE_J5o'


def authenticate(Range):
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=Range).execute()
    return result


def icy_epi_test():
    result = authenticate('Summary!H3:K10')

    values = result.get('values', [])
    table = ""
    if not values:
        print('No data found.')
    else:
        print('Values:')
        for row in values:
            if "total" not in row[0].lower():
                table += "{0:50}|{1:^5}|{2:^5}|{3:^8} \n".format(row[0], row[1], row[2], row[3])
            else:
                title = "Nuria's love potion {0} completed.".format(row[3])
                table += "{0:62}|{1:^8}".format(row[0], row[3])

    print(table)
    return title, table


def kunlun_deco(RANGE):
    result = authenticate(RANGE)

    values = result.get('values', [])
    table = ""
    if not values:
        print('No data found.')
    else:
        print('Values:')
        for row in values:
            table += "{0:42}|{1:>5} \n".format(row[0], row[2])
    note = "NOTE: Feather of Pheonix, Horn of Sacred Blue Dragon, Shell of Sacred Black Tortoise" \
           " or Skin of Silver Tiger will influence the looks of the deco."
    return table, note


def main():
    icy_epi_test()


if __name__ == '__main__':
    main()
