from currency_converter import get_currency, converter
from click.testing import CliRunner
import json


def test_currency_symbols_recognition():
    assert get_currency('Kč', 'د.ج') == ('CZK', 'DZD')
    assert get_currency('D') == ('GMD', None)
    assert get_currency('GIP') == ('GIP', None)
    assert get_currency('GYD', 'FJD') == ('GYD', 'FJD')


def test_converter():
    runner = CliRunner()

    result = runner.invoke(converter, ['--amount', '5.0', '--input_currency', 'test'])
    assert result.exit_code == 0
    assert "Input currency is not found" in result.output

    result = runner.invoke(converter, ['--amount', '5.0', '--input_currency', 'GBP'])
    results = json.loads(result.output)
    assert result.exit_code == 0
    assert results['input']['amount'] == 5.0 and results['input']['currency'] == 'GBP'
    assert isinstance(results['output']['RUB'], float) and isinstance(results['output']['USD'], float)

    result = runner.invoke(converter, ['--amount', '10.0', '--input_currency', 'GBP',
                                       '--output_currency', 'RUB'])
    results = json.loads(result.output)
    assert result.exit_code == 0
    assert results['input']['amount'] == 10.0 and results['input']['currency'] == 'GBP'
    assert isinstance(results['output']['RUB'], float)




