import yfinance as yf

class DataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_historical_data(self, start_date, end_date):
        return yf.download(self.symbol, start=start_date, end=end_date)

    def get_current_price(self):
        stock = yf.Ticker(self.symbol)
        return stock.history(period='1d')['Close'].iloc[-1]

    def get_stock_info(self):
        stock = yf.Ticker(self.symbol)
        return stock.info

    def get_intraday_data(self, interval='1m', period='1d'):
        stock = yf.Ticker(self.symbol)
        return stock.history(interval=interval, period=period)