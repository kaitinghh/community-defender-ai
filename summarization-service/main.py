from flask import Flask, request, jsonify
from summarize import first_summarize, subsequent_summarize

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.json['text']
    is_first = request.json['is_first']
    if is_first:
        summary = first_summarize(text)
    else:
        summary = subsequent_summarize(text)
    return jsonify({'summary': summary})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
