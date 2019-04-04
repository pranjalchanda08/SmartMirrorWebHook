from flask import request, Flask, jsonify
app = Flask(__name__)

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
	response = {"intent" : get_nested(request.json, "queryResult", "intent","displayName") }
	return jsonify({"response" : response}),200

if __name__ == '__main__':
	app.run(debug=True)