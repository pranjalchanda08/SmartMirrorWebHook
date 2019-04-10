from flask import request, Flask, jsonify
import importlib
import json
import sys

intent_reg = {}

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
	Intent = intent.getNested(request.json, "queryResult", "intent", "displayName")
	if 'Weather' or 'weather' is Intent:
		response = intent.Weather(request=request.json)	
	fulfillment ["fulfillmentText"] = response
	fulfillment ["fulfillmentMessages"][0]["text"]["text"] = [response]
	return jsonify(fulfillment),200

@app.route('/',methods=['GET'])
def handle_GET():
	return "Methode not supported", 405

def importFromJson(jsonFile = 'json/fnReg.json'):
	global intent_reg
	with open(jsonFile,'r') as file:
		_loads=json.load(file)
		for key in _loads:
			globals()[key]=importlib.import_module(_loads[key]["import"])

if __name__ == '__main__':
	importFromJson()
	# app.run(debug=True)