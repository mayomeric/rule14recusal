# READING PACKAGES
from __future__ import print_function
import apiclient
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

import json
import urllib.request
import pandas_bokeh



SPREADSHEET_ID = '1cgylzaHlX-v1KTTA7gxPO0-CbUT6FPqyDH93rqOgP9A'
RANGE_NAME = 'Sheet1'


# FUNCTIONS TO GET DATA FROM GOOGLE SPREADSHEET

def get_google_sheet(spreadsheet_id, range_name):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = apiclient.discovery.build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet


def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df


# GETTING DATA AND MAKING DATAFRAME

gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
df = gsheet2df(gsheet)

header_list = ['Date', 'Alderman', 'Bill_Number', 'Recusal_Reason', 'Subject', 'Title', 'Type_Of_Legislation']
df = df.reindex(columns = header_list)


# USING API AND APPENDING DATA

for index, row in df.iterrows():
    identifier = row['Bill_Number']
    api = 'https://ocd.datamade.us/bills/?identifier=' + identifier
    with urllib.request.urlopen(api) as url:
        data = json.loads(url.read().decode())

        subject = data['results'][0]['subject']
        title = data['results'][0]['title']
        classification = data['results'][0]['classification']

        df['Subject'][index] = subject
        df['Title'][index] = title
        df['Type_Of_Legislation'][index] = classification


df['Subject'] =  df['Subject'].map(lambda x: str(x)[:-2])
df['Subject'] =  df['Subject'].map(lambda x: str(x)[2:])

count = df.Subject.value_counts()
m = df.Subject.isin(count.index[count<3])
df.loc[m, 'Subject'] = 'Other'

# SAVING FILE
df.to_csv('database.csv', index = False)
