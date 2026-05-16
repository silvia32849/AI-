from flask import Flask, request, jsonify
from flask_cors import CORS
from main import process_checkout

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():

    try:

        data = request.get_json()

        print(data)

        barcode = data.get('barcode')
        original_price = data.get('originalPrice')
        discounted_price = data.get('discountedPrice')

        result = process_checkout(
            barcode,
            original_price,
            discounted_price
        )

        return jsonify(result)

    except Exception as e:

        print("에러 발생:", e)

        return jsonify({
            "error": str(e)
        }), 500

app.run(host='0.0.0.0', port=5000)