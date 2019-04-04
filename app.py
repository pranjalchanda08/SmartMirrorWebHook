from flask import request, Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

Apixu_KEY = "69d1cf64bfe445a7831103122190404"
Apixu_Request = "http://api.apixu.com/v1/forecast.json"
Apixu_Date = 'dt'
Apixu_City = 'q'
Apixu_Days = 'days'

def getNested(data, *args):
	if args and data:
		element  = args[0]
		if element:
			value = data.get(element)
			return value if len(args) == 1 else getNested(value, *args[1:])
def getDays(startDate,endDate,dFormat = '%Y-%m-%d'):
	if (type(startDate) and type(endDate) and type(dFormat)) is not str:
		return 'Invalid arguments type. Only sypports string'
	else:
		startDate = startDate.split('T')[0]
		endDate = endDate.split('T')[0]
		print(startDate)
		print(endDate)
		a = datetime.strptime(startDate,dFormat)
		b = datetime.strptime(endDate,dFormat)
		diff = b-a
		return diff.days

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	if not request.json:
		return jsonify({"request" : "Bad request"}), 400
	response = ''
	Intent = getNested(request.json, "queryResult", "intent","displayName")
	if 'Weather' in Intent:
		PARAMS = dict(key=Apixu_KEY)
		parameters = getNested(request.json, "queryResult", "parameters")
		location = getNested(parameters, "location")
		if not location:
			location = 'auto:ip'
		PARAMS['q']=location
		date = getNested(parameters, "date")
		if date is not '':
			PARAMS['days'] = date.split('T')[0]
		else:
			date_period = getNested(parameters, "date-period")
			if date_period is not '':
				days=getDays(startDate=date_period["startDate"],
					endDate = date_period["endDate"])
			PARAMS['days'] = str(days)
		print(PARAMS)
		data = requests.get(url= Apixu_Request, params=PARAMS).json()
	return jsonify({"webRequest" : PARAMS}),200

if __name__ == '__main__':
	app.run(debug=True)