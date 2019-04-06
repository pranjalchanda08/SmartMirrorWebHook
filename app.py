from flask import request, Flask, jsonify
import intent

app = Flask(__name__)

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	if not request.json:
		return jsonify({"request" : "Bad request"}), 400
	Intent = intent.getNested(request.json, "queryResult", "intent","displayName")
	if 'Weather' or 'weather' is Intent:
		response = intent.Weather(unit='C', request=request.json)
	return jsonify(response),200


if __name__ == '__main__':
	app.run(debug=True)