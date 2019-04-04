from flask import request, Flask, jsonify
app = Flask(__name__)

Apixu_KEY = 69d1cf64bfe445a7831103122190404
Apixu_Request = "http://api.apixu.com/v1/forecast.json?key="+Apixu_KEY"&q="

def get_nested(data, *args):
	if args and data:
		element  = args[0]
		if element:
			value = data.get(element)
			return value if len(args) == 1 else get_nested(value, *args[1:])

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	if not request.json:
		abort(400)
	response = ''
	Intent = get_nested(request.json, "queryResult", "intent","displayName")
	if Intent is 'Weather':
		location = get_nested(request.json, "queryResult", "parameters", "location")
	return jsonify({"response" : response}),200

if __name__ == '__main__':
	app.run(debug=True)