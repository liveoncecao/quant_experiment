import requests
from .quantexperiment import AlphaVantage as av

class Stock():
    def __init__(self,symbol,key=None):
        url = "{}function={}".format(av._ALPHA_VANTAGE_API_URL,
                                         'GlOBAL_QUOTE')
        url = '{}&{}={}'.format(url, 'symbol', symbol.upper())
        url = '{}&apikey={}'.format(url, key)
        response = list(requests.get(url).json()['Global Quote'].values())
        self._open, self._high, self._low, self._price,\
        self._volume, self._latestday , self._prevclose , self._change, \
        self._changepercent = response[1:]

    @property
    def open(self):
        return float(self._price)

    @property
    def high(self):
        return float(self._high)

    @property
    def low(self):
        return float(self._low)

    @property
    def price(self):
        return float(self._price)

    @property
    def volume(self):
        return float(self._volume)

    @property
    def latestTradingDay(self):
        return self._latestday

    @property
    def previousclose(self):
        return float(self._prevclose)

    @property
    def change(self):
        return float(self._change)

    @property
    def changePercent(self):
        return float(self._changepercent)
