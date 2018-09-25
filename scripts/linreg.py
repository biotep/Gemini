from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slope, PreText
from bokeh.layouts import column, row
import numpy as np

class Linreg:
    def __init__(self, data):
        self.source = ColumnDataSource(data=dict(date=[], Close=[], Norm=[], Time=[], Colors=[]))
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors']])
        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]
        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient = linreg[0]
        self.intercept = linreg[1]

        self.tools = 'pan,wheel_zoom,xbox_select,reset'

        self.p = figure(plot_width=550, plot_height=550, tools='pan,wheel_zoom,box_select,reset')
        self.p.scatter(x='t1', y='t2', marker='asterisk', size=5, color='Colors', alpha=0.6,  source=self.source)
        self.p.circle('t1', 't2', size=2, source=self.source, selection_color="orange", alpha=0.2,  selection_alpha=0.2)

        self.slope = Slope(gradient=self.gradient, y_intercept=self.intercept, line_color='green', line_dash='dashed', line_width=3.5)
        self.p.add_layout(self.slope)
        self.p.xaxis.axis_label = self.t1
        self.p.yaxis.axis_label = self.t2
        self.stats = PreText(text='', width=500)
        self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe())
        self.p.grid.grid_line_color = None
        self.p.background_fill_color = "#eedddd"
        layout = row(self.p, self.stats)
        self.tab = Panel(child=layout, title='Linear Regression')

    def update(self, data):
        print("linreg updating...")
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors']])
        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]
        self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe())
        self.p.xaxis.axis_label = self.t1
        self.p.yaxis.axis_label = self.t2
        #Slope update
        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient = linreg[0]
        self.intercept = linreg[1]
        self.slope.gradient = self.gradient
        self.slope.y_intercept = self.intercept
        #self.slope = Slope(gradient=self.gradient, y_intercept=self.intercept, line_color='green', line_dash='dashed', line_width=3.5)


