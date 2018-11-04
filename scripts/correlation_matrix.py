from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slope, PreText
from bokeh.layouts import column, row
import numpy as np
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import transform
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup

class Correlation_matrix:
    def __init__(self, corr_data):

        self.matrix_data = pd.DataFrame(np.round(np.corrcoef(corr_data, rowvar=0),2), columns=corr_data.columns, index=corr_data.columns.values)

        self.matrix_data.columns.name = 'B'
        self.matrix_data.index.name = 'A'

        print(self.matrix_data)

        self.matrix_data = self.matrix_data.stack().rename("value").reset_index()
        #self.matrix_data.to_pickle("/Users/Uriel/Documents/Python/Ibis/Gemini/matrix_data.pkl")

        #create plot
        colors = ['#a50026','#d73027','#f46d43','#fdae61','#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837']
        mapper = LinearColorMapper(palette=colors, low=-1, high=1)
        colors2 = colors[::-1]

        self.p = figure(plot_width=600, plot_height=600, title="My plot", x_range=list(self.matrix_data.A.drop_duplicates()),y_range=list(self.matrix_data.B.drop_duplicates())[::-1], toolbar_location=None, tools="hover", tooltips=[('coef:', '@value')], x_axis_location="above")

        self.p.rect(
            x="A",
            y="B",
            width=1,
            height=1,
            source=ColumnDataSource(self.matrix_data),
            line_color=None,
            fill_color=transform('value', mapper))

        self.p.text(
            x="A",
            y="B",
            text=str("value"),
            source=ColumnDataSource(self.matrix_data),
            text_color='black',
            text_font_size='8pt',
            x_offset=-15,
            text_align="left")

        color_bar = ColorBar(
            color_mapper=mapper,
            location=(0, 0),
            ticker=BasicTicker(desired_num_ticks=len(colors)))

        def checkbox_group_callback(attr, old, new):
            print(corr_data.columns[new])

        self.checkbox_group = CheckboxGroup(
            labels=list(corr_data.columns), active=[0, 1])

        #show(widgetbox(checkbox_group))
        self.checkbox_group.on_change('active', checkbox_group_callback)

        self.p.add_layout(color_bar, 'right')

        layout = row(self.p, widgetbox(self.checkbox_group))

        self.tab = Panel(child=layout, title='Correlation Matrix')

    def update(self, data):
        pass