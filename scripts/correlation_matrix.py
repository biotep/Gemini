from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Slope, PreText
from bokeh.layouts import column, row
import numpy as np

class Correlation_matrix:
    def __init__(self, corr_data):
        layout = column(self.p)
        self.tab = Panel(child=layout, title='Price Relation')