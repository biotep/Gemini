from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slope, PreText, Paragraph, Div
from bokeh.layouts import column, row
import numpy as np
import statsmodels.formula.api as sm
from statsmodels.tsa.stattools import coint
from scipy.odr import *

class Linreg:
    def __init__(self, data):
        self.source = ColumnDataSource(data=dict(date=[], Close=[], Norm=[], Time=[], Colors=[]))
        self.xcorrsouce= ColumnDataSource()
        self.xcorrsouce2 = ColumnDataSource()
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors']])

        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]

        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient_ols = linreg[0]
        self.intercept_ols = linreg[1]
        self.smols = sm.ols(formula="t2 ~ t1", data=data[['t1', 't2']]).fit()
        self.tls_out = self.tls(data.t1, data.t2)
        self.gradient_tls=self.tls_out.beta[0]
        self.intercept_tls = self.tls_out.beta[1]
        self.smols_summary=str(self.smols.summary(yname=self.t2, xname=['Intercept','Gradient'],  title=str("Ordinary least squares of " + self.t2 + " on " + self.t1)))
        self.tls_summary = "\n Total least squares: \n" + "slope: " + str(self.tls_out.beta[0]) + " intercept: " + str(self.tls_out.beta[1])

        self.tools = 'reset'

        self.p = figure(plot_width=450, plot_height=450, tools='reset')
        self.p.scatter(x='t1', y='t2', marker='asterisk', size=5, color='Colors', alpha=0.6,  source=self.source)
        self.p.circle('t1', 't2', size=2, source=self.source, selection_color="orange", alpha=0.2,  selection_alpha=0.2)

        self.slope_ols = Slope(gradient=self.gradient_ols, y_intercept=self.intercept_ols, line_color='green', line_dash='dashed', line_width=2.5)
        self.slope_tls = Slope(gradient=self.gradient_tls, y_intercept=self.intercept_tls, line_color='blue', line_dash='dashed', line_width=2.5)

        self.p.add_layout(self.slope_ols)
        self.p.add_layout(self.slope_tls)
        self.p.xaxis.axis_label = self.t1
        self.p.yaxis.axis_label = self.t2

        score, pvalue, _ = coint(data.t1, data.t2)
        self.cointext = "coint: " + str(pvalue)
        self.stats = PreText(text='', width=750)

        corrcoeff = np.corrcoef(data.t1, data.t2)[0][1]
        self.filedatetext1 = data.t1.index[:1][0].__str__().split()[0]
        self.filedatetext2 = data.t2.index[:1][0].__str__().split()[0]
        if self.filedatetext1 != self.filedatetext2:
            self.filedatetext3 = " File enddate diff!"
        else:
            self.filedatetext3 = " OK"


        #self.stats.text = str(data[[self.t1, self.t2, self.t1 + '_normal', self.t2 + '_normal']].describe()) + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff)
        self.stats.text = self.smols_summary + "\n" + self.tls_summary + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff) + "\n" + self.cointext
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

        layout = row(column(self.p,self.h),self.stats)
        self.tab = Panel(child=layout, title='Linear Regression')

    def tls(self, x, y):
        def linear_func(p, x):
            m, c = p
            return m * x + c

        # Create a model for fitting.
        linear_model = Model(linear_func)

        # Create a RealData object using our initiated data from above.
        data = RealData(x, y)

        # Set up ODR with the model and data.
        odr = ODR(data, linear_model, beta0=[0., 1.])

        # Run the regression.
        out = odr.run()
        return out



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

        self.smols = sm.ols(formula="t2 ~ t1", data=data[['t1', 't2']]).fit()
        self.tls_out = self.tls(data.t1, data.t2)
        #for cointegration
        score, pvalue, _ = coint(data.t1, data.t2)
        self.cointext = "coint: " + str(pvalue)
        print("self.cointext", self.cointext)

        self.smols_summary=str(self.smols.summary(yname=self.t2, xname=['Intercept','Gradient'], title=str("Ordinary least squares of " + self.t2 + " on " + self.t1)))
        self.tls_summary = "\n Total least squares: \n" + "slope: " + str(self.tls_out.beta[0]) + " intercept: " + str(self.tls_out.beta[1])
        self.stats.text = self.smols_summary + "\n" + self.tls_summary + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff) + "\n" + self.cointext


        self.filedatetext1 = data.t1.index[:1][0].__str__().split()[0]
        self.filedatetext2 = data.t2.index[:1][0].__str__().split()[0]
        if self.filedatetext1 != self.filedatetext2:
            self.filedatetext3 = " File enddate diff!"
        else:
            self.filedatetext3 = " OK"

        self.stats.text = self.smols_summary + "\n" + self.tls_summary + "\nEOF    " + self.filedatetext1 +"   " + self.filedatetext2 + self.filedatetext3 + "\ncorrelation : " + str(corrcoeff) + "\n" + self.cointext

        self.p.xaxis.axis_label = self.t1
        self.p.yaxis.axis_label = self.t2
        #Slope update
        linreg = np.polyfit(data.t1, data.t2, 1)
        self.gradient_ols = linreg[0]
        self.intercept_ols = linreg[1]
        self.slope_ols.gradient = self.gradient_ols
        self.slope_ols.y_intercept = self.intercept_ols
        self.gradient_tls=self.tls_out.beta[0]
        self.intercept_tls = self.tls_out.beta[1]
        self.slope_tls.gradient = self.gradient_tls
        self.slope_tls.y_intercept = self.intercept_tls

