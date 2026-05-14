from flask import Flask, request, jsonify
from flask_cors import CORS
from main import process_checkout

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():

    data = request.json

    barcode = data['barcode']

    original_price = data['originalPrice']

    discounted_price = data.get('discountedPrice')

    result = process_checkout(
        barcode,
        original_price,
        discounted_price
    )

    return jsonify(result)

app.run(host='0.0.0.0', port=5000)