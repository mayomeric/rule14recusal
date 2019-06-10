from datetime import date
from random import randint
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

output_file("data_table.html")
df = pd.read_csv('database.csv')
#data = dict(
        #dates=[date(2014, 3, i+1) for i in range(10)],
        #downloads=[randint(0, 100) for i in range(10)],
    #)
source = ColumnDataSource(df)

columns = [
        TableColumn(field="Date", title="Date"),
        TableColumn(field="Alderman", title="Alderman"),
        TableColumn(field="Bill_Number", title="Bill Number"),
        TableColumn(field="Recusal_Reason", title= "Reason for Recusal"),
        TableColumn(field="Subject", title = "Topic"),
        TableColumn(field="Title", title = "Bill Title"),
    ]
data_table = DataTable(source=source, columns=columns, width=4000, height=2800)

show(data_table)
