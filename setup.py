from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = 'Make it easier for you to experiment with quantitative ideas.'

setup(
    name='quant_experiment',
    version='1.0.4',
    description='Python module to get stock and option information through Wed Scraping and Alpha Vantage API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/liveoncecao/quant_experiment',
    author='Quentin Sun',
    author_email='qsun.career@gmail.com',
    license='MIT',
    packages=find_packages(
        exclude=[]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['stocks', 'market', 'options', 'pricing', 'quant', 'quotes', 'tickers', 'symbol'],
    install_requires=['requests', 'pandas', 'beautifulsoup4', 'datetime', 'pytest'],
)
