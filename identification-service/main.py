from flask import Flask, request, jsonify
from identify_condition import identify_condition
from identify_details import identify_details
from text_parser import text_to_json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/identify-condition', methods=['POST'])
def identify_condition_api():
    text = request.json['text']
    condition = identify_condition(text)
    return jsonify({'condition': condition})

@app.route('/identify-details', methods=['POST'])
def identify_details_api():
    text = request.json['text']
    details = identify_details(text)
    return text_to_json(details)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)