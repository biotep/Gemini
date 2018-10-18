from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slider, RangeSlider, Span
from bokeh.layouts import column, row
import pandas as pd
import numpy as np

class Residual_model:
    def __init__(self, data):
        #self.source = ColumnDataSource(data=dict(Time=[], residual_ols=[],residual_tls=[], Beta=[], Alfa=[], STD=[], Z=[], Un=[], Ln=[], Ux=[], Lx=[]))
        self.source = ColumnDataSource()
        self.data = data
        self.LRperiod = 20
        self.EntryT = 2.5
        self.ExitT = 0.0
        self.tools = 'reset'
        self.t1 = self.data.keys()[0]
        self.t2 = self.data.keys()[2]

        self.isLRperiodChanged = True

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
        self.p1.line('date', 'Un', source=self.source, line_width=1, color='green', alpha=0.8)
        self.p1.line('date', 'Ln', source=self.source, line_width=1, color='blue', alpha=0.8)
        self.p1.line('date', 'Ux', source=self.source, line_width=1, color='brown', alpha=0.8)
        self.p1.line('date', 'Lx', source=self.source, line_width=1, color='pink', alpha=0.8)




        self.p1.legend.location = "bottom_left"
        self.p1.title.text = 'Residual of prices: ' + self.t1 + ' and ' + self.t2


        self.LR_slider = Slider(start=10, end=80, value=25, step=1, title='Experimental! Regresson Period', callback_policy = "mouseup", callback_throttle=1000)
        self.Entry_slider = Slider(start=1.0, end=5.0, value=2.0, step=0.1, title='Entry Treshold')
        self.Exit_slider = Slider(start=0.0, end=1.5, value=0.0, step=0.1, title='Exit Treshold')
        self.Entry_slider.on_change('value', self.Entry_slider_callback)
        self.Exit_slider.on_change('value', self.Exit_slider_callback)
        self.LR_slider.on_change('value', self.LR_slider_callback)
        self.update(self.data)

        layout = row(column(self.p1), column(self.LR_slider, self.Entry_slider, self.Exit_slider))

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
        indices = []
        stds = []

        for r in range(0, (resids.count() - self.LRperiod) + 1):
            r0 = resids[r:r + self.LRperiod]

            std = np.std(r0)
            stds.append(std)
            indices.append(r0.index[-1])

        stds = pd.Series(stds, index=indices)
        zscore = (resids / stds)
        zscore.dropna(inplace=True)


        return zscore

    def LR_slider_callback(self, attr, old, new):
        self.LRperiod = new
        self.isLRperiodChanged = True
        self.update(self.data)

    def Entry_slider_callback(self, attr, old, new):
        self.EntryT = new
        self.update(self.data)

    def Exit_slider_callback(self, attr, old, new):
        self.ExitT = new
        self.update(self.data)

    # def check_trade(self):
    #     isPosition=False
    #     self.data['buy'] =



    def update(self, data):
        data['Un'] = self.EntryT
        data['Ln'] = self.EntryT * -1
        data['Ux'] = self.ExitT
        data['Lx'] = self.ExitT * -1

        if self.isLRperiodChanged:
            data['resids'] = self.calculate_resid(data)
            self.isLRperiodChanged = False

        self.source.data = self.source.from_df(data[['Time',  'resids', 'Un', 'Ln', 'Ux', 'Lx']])
        self.data = data
        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]

        self.p1.title.text = 'Ratio of prices: ' + self.t1 + ' and ' + self.t2
