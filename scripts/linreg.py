from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slope, PreText, Paragraph, Div
from bokeh.layouts import column, row
import numpy as np

class Linreg:
    def __init__(self, data):
        self.source = ColumnDataSource(data=dict(date=[], Close=[], Norm=[], Time=[], Colors=[]))
        self.xcorrsouce= ColumnDataSource()
        self.xcorrsouce2 = ColumnDataSource()
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
        corrcoeff = np.corrcoef(data.t1, data.t2)[0][1]
        self.filedatetext1 = data.t1.index[:1][0].__str__().split()[0]
        self.filedatetext2 = data.t2.index[:1][0].__str__().split()[0]
        if self.filedatetext1 != self.filedatetext2:
            self.filedatetext3 = " File enddate diff!"
        else:
            self.filedatetext3 = " OK"


        self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe()) + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff)
        self.p.grid.grid_line_color = None
        self.p.background_fill_color = "#eedddd"

        self.h = figure(title="Cross Correlation", background_fill_color="#E8DDCB", plot_height=250, plot_width=480, y_range=(-1, 1))
        lags, ccor = self.crosscorr(data.t1, data.t2)
        self.xcorrsouce2.data = {'lags': lags, 'ccor':ccor}
        self.verticalLine = Slope(gradient=1, y_intercept=0, line_color='black', line_dash='dashed',line_width=1.5)
        self.h.add_layout(self.verticalLine)

        hist, edges = np.histogram(ccor, density=True, bins=50)
        self.xcorrsouce.data = {'hist': hist, 'left': edges[:-1], 'right':edges[1:]}

        #self.h.quad(top='hist', bottom=0, left='left', right='right', fill_color="#036564", line_color="#033649", source = self.xcorrsouce)
        self.h.line('lags', 'ccor', source=self.xcorrsouce2, line_width=2, color='red', alpha=0.4)
        self.h.ygrid.band_fill_alpha = 0.1
        self.h.ygrid.band_fill_color = "navy"

        layout = row(self.p, column(self.stats, self.h))
        self.tab = Panel(child=layout, title='Linear Regression')

    def crosscorr(self, x, y):
        npts = x.count()
        lags = np.arange(-npts + 1, npts)
        ccov = np.correlate(x - x.mean(), y - y.mean(), mode='full')
        ccor = ccov / (npts * x.std() * y.std())
        return lags, ccor


    def update(self, data):
        print("linreg updating...")
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors']])

        crosscorr = np.correlate(data.t1, data.t2, "full")
        hist, edges = np.histogram(crosscorr, density=True, bins=50)
        self.xcorrsouce.data = {'hist': hist, 'left': edges[:-1], 'right':edges[1:]}
        lags, ccor = self.crosscorr(data.t1, data.t2)
        self.xcorrsouce2.data = {'lags': lags, 'ccor':ccor}


        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]
        corrcoeff = np.corrcoef(data.t1, data.t2)[0][1]

        self.filedatetext1 = data.t1.index[:1][0].__str__().split()[0]
        self.filedatetext2 = data.t2.index[:1][0].__str__().split()[0]
        if self.filedatetext1 != self.filedatetext2:
            self.filedatetext3 = " File enddate diff!"
        else:
            self.filedatetext3 = " OK"

        self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe()) + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff)
        #self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe()) + "\ncorrelation : " + str(corrcoeff)
        self.p.xaxis.axis_label = self.t1
        self.p.yaxis.axis_label = self.t2
        #Slope update
        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient = linreg[0]
        self.intercept = linreg[1]
        self.slope.gradient = self.gradient
        self.slope.y_intercept = self.intercept
        #self.slope = Slope(gradient=self.gradient, y_intercept=self.intercept, line_color='green', line_dash='dashed', line_width=3.5)


