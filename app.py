from flask import request, Flask, jsonify
import requests

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
	if (type(startDate) and type(endDate) and tyepe(dFormat)) is not str:
		return 'Invalid arguments type. Only sypports string'
	else:
		startDate = startDate.split('T')[0]
		endDate = startDate.split('T')[0]
		a = datetime.strptime(starDate,dFormat)
		b = datetime.strptime(endDate,dFormat)
		diff = b-a
		return diff.days

@app.route('/request/dailogueflow/' , methods=['POST'])
def handle_POST():
	if not request.json:
		abort(400)
	response = ''
	Intent = getNested(request.json, "queryResult", "intent","displayName")
	if Intent is 'Weather':
		PARAMS = dict(key=Apixu_KEY)
		location = getNested(request.json, "queryResult", "parameters", "location")
		if not location:
			location = 'auto:ip'
		PARAMS['q']=location
		date = getNested(request.json, "queryResult", "parameters", "date")
		if date is '':
			date_period = getNested(request.json, "queryResult", "parameters", "date-period")
			if date_period is not '':
				days=getDays(startDate=getNested(date_period, "startDate"),
					endDate = getNested(date_period, "endDate"))
			PARAMS['days'] = str(days)
		else:
			PARAMS['days'] = date.split('T')[0]
		data = requests.get(url= Apixu_Request, params=PARAMS).json()		
	return jsonify({"response" : response}),200

if __name__ == '__main__':
	app.run(debug=True)