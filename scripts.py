from bokeh.plotting import figure, output_file, save
import pandas_bokeh
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn


df = pd.read_csv ('database.csv')


# CHART 1: RECUSALS BY DATE; CLICK ON ALDERMAN
output_file('recusals_by_date.html', mode='inline')

recusals_df = df.groupby(( "Date", "Alderman")).size().to_frame().reset_index()
recusals_df.rename(columns={0:"num_recusals"}, inplace=True)
recusals_df = recusals_df.pivot("Date", "Alderman", "num_recusals")
recusals_df = recusals_df.fillna(0)


chart1 = recusals_df.plot_bokeh.bar(
    figsize =  (1300, 750),
    ylabel = "Number of Recusals",
    title = "Recusals by Date",
    alpha = 1)



save(chart1)



# CHART 2: ALDERMAN BY TYPE OF RECUSAL

output_file('recusals_by_reason.html', mode='inline')

recusals_df = df.groupby(( "Alderman", "Recusal_Reason")).size().to_frame().reset_index()
recusals_df.rename(columns={0:"num_recusals"}, inplace=True)
recusals_df = recusals_df.pivot( "Alderman", "Recusal_Reason", "num_recusals")
recusals_df = recusals_df.fillna(0)


chart2 = recusals_df.plot_bokeh.bar(
    figsize =  (1300, 750),
    ylabel = "Number of Recusals",
    title = "Recusals by Reason",
    alpha = 1)



save(chart2)


# CHART 3: RECUSALS BY SUBJECT; CLICK ON Subject

output_file('recusals_by_subject.html', mode='inline')

recusals_df = df.groupby(("Alderman", "Subject")).size().to_frame().reset_index()
recusals_df.rename(columns={0:"num_recusals"}, inplace=True)
recusals_df = recusals_df.pivot("Alderman","Subject", "num_recusals")
recusals_df = recusals_df.fillna(0)


chart3 = recusals_df.plot_bokeh.bar(
    figsize =  (1300, 750),
    ylabel = "Number of Recusals",
    title = "Recusals by Subject",
    alpha = 1)


save(chart3)


# CHART 4: DATA TABLE

output_file('data_table.html', mode='inline')
source = ColumnDataSource(df)

columns = [
        TableColumn(field="Date", title="Date"),
        TableColumn(field="Alderman", title="Alderman"),
        TableColumn(field="Bill_Number", title="Bill Number"),
        TableColumn(field="Recusal_Reason", title= "Reason for Recusal"),
        TableColumn(field="Subject", title = "Topic"),
        TableColumn(field="Title", title = "Bill Title"),
    ]
data_table = DataTable(source=source, columns=columns, width=1400, height=1000)



save(data_table)
