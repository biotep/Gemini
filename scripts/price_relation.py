from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.layouts import column, row
import pandas as pd
from math import pi

class Price_relation:
    def __init__(self, data, t1_data, t2_data):
        self.source=ColumnDataSource()
        self.t1_source = ColumnDataSource()
        self.t2_source = ColumnDataSource()
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors', 'Ticker']])
        self.t1_source.data = self.t1_source.from_df(t1_data[['Open', 'High', 'Low', 'Close', 'Volume']])
        self.t2_source.data = self.t2_source.from_df(t2_data[['Open', 'High', 'Low', 'Close', 'Volume']])
        self.tools = 'pan,wheel_zoom,xbox_select,reset'

        #---------------------------------

        self.t1_data=t1_data

        self.t1_data_open = t1_data.Open.resample('W-FRI').first()
        self.t1_data_high = t1_data.High.resample('W-MON').max()
        self.t1_data_low = t1_data.Low.resample('W-MON').min()
        self.t1_data_close = t1_data.Close.resample('W-FRI').last().resample('W-MON').last()

        self.t1_df = pd.concat([self.t1_data_open, self.t1_data_high, self.t1_data_low, self.t1_data_close], axis=1)
        self.t1_df['date']=pd.to_datetime(self.t1_df.index)
        self.t1_df.columns = ['open', 'high', 'low', 'close', 'date']
        dec = self.t1_df.open > self.t1_df.close
        inc = self.t1_df.close > self.t1_df.open

        w = 12 * 60 * 60 * 1000  * 7 # half day in ms

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        print(self.t1_df.head(19))

        self.c1 = figure(x_axis_type="datetime", tools=TOOLS, plot_width=900, plot_height=300, title=data.keys()[0])
        self.c1.xaxis.major_label_orientation = pi / 4
        self.c1.grid.grid_line_alpha = 0.3

        self.c1.segment(self.t1_df.index, self.t1_df.high, self.t1_df.index, self.t1_df.low, color="black")
        self.c1.vbar(x=self.t1_df.index[inc], width=w, bottom=self.t1_df.open[inc],  top=self.t1_df.close[inc], fill_color="#37e57c", line_color="black")
        self.c1.vbar(x=self.t1_df.index[dec], width=w, bottom=self.t1_df.open[dec],  top=self.t1_df.close[dec], fill_color="#F2583E", line_color="black")


        #---------------------------------

        self.p = figure(plot_width=900, plot_height=300, tools=self.tools, x_axis_type="datetime", active_drag="xbox_select")
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
        self.p.line('date', 't1_normal', source=self.source, line_width=2, color='red', alpha=0.4, legend='Top')
        self.p.line('date', 't2_normal', source=self.source, line_width=2, color='blue', alpha=0.4, legend='Bottom')
        self.p.legend.location = "bottom_left"
        self.p.legend.click_policy = "hide"
        self.p.circle('date', 't1_normal', size=1.5, source=self.source, color=None, selection_color="green")
        self.p.circle('date', 't2_normal', size=1.5, source=self.source, color=None, selection_color="black")


        layout = column(self.p, self.c1)
        self.tab = Panel(child=layout, title='Price Relation')


    def update(self, data):
        print("Price relation updating...")
        print(data.head())
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors', 'Ticker']])
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
        self.p.legend[0].plot.legend[0].plot.legend[0]._property_values['items'][0].label['value'] = 'Marc'
