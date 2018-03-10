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
#    print(input_currency, output_currency)
    if not input_currency:
        print("Input currency is not found. Check whether you specified a code for multivalued symbols")
        return
    result = dict(
        input=dict(
            amount=amount,
            currency=input_currency))
    if not output_currency:
        result['output'] = get_currency_rates_for(amount, input_currency)
    else:
        rate = {}
        rate[output_currency] = get_exchange_rate(amount, input_currency, output_currency)
        result['output'] = rate
    print(json.dumps(result))


def get_multivalued_symbols_from_config(symbol):
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


def is_problem_with_sym(codes, currency):
    if len(codes) > 0:
        if len(codes) > 1:
            return get_multivalued_symbols_from_config(currency)
        return codes[0]
    else:
        return None


def get_currency(input_currency, output_currency=None):
    get_request = 'https://justforex.com/education/currencies'
    search = requests.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    currency_table = soup.find('table', attrs={'id': 'js-table-currencies'})
    rows = currency_table.select('tr')
    currencies = {}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            currencies[cols[0].next] = cols[1].next
    if input_currency not in currencies or \
            (output_currency is not None and output_currency not in currencies):
        if output_currency is not None and output_currency not in currencies:
            output_currency_search = output_currency
        else:
            output_currency_search = None
        input_currency_codes = []
        output_currency_codes = []
        for code, sym in currencies.items():
            if sym == input_currency:
                input_currency_codes.append(code)
            if output_currency_search and sym == output_currency_search:
                output_currency_codes.append(code)
        input_currency = is_problem_with_sym(input_currency_codes, input_currency)
        if output_currency_search:
            output_currency = is_problem_with_sym(output_currency_codes, output_currency)
    return input_currency, output_currency


def get_currency_rates_for(amount, input_currency):
    get_request = 'http://www.xe.com/currencytables/?from={}'.format(input_currency)
    session = requests.Session()
    search = session.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    currency_table = soup.find('table', attrs={'id': 'historicalRateTbl'})
    rows = currency_table.select('tr')
    currency_rates = {}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            currency_rates[cols[0].next.next] = amount * float(cols[2].next)
    return currency_rates


def get_exchange_rate(amount, input_currency, output_currency):
    get_request = 'http://xe.com/currencyconverter/convert/?Amount={}&From={}&To={}'\
        .format(amount, input_currency, output_currency)
    session = requests.Session()
    search = session.get(get_request)
    soup = BeautifulSoup(search.content, 'html.parser')
    exchange_amount = soup.find('span', attrs={'class': 'uccResultAmount'}).next
    return float(exchange_amount)


if __name__ == '__main__':
    converter()