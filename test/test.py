import pandas as pd
from yahoofinancials import YahooFinancials
from datetime import datetime

ticker = 'AAPL'
yahoo_financials = YahooFinancials(ticker)

data = yahoo_financials.get_historical_price_data(
    '2008-09-15', '2018-09-15', 'weekly')

dat = pd.DataFrame(data[ticker]['prices']).drop(['date', 'adjclose'], axis=1)
dat.dropna(inplace=True)  # drop row with na to remove non trading days
dat['formatted_date'] = pd.to_datetime(
    dat['formatted_date'], format="%Y-%m-%d")
dat.set_index('formatted_date', inplace=True)
dat.index.name = ""
dat.columns = ['High', "Low", "Open", "Close", "Volume"]
dat = dat[["Open", 'High', "Low", "Close", "Volume"]]
print(dat.head())