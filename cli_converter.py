import json
import click
from currency_converter import convert_currency, IncorrectInputError


@click.command()
@click.option('--amount', help='amount of money in original currency, float', type=float, required=True)
@click.option('--input_currency', help='input currency, 3 letters name or currency symbol', required=True)
@click.option('--output_currency', help='requested/output currency - 3 letters name or currency symbol',
              required=False)
def converter_cli(amount, input_currency, output_currency):
    try:
        print(json.dumps(convert_currency(amount, input_currency, output_currency)))
    except IncorrectInputError as e:
        print('Please check your input:', str(e))
    except Exception as e:
        print('Unexpected error occurred:', str(e))


if __name__ == '__main__':
    converter_cli()
