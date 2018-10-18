from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slider, RangeSlider
from bokeh.layouts import column, row
import pandas as pd
import numpy as np

class Residual_model:
    def __init__(self, data):
        #self.source = ColumnDataSource(data=dict(Time=[], residual_ols=[],residual_tls=[], Beta=[], Alfa=[], STD=[], Z=[], Un=[], Ln=[], Ux=[], Lx=[]))
        self.source = ColumnDataSource()
        self.data = data
        self.LRperiod = 20
        self.STDperiod = 10
        self.EntryT = 2.5
        self.ExitT = -0.2
        self.tools = 'pan,wheel_zoom,xbox_select,reset'
        self.t1 = self.data.keys()[0]
        self.t2 = self.data.keys()[2]

        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient = linreg[0]
        self.intercept = linreg[1]
        self.resids = self.calculate_resid(data)
        self.data['resids']=self.resids
        #self.data=self.data.dropna()

        self.p1 = figure(plot_width=1100, plot_height=300, tools=self.tools, x_axis_type="datetime")
        self.source.data = ColumnDataSource.from_df(data[['Time', 'resids']])

        self.p1.title.text = 'Residual of prices: '+ self.t1 + ' and ' + self.t2
        self.p1.line('date', 'resids', source=self.source,  line_width=2, color='black', alpha=0.8)
        # self.p1.line('date', 'Un', source=self.source, line_width=1, color='green', alpha=0.5)
        # self.p1.line('date', 'Ln', source=self.source, line_width=1, color='blue', alpha=0.5)
        # self.p1.line('date', 'Ux', source=self.source, line_width=1, color='red', alpha=0.5)


        self.p1.legend.location = "bottom_left"
        self.p1.title.text = 'Residual of prices: ' + self.t1 + ' and ' + self.t2


        self.LR_slider = Slider(start=10, end=80, value=25, step=1, title='Experimental! Regresson Period', callback_policy = "mouseup", callback_throttle=1000)
        #self.LR_slider.callback_policy = "mouseup"
        self.LR_slider.on_change('value', self.LR_slider_callback)

        self.STD_slider = Slider(start=10, end=80, value=15, step=1, title='Standard Deviation')
        self.STD_slider.on_change('value', self.STD_slider_callback)
        self.update(self.data)

        layout = row(column(self.p1), column(self.LR_slider, self.STD_slider))

        self.tab = Panel(child=layout, title='Residual Model')

    def calculate_resid(self, data):
        slopes=[]
        intercepts=[]
        resids=[]
        res_indices=[]
        data_lines=data.t1.count()


        for r in range(0, (data_lines - self.LRperiod) + 1):
            c0 = data.t1[r:r+self.LRperiod]
            c1 = data.t2[r:r+self.LRperiod]
            slope, intercept = np.polyfit(c1,c0, 1)
            resid = (c0 - (slope * c1 + intercept))
            # slopes.append(slope)
            # intercepts.append(intercept)
            resids.append(resid[-1])
            res_indices.append(c0.index[-1])
        # slopes = pd.Series(slopes, index=res_indices)
        # intercepts = pd.Series(intercepts, index=res_indices)
        resids = pd.Series(resids, index=res_indices)
        standev = resids.rolling(self.STDperiod).std()
        zscore = resids / standev
        return zscore

    def LR_slider_callback(self, attr, old, new):
        self.LRperiod = new
        self.update(self.data)

    def STD_slider_callback(self, attr, old, new):
        self.STDperiod = new
        self.update(self.data)

    def update(self, data):
        #self.MAperiod = self.MA_slider.value

        #linreg = np.polyfit(data.t1, data.t2, 1)
        #self.gradient = linreg[0]
        #self.intercept = linreg[1]

        #data['LR'] = data.Ratio.rolling(window=self.LRperiod).mean()
        #data['STD'] = data.Ratio.rolling(window=self.STDperiod).std()
        #data['Z'] = (data.Ratio - data.MA) / data.STD
        #data['Un'] = data.MA + data.STD * self.EntryT
        #data['Ln'] = data.MA - data.STD * self.EntryT
        #data['Ux'] = data.MA + data.STD * self.ExitT
        #data['Lx'] = data.MA - data.STD * self.ExitT
        data['resids'] = self.calculate_resid(data)

        self.source.data = self.source.from_df(data[['Time',  'resids']])
        self.data = data
        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]

        self.p1.title.text = 'Ratio of prices: ' + self.t1 + ' and ' + self.t2