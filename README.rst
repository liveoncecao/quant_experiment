================
Quant_Experiment
================

..  image:: https://img.shields.io/pypi/v/quant_experiment.svg
    :target: https://pypi.python.org/pypi/quant_experiment
    :alt: PyPI Version

..  image:: https://img.shields.io/pypi/l/quant_experiment.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License

..  image:: https://img.shields.io/pypi/pyversions/quant_experiment.svg
    :target: https://pypi.python.org/pypi/quant_experiment
    :alt: Python Version Support

Features
========

- **Realtime stock and option data:** You can easily extract the latest stock and option information
- **Option characteristics:** Library provides you with option relevant characteristics based on Black-Scholes model

Installation
============

Installing With ``pip``
-----------------------
.. code-block:: bash

    $ pip install quant_experiment

Quickstart
==========
Data is retrieved from Alpha Vantage API free services, make sure initializing a key variable first

.. code:: python

    key = "YOUR_API_KEY"

1. Operation on stock data

.. code:: python

    from quant_experiment import finproducts
        stock_demo = finproducts.Stock('AAPL',key)
        stock_demo.price #return realtime stock price
        stock_demo.latestTradingDay #lastest trading day
        stock_demo.volume #volume

2. Operation on option data

.. code:: python

    from quant_experiment import finproducts
        option_demo = finproducts.VanillaOption('AAPL', 21, 6, 2019, 180, 'calls')
        #call option with expiration date 2019-06-21 and strike price 180
        option_demo.option_info()

Giving us output as:

.. figure:: https://github.com/liveoncecao/quant_experiment/blob/master/images/option_info.png?raw=true
   :alt: alias of image

3. Return option property based on Black-Scholes

.. code:: python

    from quant_experiment import finproducts
        option_demo = finproducts.VanillaOption('AAPL', 21, 6, 2019, 180, 'calls')
        option_demo.BS_Info(key) #return implied volatility by default
        option_demo.BS_Info(key,'greeks') #return delta, gamma, vega, theta and rho


Contributing
============
All contributions are welcome.
