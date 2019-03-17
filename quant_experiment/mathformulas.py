import requests
import numpy as np
from bs4 import BeautifulSoup
from .constants import TREASURY_URL, OVERNIGHT_RATE
from scipy.interpolate import interp1d
from scipy.stats import norm
from scipy.optimize import fsolve
import math


def riskfree():
    r = requests.get(TREASURY_URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find("table", attrs={'class' : 't-chart'})
    rows= table.find_all('tr')
    lastrow = len(rows)-1
    cells = rows[lastrow].find_all("td")
    date = cells[0].get_text()
    m1 = float(cells[1].get_text())
    m3 = float(cells[2].get_text())
    m6 = float(cells[3].get_text())
    y1 = float(cells[4].get_text())
    y2 = float(cells[5].get_text())
    y3 = float(cells[6].get_text())
    y5 = float(cells[7].get_text())
    y7 = float(cells[8].get_text())
    y10 = float(cells[9].get_text())
    y20 = float(cells[10].get_text())
    y30 = float(cells[11].get_text())

    years = (0, 1/12, 3/12, 6/12, 12/12, 24/12, 36/12, 60/12, 84/12, 120/12, 240/12, 360/12)
    rates = (OVERNIGHT_RATE, m1/100, m3/100, m6/100, y1/100, y2/100, y3/100, y5/100, y7/100, y10/100, y20/100, y30/100)
    return interp1d(years, rates)


class BlackandScholes:
    def __init__(self, S0, K, tau, r, price, op_type, q=0):
        """
        :param S0:
        :param K:
        :param tau:
        :param r:
        :param price: the bid price is used here
        :param op_type:
        :param q:
        """
        self._S0 = S0
        self._K = K
        self._tau = tau
        self._r = r
        self._q = q
        self._op_price = price
        self._op_type = op_type
        self.implied_vol = self.implied_vol()

    @staticmethod
    def bs_call(S0, K, tau, r, sigma, q=0):
        d1 = (np.log(S0/K)+(r-q+sigma**2/2)*tau)/(sigma*np.sqrt(tau))
        d2 = d1 - sigma*np.sqrt(tau)
        return S0*np.exp(-q*tau)*norm.cdf(d1) - K*np.exp(-r*tau)*norm.cdf(d2)

    @staticmethod
    def bs_put(S0, K, tau, r, sigma, q=0):
        d1 = (np.log(S0 / K) + (r - q + sigma ** 2 / 2) * tau) / (sigma * np.sqrt(tau))
        d2 = d1 - sigma * np.sqrt(tau)
        return K*np.exp(-r*tau)*norm.cdf(-d2) - S0*np.exp(-q*tau)*norm.cdf(-d1)

    def _fprime(self, sigma):
        logSoverK = np.log(self._S0 / self._K)
        n12 = ((self._r + sigma ** 2 / 2) * self._tau)
        numerd1 = logSoverK + n12
        d1 = numerd1 / (sigma * np.sqrt(self._tau))
        return self._S0 * np.sqrt(self._tau) * norm.pdf(d1) * np.exp(-self._r * self._tau)

    def implied_vol(self):
        if self._op_type.lower() == 'calls':
            func = lambda x: (self.bs_call(self._S0, self._K, self._tau, self._r, x, self._q) - self._op_price)
            # An approximation formula for choosing starting point
            initial = np.sqrt(2*math.pi/self._tau)*self._op_price/self._S0
            return fsolve(func, initial, fprime=self._fprime)[0]
        if self._op_type.lower() == 'puts':
            func = lambda x: (self.bs_put(self._S0, self._K, self._tau, self._r, x, self._q) - self._op_price)
            initial = np.sqrt(2 * math.pi / self._tau) * self._op_price / self._S0
            return fsolve(func, initial, fprime=self._fprime)[0]




