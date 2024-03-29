from flask import request, Flask, jsonify
import importlib
import json
import sys
sys.path.insert(0, 'dev')
import common
import os

intent_reg = {}
intent_string = ''

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
def RegisterJson(jsonFile = 'json/fnReg.json'):
	global intent_reg
	global intent_string 
	with open(jsonFile,'r') as file:
		_loads=json.load(file)
		for key in _loads:
			globals()[key]=importlib.import_module(_loads[key]["import"])
			intent = _loads[key]['intents']
			intent_reg = {**intent_reg,**intent}
			for intentName in intent:
				intentVal = intent.get(intentName)
				if intentVal['include'] is True:
					intent_string += intentName.lower() + ' '
					globals()[intentVal['alias']]=common.getObject(intentVal['module'],intentVal['func'])
			print(intent_string)

RegisterJson()

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	global intent_reg, intent_string
	if not request.json:
		return jsonify({"request" : "Bad request"}), 400
	Intent = common.getNested(request.json, "queryResult", "intent", "displayName")
	Intent = Intent.lower()
	if Intent in intent_string:
		disp, speech = globals()[intent_reg[Intent]["alias"]](request=request.json)
	else:
		speech = 'Error:101'
		disp = 'Error:101'
		print("Intent not registered! Please make include to true to add this intent to intent list.")
	fulfillment ["fulfillmentText"] = disp
	fulfillment ["fulfillmentMessages"][0]["text"]["text"] = [speech]
	return jsonify(fulfillment),200

@app.route('/',methods=['GET'])
def handle_GET():
	return "Methode not supported", 405

if __name__ == '__main__':
	app.run(debug=True,port=5000)
