from currency_converter import get_currency, convert_currency, CurrencyNotFoundError
from pytest import raises


def test_currency_symbols_recognition():
    assert get_currency('Kč', 'د.ج') == ('CZK', 'DZD')
    assert get_currency('D') == ('GMD', None)
    assert get_currency('GIP') == ('GIP', None)
    assert get_currency('GYD', 'FJD') == ('GYD', 'FJD')


def test_converter():
    with raises(CurrencyNotFoundError):
        convert_currency(5.0, 'test', None)

    results = convert_currency(5.0, 'GBP', None)
    assert results['input']['amount'] == 5.0 and results['input']['currency'] == 'GBP'
    assert isinstance(results['output']['RUB'], float) and isinstance(results['output']['USD'], float)

    results = convert_currency(10.0, 'GBP', 'RUB')
    assert results['input']['amount'] == 10.0 and results['input']['currency'] == 'GBP'
    assert isinstance(results['output']['RUB'], float)




