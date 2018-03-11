from flask import Flask, request, jsonify, make_response, abort
from currency_converter import convert_currency, IncorrectInputError

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, this is a currency converter! :)"


@app.route("/currency_converter", methods=['GET'])
def currency_converter():
    try:
        amount = float(request.args.get('amount'))
        input_currency = request.args.get('input_currency')
        output_currency = request.args.get('output_currency')
        results = convert_currency(amount, input_currency, output_currency)
        return jsonify(results)
    except IncorrectInputError as e:
        abort(make_response(jsonify(status="error", error=str(e)), 400))
    except Exception as e:
        abort(make_response(jsonify(status="unexpected_error", error=str(e)), 500))


if __name__ == '__main__':
    app.run(debug=True)
