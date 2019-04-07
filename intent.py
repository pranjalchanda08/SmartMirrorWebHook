import requests
from datetime import datetime

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
		a = datetime.strptime(startDate,dFormat)
		b = datetime.strptime(endDate,dFormat)
		diff = b-a
		return diff.days

def Weather(request,unit='C'):
	global fulfillment
	Apixu_KEY = "69d1cf64bfe445a7831103122190404"
	Apixu_Request = "http://api.apixu.com/v1/forecast.json"
	forcast = False
	PARAMS = dict(key=Apixu_KEY)
	parameters = getNested(request, "queryResult", "parameters")
	location = getNested(parameters, "geo-city")
	if not location:
		location = 'auto:ip'
	PARAMS['q']=location
	date = getNested(parameters, "date")
	if date is not '':
		PARAMS['dt'] = date.split('T')[0]
		now = datetime.now().isoformat()
		days=getDays(now,PARAMS['dt'])
		if days is not 0:
			forcast = True
	else:
		date_period = getNested(parameters, "date-period")
		if date_period is not '':
			days=getDays(startDate=date_period["startDate"],
				endDate = date_period["endDate"])
			forcast = True
		PARAMS['days'] = str(days)
	data = requests.get(url= Apixu_Request, params= PARAMS).json()
	if not forcast:
		speech = "Its goning to be {}, with a feel of {}°{}".format(getNested(data,"current","condition","text"),
			getNested(data,"current",("feelslike_c" if unit=='C' else "feelslike_f")), unit)
	else:
		forcast_data = data["forecast"]["forecastday"]
		speech=''
		for x in range(len(forcast_data)):
			date= datetime.strptime(forcast_data[x]['date'],'%Y-%m-%d').strftime("%A, %B %d")
			temp_max= forcast_data[x]['day'][("maxtemp_c" if unit=='C' else "maxtemp_f")]
			temp_min= forcast_data[x]['day'][("mintemp_c" if unit=='C' else "mintemp_f")]
			condition= forcast_data[x]['day']['condition']['text']
			speech+= '{} is {}, with a maximum of {}°{} and a min of {}°{}. '.format(date,condition,
										temp_max,unit,temp_min,unit)
	fulfillment ["fulfillmentText"] = speech
	fulfillment ["fulfillmentMessages"][0]["text"]["text"] = [speech]
	return fulfillment
