from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slider, RangeSlider
from bokeh.layouts import column, row

class Ratio_model:
    def __init__(self, data):
        self.source = ColumnDataSource(data=dict(Time=[], Ratio=[], MA=[], STD=[], Z=[], Un=[], Ln=[], Ux=[], Lx=[]))
        self.data = data
        self.MAperiod = 25
        self.STDperiod = 10
        self.EntryT = 2.5
        self.ExitT = -0.2
        self.tools = 'pan,wheel_zoom,xbox_select,reset'
        self.t1 = self.data.keys()[0]
        self.t2 = self.data.keys()[2]


        self.p1 = figure(plot_width=900, plot_height=300, tools=self.tools, x_axis_type="datetime")
        self.p2 = figure(plot_width=900, plot_height=300, tools=self.tools, x_axis_type="datetime")

        self.p1.title.text = 'Ratio of prices: '+ self.t1 + ' and ' + self.t2
        self.p1.line('date', 'Ratio', source=self.source,  line_width=2, color='black', alpha=0.8)
        self.p1.line('date', 'Un', source=self.source, line_width=1, color='green', alpha=0.5)
        self.p1.line('date', 'Ln', source=self.source, line_width=1, color='blue', alpha=0.5)
        self.p1.line('date', 'Ux', source=self.source, line_width=1, color='red', alpha=0.5)


        self.p1.legend.location = "bottom_left"
        self.p1.title.text = 'Ratio of prices: ' + self.t1 + ' and ' + self.t2


        self.MA_slider = Slider(start=10, end=80, value=25, step=1, title='Moving Average')
        self.MA_slider.on_change('value', self.MA_slider_callback)
        self.STD_slider = Slider(start=10, end=80, value=15, step=1, title='Standard Deviation')
        self.STD_slider.on_change('value', self.STD_slider_callback)
        self.update(self.data)

        layout = row(column(self.MA_slider, self.STD_slider), self.p1, self.p2)
        self.tab = Panel(child=layout, title='Ratio Model')

    def MA_slider_callback(self, attr, old, new):
        self.MAperiod = new
        self.update(self.data)

    def STD_slider_callback(self, attr, old, new):
        self.STDperiod = new
        self.update(self.data)

    def update(self, data):
        print("ratio model updating...")
        #self.MAperiod = self.MA_slider.value

        data['Ratio'] = data.t1 / data.t2
        data['MA'] = data.Ratio.rolling(window=self.MAperiod).mean()
        data['STD'] = data.Ratio.rolling(window=self.STDperiod).std()
        data['Z'] = (data.Ratio - data.MA) / data.STD
        data['Un'] = data.MA + data.STD * self.EntryT
        data['Ln'] = data.MA - data.STD * self.EntryT
        data['Ux'] = data.MA + data.STD * self.ExitT
        data['Lx'] = data.MA - data.STD * self.ExitT

        self.source.data = self.source.from_df(data[['Time', 'Ratio', 'MA', 'STD', 'Z', 'Un', 'Ln', 'Ux', 'Lx']])
        self.data = data
        self.t1 = data.keys()[0]
        self.t2 = data.keys()[2]

        self.p1.title.text = 'Ratio of prices: ' + self.t1 + ' and ' + self.t2