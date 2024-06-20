from flask import Flask, request, jsonify
from identify import identify_condition

app = Flask(__name__)

@app.route('/identify', methods=['POST'])
def identify():
    text = request.json['text']
    condition = identify_condition(text)
    return jsonify({'condition': condition})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
