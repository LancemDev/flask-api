from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/echo', methods=['POST'])
def echo():
    return jsonify(request.json)

if __name__ == '__main__':
    app.run(debug=True)