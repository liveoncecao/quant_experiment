from .quant_experiment import finproducts
import pytest


def test_VanillaOption(symbol, d, m, y, strike, opt_type):
    # check format of input parameters
    assert opt_type == 'calls' or opt_type == 'puts'
    assert type(symbol) is str
    assert (type(d) is int) and (type(m) is int) and (type(y) is int)
    assert (type(strike) is float or type(strike) is int) and (strike > 0)
    # check column names for the returned value
    assert (list(finproducts.VanillaOption(symbol, d, m, y, strike, opt_type).option_info().columns) == ['contractSymbol', 'strike', 'currency', 'lastPrice', 'change', 'percentChange', 'volume', 'openInterest', 'bid', 'ask',
                                                                                                         'contractSize', 'expiration', 'lastTradeDate', 'impliedVolatility', 'inTheMoney'])
