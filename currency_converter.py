import click
import requests
import json
from bs4 import BeautifulSoup
from ruamel.yaml import YAML


@click.command()
@click.option('--amount', help='amount of money in original currency, float', type=float, required=True)
@click.option('--input_currency', help='input currency, 3 letters name or currency symbol', required=True)
@click.option('--output_currency', help='requested/output currency - 3 letters name or currency symbol',
              required=False)
def converter(amount, input_currency, output_currency):
    input_currency, output_currency = get_currency(input_currency, output_currency)
    if not input_currency:
        print(
            "Input currency is not found. "
            "Check whether you specified a definition for multivalued symbols in configs.yaml"
        )
        return
    result = dict(
        input=dict(
            amount=amount,
            currency=input_currency))
    if output_currency:
        amount = {}
        amount[output_currency] = get_amount_in_currency(amount, input_currency, output_currency)
        result['output'] = amount
    else:
        result['output'] = get_amount_in_all_currencies(amount, input_currency)
    print(json.dumps(result))


def get_predefined_currency_match(symbol):
    """
    When there are more than one ISO code corresponding to a symbol,
    check configs.yaml for predefined default ISO code
    :param symbol: symbol of currency
    :return: predefined ISO code, or None if not predefined
    """
    yaml_config = YAML()
    with open('configs.yaml') as stream:
        try:
            config_info = yaml_config.load(stream)
            if 'default_currency_codes' in config_info:
                return config_info['default_currency_codes'].get(symbol)
            return None
        except yaml_config.YAMLError as exc:
            print('Something wrong with the configs.yaml file:')
            print(exc)


def get_iso_code(requested_currency, currencies):
    """
    Get ISO code for requested currency
    :param requested_currency: symbol/ISO code of currency
    :param currencies: dictionary with 'ISO code' as a key and 'Symbol' as a value
    :return: ISO code if found, otherwise None
    """
    if requested_currency not in currencies:
        currency_codes = []
        for code, sym in currencies.items():
            if sym == requested_currency:
                currency_codes.append(code)

        if len(currency_codes) > 0:
            if len(currency_codes) > 1:
                iso_currency = get_predefined_currency_match(requested_currency)
            else:
                iso_currency = currency_codes[0]
        else:
            iso_currency = None
    else:
        iso_currency = requested_currency
    return iso_currency


def get_currency(input_currency, output_currency=None):
    """
    Find currencies among ISO codes and symbols using justforex.com
    :param input_currency: input currency ISO code/symbol
    :param output_currency: output currency ISO code/symbol (if requested)
    :return: input currency and output currency ISO codes, if found
    """
    get_request = 'https://justforex.com/education/currencies'
    search = requests.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    currency_table = soup.find('table', attrs={'id': 'js-table-currencies'})

    rows = currency_table.select('tr')
    currencies = {}  # dictionary with 'ISO code' as a key and 'Symbol' as a value, like {'USD': '$'}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            currencies[cols[0].next] = cols[1].next

    input_currency = get_iso_code(input_currency, currencies)
    if output_currency:
        output_currency = get_iso_code(output_currency, currencies)
    return input_currency, output_currency


def get_amount_in_all_currencies(amount, input_currency):
    """
    Convert input currency amount to all another currencies
    :param amount: float value of requested amount
    :param input_currency: input currency ISO code
    :return: dictionary with 'ISO code' as a key and converted amount as a value, like {'USD': 2.05}
    """
    get_request = 'http://www.xe.com/currencytables/?from={}'.format(input_currency)
    session = requests.Session()
    search = session.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    currency_table = soup.find('table', attrs={'id': 'historicalRateTbl'})
    rows = currency_table.select('tr')
    currency_amounts = {}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            currency_amounts[cols[0].next.next] = amount * float(cols[2].next)
    return currency_amounts


def get_amount_in_currency(amount, input_currency, output_currency):
    """
    Convert input currency amount to output currency
    :param amount: requested amount (float)
    :param input_currency: ISO code of input currency
    :param output_currency: ISO code of output currency
    :return: converted amount
    """
    get_request = 'http://xe.com/currencyconverter/convert/?Amount={}&From={}&To={}'\
        .format(amount, input_currency, output_currency)
    session = requests.Session()
    search = session.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    converted_amount = soup.find('span', attrs={'class': 'uccResultAmount'}).next
    return float(converted_amount)


if __name__ == '__main__':
    converter()
