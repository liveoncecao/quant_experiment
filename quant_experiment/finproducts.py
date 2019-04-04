import requests
import pandas as pd
from time import mktime
from datetime import datetime, date
from .constants import _Y_API
from .constants import _ALPHA_VANTAGE_API_URL
from .mathformulas import BlackandScholes
from .mathformulas import riskfree


class VanillaOption:
    def __init__(self, symbol, d, m, y, strike, opt_type):
        """
        :param symbol: e.g. 'AAPL', 'MSFT'
        :param d: e.g. 1,2,3,...,31
        :param m: e.g. 1,2,....,12
        :param y: e.g. 2018,2019
        :param strike: e.g. 100,105
        :param opt_type: e.g. 'calls' or 'puts'
        """

        self._strike = strike
        self._symbol = symbol
        self._epoch = int(round(mktime(date(y, m, d).timetuple()) / 86400, 0) * 86400)
        self._date = datetime.utcfromtimestamp(self._epoch).date()
        url = _Y_API + symbol.upper() + '?date=' + str(self._epoch)
        self._response = requests.get(url).json()['optionChain']['result']

        if len(self._response) == 0:
            raise LookupError("Could not corresponding information for the symbol.")

        self._expirationDates = [datetime.utcfromtimestamp(
            i).date() for i in self._response[0]['expirationDates']]
        self._strikes = self._response[0]['strikes']

        # Raise error when could not find information for relevant expiration date or strike price
        if self._date not in self._expirationDates:
            raise LookupError("Expiration dates are: ", self._expirationDates)
        elif strike not in self._strikes:
            raise LookupError("Strike prices are: ", self._strikes)

        # Raise error when returned value is empty because sometimes there could be only call or put
        self._type = opt_type.lower()
        if self._type == 'calls' and len(self._response[0]['options'][0]['calls']) == 0:
            raise LookupError('No such call exists.')
        if self._type == 'puts' and len(self._response[0]['options'][0]['puts']) == 0:
            raise LookupError('No such put exists.')

        toLookup = self._response[0]['options'][0][self._type]
        for c in toLookup:
            if c['strike'] == self._strike:
                found = c
                break
        found['expiration'] = datetime.utcfromtimestamp(found['expiration']).date()
        found['lastTradeDate'] = datetime.utcfromtimestamp(found['lastTradeDate']).date()
        self._last_trade_date = found['lastTradeDate']
        self._option_info = pd.DataFrame(columns=found.keys())
        self._option_info.loc[0] = list(found.values())

    def option_info(self):
        """
        :return: return information for the vanilla option
        """
        return self._option_info

    def BS_Info(self, key=None, info_name='implied_vol', q=0):
        """
        Based on Black Scholes model, calculated implied vol will lose its accuracy for DeepInTheMoney
        and DeepOutOfMoney options with relatively short time to maturity, use with your own discretion
        """
        stock_info = Stock(self._symbol, key)
        self._stock_price = stock_info.price
        self._tau = (self._date - self._last_trade_date).days/365
        self._r = riskfree()(self._tau)

        self.BandS = BlackandScholes(self._stock_price, self._strike, self._tau, self._r,
                                     self._option_info['lastPrice'][0], self._type, q)

        if info_name == 'implied_vol':
            return self.BandS.imp_vol
        if info_name == 'greeks':
            columns = ['delta', 'gamma', 'vega', 'theta', 'rho']
            return pd.DataFrame([[self.BandS.delta(), self.BandS.gamma(), self.BandS.vega(),
                                  self.BandS.theta(), self.BandS.rho()]], columns=columns)


class Stock:
    def __init__(self, symbol, key=None):
        url = "{}function={}".format(_ALPHA_VANTAGE_API_URL, 'GlOBAL_QUOTE')
        url = '{}&{}={}'.format(url, 'symbol', symbol.upper())
        url = '{}&apikey={}'.format(url, key)
        response = list(requests.get(url).json()['Global Quote'].values())
        self._open, self._high, self._low, self._price,\
            self._volume, self._latestday, self._prevclose, self._change, \
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
