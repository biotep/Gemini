from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.layouts import column, row
import pandas as pd
from math import pi
import numpy as np

class Price_relation:
    #def __init__(self, data, t1_data, t2_data):
    def __init__(self, data):
        self.source=ColumnDataSource()
        self.t1_source = ColumnDataSource()
        self.t2_source = ColumnDataSource()
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'residual_ols','residual_tls', 'Time', 'Colors', 'Ticker']])

        self.tools = 'pan,wheel_zoom,xbox_select,reset'

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        #---------------------------------

        self.p = figure(plot_width=900, plot_height=300, tools=self.tools, x_axis_type="datetime", active_drag="xbox_select")
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
        self.p.line('date', 't1_normal', source=self.source, line_width=2, color='red', alpha=0.4)
        self.p.line('date', 't2_normal', source=self.source, line_width=2, color='blue', alpha=0.4)
        self.p.legend.location = "bottom_left"
        self.p.legend.click_policy = "hide"
        self.p.circle('date', 't1_normal', size=1.5, source=self.source, color=None, selection_color="green")
        self.p.circle('date', 't2_normal', size=1.5, source=self.source, color=None, selection_color="black")

        #--------------------------------------------------------------

        self.r1 = figure(x_axis_type="datetime", tools=TOOLS, plot_width=900, plot_height=300, title=data.keys()[0])
        self.r1.title.text = 'Residuals of lineal regression of ' + data.keys()[0] + " and " + data.keys()[2]
        self.r1.line('date', 'residual_ols', source=self.source, line_width=2, color='green', alpha=0.4, legend='ols')
        self.r1.line('date', 'residual_tls', source=self.source, line_width=2, color='blue', alpha=0.4, legend='tls')
        self.r1.legend.location = "bottom_left"
        self.r1.legend.click_policy = "hide"

        layout = column(self.p, self.r1)
        self.tab = Panel(child=layout, title='Price Relation')


    def update(self, data):
        print("Price relation updating...")
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'residual_ols','residual_tls', 'Time', 'Colors', 'Ticker']])
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
        self.r1.title.text = 'OLS and TLS Residuals of ' + data.keys()[0] + " and " + data.keys()[2]
