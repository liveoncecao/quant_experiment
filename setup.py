from setuptools import setup, find_packages

setup(
    name='quant_experiment',
    version='1.0.0',
    description='Python module to get stock and option information through Wed Scraping and Alpha Vantage API',
    url='https://github.com/liveoncecao/quant_experiment',
    author='Quentin Sun',
    author_email='qsun.career@gmail.com',
    license='MIT',
    packages=find_packages(
        exclude=[]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['stocks', 'market', 'options', 'pricing', 'quant', 'quotes', 'tickers', 'symbol'],
    install_requires=['requests', 'math', 'pandas', 'beautifulsoup4'],
)