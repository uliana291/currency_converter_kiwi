from flask import Flask, request, jsonify, red
from currency_converter import convert_currency
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, this is a currency converter! :)"


@app.route("/currency_converter", methods=['GET'])
def currency_converter():
    amount = float(request.args.get('amount'))
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency')
    results = convert_currency(amount, input_currency, output_currency)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
