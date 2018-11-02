from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import  Select, TextInput, Button, Div, RadioButtonGroup, Paragraph, Tabs, TableColumn, DataTable, DateFormatter, PreText
import bokeh.palettes as bk_pal
import configparser
import time
from ib_insync import *
import asyncio
import numpy as np
import pandas as pd
import os
import os.path
from bs4 import BeautifulSoup
import getpass
import statsmodels.formula.api as sm
from scipy.odr import *

from scripts.linreg import Linreg
from scripts.price_relation import Price_relation
from scripts.ratio_model import Ratio_model
from scripts.residual_model import Residual_model
from scripts.correlation_matrix import Correlation_matrix



from pathlib import Path
home = str(Path.home())

username = getpass.getuser()
config = configparser.ConfigParser()
configFile = home + '/Documents/Python/Ibis/config.ini'

config.read(configFile)
history_dir = config['History directory']['history_dir']
history_root = config['History directory']['history_dir']
server = config['Server']['server_document']
catalog_file = history_root+"catalog.csv"
ib_server = config['IB']['IB_Server']
ib_port = config['IB']['IB_Port']


class Gemini:
    def __init__(self):
        self.TIMEFRAME = 'Daily'
        self.history_dir = history_dir + self.TIMEFRAME + "/"
        if os.path.isfile(catalog_file):
            self.catalog = pd.read_csv(catalog_file)
        elif not os.path.isfile(catalog_file):
            self.catalog = pd.DataFrame(columns=['STOCK', 'COMPANY', 'INDUSTRY', 'MARKETCAP', 'EBIDTA'])
            self.catalog.to_csv(catalog_file)

        self.DEFAULT_TICKERS = self.collect_downloaded_symbols()
        self.view_setup()

    def tickerInfoTextSetup(self):
        ticker1 = self.ticker1.value
        ticker2 = self.ticker2.value

        company_name1 = self.catalog.loc[self.catalog.STOCK.isin([ticker1])][['COMPANY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        industry1 = self.catalog.loc[self.catalog.STOCK.isin([ticker1])][['INDUSTRY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        marketcap1 = self.catalog.loc[self.catalog.STOCK.isin([ticker1])][['MARKETCAP']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        ebidta1 = self.catalog.loc[self.catalog.STOCK.isin([ticker1])][['EBIDTA']].to_string(header=False, index=False, index_names=False).split('\n')[0]

        company_name2 = self.catalog.loc[self.catalog.STOCK.isin([ticker2])][['COMPANY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        industry2 = self.catalog.loc[self.catalog.STOCK.isin([ticker2])][['INDUSTRY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        marketcap2 = self.catalog.loc[self.catalog.STOCK.isin([ticker2])][['MARKETCAP']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        ebidta2 = self.catalog.loc[self.catalog.STOCK.isin([ticker2])][['EBIDTA']].to_string(header=False, index=False, index_names=False).split('\n')[0]

        self.tickerColumn1 = Div(text="Company Name", width=120)
        self.tickerColumn2 = Div(text="Industry", width=120)
        self.tickerInfo1 = Div(text='<b>'+company_name1+'</b>', width=300)
        self.tickerInfo2 = Div(text=industry1, width=300)
        self.tickerInfo3 = Div(text='Market cap: ' + marketcap1, width=300)
        self.tickerInfo4 = Div(text='EBIDTA: ' + ebidta1, width=300)

        self.tickerInfo5 = Div(text='<b>'+company_name2+'</b>', width=300)
        self.tickerInfo6 = Div(text=industry2, width=300)
        self.tickerInfo7 = Div(text='Market cap: ' + marketcap2, width=300)
        self.tickerInfo8 = Div(text='EBIDTA: ' + ebidta2, width=300)

    def view_setup(self):
        self.text1 = Div(text="Pair Selector:", width = 150)
        self.timeframebutton = RadioButtonGroup(labels=["Daily", "Hourly"], active=0, width=140)
        self.timeframebutton.on_change("active", self.timeframe_change)

        self.ticker1 = Select(value=self.DEFAULT_TICKERS[0], options=self.nix(self.DEFAULT_TICKERS[1], self.DEFAULT_TICKERS), width=110)
        self.ticker2 = Select(value=self.DEFAULT_TICKERS[1], options=self.nix(self.DEFAULT_TICKERS[0], self.DEFAULT_TICKERS), width=110)
        self.ticker1.on_change('value', self.ticker1_change)
        self.ticker2.on_change('value', self.ticker2_change)
        self.data ,self.t1_data, self.t2_data = self.get_data(self.ticker1.value, self.ticker2.value)
        self.all_stocks_data = self.create_all_stocks_data()

        self.text2 = Div(text='<center><h3>'+"stock information:"+'</h3></center>', width = 400)

        self.tickerInfoTextSetup()

        self.text5 = Div(text="Ticker downloader:", width = 150)
        self.text01 = Div(text="File Dates:", width=150)
        self.tickerdownloader = TextInput(value='',width = 80)
        self.tickerdownloadbutton = Button(label='Press to download', button_type='default', disabled=False, width = 50)
        self.tickerdownloadbutton.on_click(self.tickerdownloadbutton_handler)

        self.widgets = column(
            row(column(self.text1, self.timeframebutton, self.ticker1, self.ticker2), column(column(self.text2), row(self.tickerInfo1, self.tickerInfo5),  row(self.tickerInfo2, self.tickerInfo6), row(self.tickerInfo3, self.tickerInfo7),  row(self.tickerInfo4, self.tickerInfo8)),
                column(self.text5, self.tickerdownloader, self.tickerdownloadbutton)))
        main_row = row(self.widgets)
        layout = column(main_row)


        self.linreg = Linreg(self.data)
        self.price_relation = Price_relation(self.data)
        self.ratio_model = Ratio_model(self.data)
        self.residual_model = Residual_model(self.data)
        self.correlation_matrix = Correlation_matrix(self.all_stocks_data)

        self.tab1 = self.linreg.tab
        self.tab2 = self.price_relation.tab
        self.tab3 = self.ratio_model.tab
        self.tab4 = self.residual_model.tab
        self.tab5 = self.correlation_matrix.tab
        tabs = Tabs(tabs = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5])

        curdoc().add_root(layout)
        curdoc().add_root(tabs)
        curdoc().title = "Stocks"

    def ticker1_change(self,attrname, old, new):
        self.tickerInfo1.text = '<b>' + self.catalog.loc[self.catalog.STOCK.isin([new])][['COMPANY']].to_string(header=False, index=False, index_names=False).split('\n')[0] + '</b>'
        self.tickerInfo2.text = self.catalog.loc[self.catalog.STOCK.isin([new])][['INDUSTRY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        self.tickerInfo3.text = 'Market cap: ' + self.catalog.loc[self.catalog.STOCK.isin([new])][['MARKETCAP']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        self.tickerInfo4.text = 'EBIDTA: ' + self.catalog.loc[self.catalog.STOCK.isin([new])][['EBIDTA']].to_string(header=False, index=False, index_names=False).split('\n')[0]

        self.update()

    def ticker2_change(self, attrname, old, new):
        self.tickerInfo5.text = '<b>' + self.catalog.loc[self.catalog.STOCK.isin([new])][['COMPANY']].to_string(header=False, index=False, index_names=False).split('\n')[0] + '</b>'
        self.tickerInfo6.text = self.catalog.loc[self.catalog.STOCK.isin([new])][['INDUSTRY']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        self.tickerInfo7.text = 'Market cap: ' + self.catalog.loc[self.catalog.STOCK.isin([new])][['MARKETCAP']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        self.tickerInfo8.text = 'EBIDTA: ' + self.catalog.loc[self.catalog.STOCK.isin([new])][['EBIDTA']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        self.update()


    def timeframe_change(self, attrname, old, new):
        self.TIMEFRAME = self.timeframebutton.labels[self.timeframebutton.active]
        self.DEFAULT_TICKERS=self.collect_downloaded_symbols()
        self.history_dir=history_dir+self.TIMEFRAME+'/'
        self.ticker1.value=self.DEFAULT_TICKERS[0]
        self.ticker2.value=self.DEFAULT_TICKERS[1]
        self.update()

    def tickerdownloadbutton_handler(self):
        print('downloading ticker: ' + self.tickerdownloader.value)
        self.tickerdownloadbutton.label = 'downloading...'
        s = self.download_from_ibs(self.tickerdownloader.value)
        print("Control is back here :) ")
        if s.empty:
            print("returned an empty dataframe...")
            self.tickerdownloadbutton.button_type = 'danger'
            self.tickerdownloadbutton.label = 'download failed'
            time.sleep(2)
            self.tickerdownloadbutton.button_type = 'default'
            self.tickerdownloadbutton.label = 'press to download'
            return
        elif not s.empty:
            self.tickerdownloadbutton.button_type = 'success'
            self.tickerdownloadbutton.label = 'downloaded'
            time.sleep(2)
            self.tickerdownloader.value = ''
            self.tickerdownloadbutton.button_type = 'default'
            self.tickerdownloadbutton.label = 'press to download'
        self.update()

    def nix(self, val, lst):
        return [x for x in lst if x != val]

    def download_from_ibs(self, symbol_to_download, venue='SMART', ccy='USD'):

        if self.TIMEFRAME=='Daily':
            barSizeSetting = '1 day'
            duration = '2 Y'
        elif self.TIMEFRAME=='Hourly':
            barSizeSetting = '1 hour'
            duration = '1 M'

        print('called')

        def onError(reqId, errorCode, errorString, contract):
            print("ERROR", reqId, errorCode, errorString)
            if "ambiguous" in errorString:
                self.tickerdownloadbutton.button_type = 'danger'
                self.tickerdownloadbutton.label = 'ambigous symbol'
                time.sleep(2)
                self.tickerdownloadbutton.button_type = 'default'
                self.tickerdownloadbutton.label = 'press to download'
                ib.disconnect()

        ib = IB()
        ib.errorEvent += onError
        ib.setCallback('error', onError)
        util.patchAsyncio()

        print('not connected...trying to connect')
        if not ib.isConnected():
            ib.connect(ib_server, ib_port, clientId=25)

        contract1 = Stock(symbol_to_download, venue, ccy)
        try:
            timeout = 10
            req = ib.reqHistoricalDataAsync(contract1, endDateTime='', durationStr=duration,
                                     barSizeSetting=barSizeSetting, whatToShow='TRADES', useRTH=True)
            bars1=ib.run(asyncio.wait_for(req, timeout))
        except (asyncio.TimeoutError):
            print("TimeOuterror caught")
            ib.disconnect()
            return pd.DataFrame()

        if contract1.symbol not in self.catalog.STOCK:
            fundamentals = ib.reqFundamentalData(contract1, 'ReportSnapshot')
            soup = BeautifulSoup(fundamentals, 'xml')
            CompanyName = soup.find('CoID', Type='CompanyName').contents[0]
            Industry = soup.find('Industry').contents[0]
            ebitda = soup.find('Ratio', FieldName='TTMEBITD').string
            marketcap = soup.find('Ratio', FieldName='MKTCAP').string
            catalog_line = pd.DataFrame([[contract1.symbol, CompanyName, Industry, marketcap, ebitda]],
                                        columns=['STOCK', 'COMPANY', 'INDUSTRY', 'MARKETCAP', 'EBIDTA'])
            self.catalog = self.catalog.append(catalog_line, ignore_index=True)
            self.catalog.to_csv(catalog_file)

        ib.disconnect()

        df0 = util.df(bars1)
        df0 = pd.DataFrame(df0)
        if df0.empty:
            print("df0 is empty!!!")
            return df0

        dp0 = self.history_dir + symbol_to_download + '.csv'
        try:
            os.remove(dp0)
        except OSError:
            pass
        df0.to_csv(dp0)
        df0 = pd.read_csv(self.history_dir + symbol_to_download + '.csv',
                          index_col='date',
                          usecols=[1, 2, 3, 4, 5, 6], parse_dates=True)

        time.sleep(1)
        #get the fundamental data:

        return df0

    def collect_downloaded_symbols(self):
        print("collect_downloaded_symbols called")
        symbols = []
        for root, dirs, files in os.walk(self.history_dir):
            for file in files:
                if file.endswith('.csv') and file.split('.')[0].isalpha() and file != 'catalog.csv':
                    symbols.append(file.split('.')[0])
        print(symbols)
        return symbols

    def create_all_stocks_data(self):
        all_symbols = self.collect_downloaded_symbols()
        df = pd.DataFrame(columns=all_symbols)
        for s in all_symbols:
            df[s] = self.load_ticker(s)[1]['Close']
        print(df.head())
        df.dropna(inplace=True)

        return df



    def load_ticker(self, ticker):
        print("loading ", ticker)
        df = pd.read_csv(self.history_dir + ticker + '.csv', index_col='date', usecols=[1, 2, 3, 4, 5, 6], parse_dates=True)
        df.index = pd.to_datetime(df.index, format=('%Y-%m-%d %H:%M:%S'), box=True)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        def normalize(data):
            norm = (data.Close - data.Close.mean()) / (data.Close.max() - data.Close.min())
            return norm

        df['Norm'] = normalize(df)
        dff = pd.DataFrame({ticker: df.Close, ticker+'_normal': df.Norm})
        return dff, df

    def tls_calc(self, x, y):
        def linear_func(p, x):
            m, c = p
            return m * x + c

        linear_model = Model(linear_func)
        data = RealData(x, y)
        odr = ODR(data, linear_model, beta0=[0., 1.])
        out = odr.run()
        residual_tls = (y - ((x*out.beta[0]) + out.beta[1]))
        return residual_tls

    def get_data(self, t1, t2):
        print("t1 -> ", t1)
        df1, t1_data = self.load_ticker(t1)
        df2, t2_data = self.load_ticker(t2)
        self.data = pd.concat([df1, df2], axis=1)
        self.data = self.data.dropna()
        t1_data = t1_data.reindex_like(t2_data).dropna()
        t2_data = t2_data.reindex_like(t1_data).dropna()

        linreg = np.polyfit(self.data[t1], self.data[t2], 1)
        gradient = linreg[0]
        intercept = linreg[1]

        residual_ols = self.data[t2] - (gradient * self.data[t1] + intercept)
        residual_tls = self.tls_calc(self.data[t1], self.data[t2])

        self.data['t1'] = self.data[t1]
        self.data['t2'] = self.data[t2]
        self.data['t1_normal'] = self.data[t1 + '_normal']
        self.data['t2_normal'] = self.data[t2 + '_normal']
        self.data['residual_ols'] = residual_ols
        self.data['residual_tls'] = residual_tls
        self.data['Time'] = self.data.index.to_julian_date()
        cmin = self.data['Time'].min()
        crange = self.data['Time'].max() - self.data['Time'].min()
        cols = (self.data['Time'] - cmin) * 255 // crange
        self.data['Colors'] = np.array(bk_pal.Plasma256)[cols.astype(int).tolist()]
        nrows = (int((self.data['t1'].count()) / 2))+1
        ticker_tile = np.tile([t1, t2], nrows)
        ticker_tile = ticker_tile[:self.data.index.__len__()]
        tickers = pd.DataFrame(ticker_tile, index=self.data.index, columns=['Ticker'])
        self.data = pd.concat([self.data, tickers], axis=1)
        return self.data, t1_data, t2_data

    def update(self, selected=None):
        print("UPDATE CALLED")
        self.history_dir = history_dir + self.TIMEFRAME + "/"
        self.DEFAULT_TICKERS = self.collect_downloaded_symbols()
        self.ticker2.options = self.nix(self.ticker1.value, self.DEFAULT_TICKERS)
        self.ticker1.options = self.nix(self.ticker2.value, self.DEFAULT_TICKERS)
        t1, t2 = self.ticker1.value, self.ticker2.value
        # if t1 and t2:
        #     self.data, t1_data, t2_data = self.get_data(t1, t2)
        if t1 and t2:
            self.data, t1_data, t2_data = self.get_data(t1, t2)
        self.all_stocks_data=self.create_all_stocks_data()
        self.residual_model.isLRperiodChanged = True
        self.residual_model.update(self.data)
        self.linreg.update(self.data)
        self.price_relation.update(self.data)
        print("PAUSEEE")
        self.ratio_model.update(self.data)

        self.correlation_matrix.update(self.all_stocks_data)


gemini=Gemini()
