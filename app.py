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

# @app.route('/request/system/restart', methods = ['UNLINK'])
# def handle_sysRestart():
# 	os.system("bash ../serverStartup.sh")

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	RegisterJson()
	global intent_reg, intent_string
	if not request.json:
		return jsonify({"request" : "Bad request"}), 400
	Intent = common.getNested(request.json, "queryResult", "intent", "displayName")
	Intent = Intent.lower()
	if Intent in intent_string:
		response = globals()[intent_reg[Intent]["alias"]](request=request.json)	
	fulfillment ["fulfillmentText"] = response
	fulfillment ["fulfillmentMessages"][0]["text"]["text"] = [response]
	return jsonify(fulfillment),200

@app.route('/',methods=['GET'])
def handle_GET():
	return "Methode not supported", 405

def RegisterJson(jsonFile = 'json/fnReg.json'):
	global intent_reg
	global intent_string 
	with open(jsonFile,'r') as file:
		_loads=json.load(file)
		print(_loads)
		for key in _loads:
			globals()[key]=importlib.import_module(_loads[key]["import"])
			intent = _loads[key]['intents']
			intent_reg = {**intent_reg,**intent}
			for intentName in intent:
				intent_string += intentName.lower() + ''
				intentVal = intent.get(intentName)
				globals()[intentVal['alias']]=common.getObject(intentVal['module'],intentVal['func'])

 
if __name__ == '__main__':
	RegisterJson()
	app.run(debug=True,port=5000)
