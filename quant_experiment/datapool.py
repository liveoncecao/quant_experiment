from .quantexperiment import AlphaVantage as av

class DataPool(av):

    @av._output_format
    @av._call_api_on_func
    def get_quote_endpoint(self, symbol):
        """ Return the latest price and volume information for a
         security of your choice; only support 'json' format

        Keyword Arguments:
            symbol:  the symbol for the equity we want to get its data

        """
        _FUNCTION_KEY = "GLOBAL_QUOTE"
        return _FUNCTION_KEY, 'Global Quote', None