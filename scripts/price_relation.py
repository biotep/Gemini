from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.layouts import column, row

class Price_relation:
    def __init__(self, data):
        self.source=ColumnDataSource()
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors', 'Ticker']])
        self.tools = 'pan,wheel_zoom,xbox_select,reset'

        self.p = figure(plot_width=900, plot_height=300, tools=self.tools, x_axis_type="datetime", active_drag="xbox_select")
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
        self.p.line('date', 't1_normal', source=self.source, line_width=2, color='red', alpha=0.4, legend='Ticker')
        self.p.line('date', 't2_normal', source=self.source, line_width=2, color='blue', alpha=0.4, legend='Ticker')
        self.p.legend.location = "bottom_left"
        self.p.legend.click_policy = "hide"
        self.p.circle('date', 't1_normal', size=1.5, source=self.source, color=None, selection_color="green")
        self.p.circle('date', 't2_normal', size=1.5, source=self.source, color=None, selection_color="black")


        layout = row(self.p)
        self.tab = Panel(child=layout, title='Price Relation')


    def update(self, data):
        print("Price relation updating...")
        print(data.head())
        self.source.data = self.source.from_df(data[['t1', 't2', 't1_normal', 't2_normal', 'Time', 'Colors', 'Ticker']])
        self.p.title.text = 'Normalised prices: ' + data.keys()[0] + " and " + data.keys()[2]
