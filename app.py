from flask import request, Flask, jsonify
import intent

app = Flask(__name__)
fulfillment = {
	"fulfillmentText" : '',
	"fulfillmentMessages": [
		{
			"text" : {
				"text" : ['abcd']
			}
		}
	],
	"source" : "webhook",
}
@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	if not request.json:
		return jsonify({"request" : "Bad request"}), 400
	Intent = intent.getNested(request.json, "queryResult", "intent","displayName")
	if 'Weather' or 'weather' is Intent:
		response = intent.Weather(unit='C', request=request.json)
	
	fulfillment ["fulfillmentText"] = response
	fulfillment ["fulfillmentMessages"][0]["text"]["text"] = [response]
	return jsonify(fulfillment),200

@app.route('/',methods=['GET'])
def handle_GET():
	return jsonify({"request" : "Methode not supported"}), 405

if __name__ == '__main__':
	app.run(debug=True)