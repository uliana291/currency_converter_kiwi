# Currency converter

This is an application for converting specified amount from one currency to another. 
If only one currency is specified, amount is converted to all currencies.

## Getting started

The application works in 2 modes: CLI application and web API application.
If you want to use it as a CLI application, run `cli_converter.py`,
if you want to use a web API application, run `flask_api_converter.py`.

### Prerequisites

You can find all the requirements in `requirements.txt` file.

## CLI application

To run CLI application, run `cli_converter.py` and specify arguments:
- `amount` - amount which you want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

If you don't specify `output_currency`, then input_currency will be converted to all known currencies.

Example: 
```
./cli_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2546.72, 
    }
}
```

```
./cli_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{   
    "input": {
        "amount": 0.9,
        "currency": "JPY"
    },
    "output": {
        "AUD": 0.0107326, 
    }
}
```

**Note:**
if you want to use symbols, please predefine ISO codes for those currencies, which can be interpreted differently.

For example, symbol `$` may be `MXN`, `KYD`, `USD`, ... 

If you want to use `$`, specify the definition in `configs.yaml`, like this:
```
default_currency_codes:
  $: USD
  .
  .
  .
```  

## Web API application

To run web API application, run `flask_api_converter.py`. Specify the arguments, like here:

```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{   
    "input": {
        "amount": 0.9,
        "currency": "JPY"
    },
    "output": {
        "AUD": 0.0107326, 
    }
}
```

```
GET /currency_converter?amount=10.92&input_currency=$ HTTP/1.1
{
    "input": {
        "amount": 10.92,
        "currency": "USD"
    },
    "output": {
        "EUR": 8.872859007012,
        "RUB": 618.5315689982519,
        "BSD": 10.92,
        .
        .
        .
    }
}
```


## Running the tests

To run tests, use `pytest`. It will run `test_currency_converter.py`, where tests are implemented.

## Author

* **Julia Gurianova** - [uliana291](https://github.com/uliana291)