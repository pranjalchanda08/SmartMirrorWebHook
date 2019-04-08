import requests
from datetime import datetime

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
	forecast = False
	PARAMS = dict(key=Apixu_KEY)
	parameters = getNested(request, "queryResult", "parameters")
	geo_city = getNested(parameters, "city")
	geo_state = getNested(parameters, "state")
	location = geo_city if geo_state =='' else geo_state  
	if location is '':
		ipPARAM = {'format' : 'json'}
		location = (requests.get(url='https://api.ipify.org', params=ipPARAM).json())['ip']
	PARAMS['q']=location
	date = getNested(parameters, "date")
	date_period = getNested(parameters, "date-period")
	if date is not '':
		PARAMS['dt'] = date.split('T')[0]
		now = datetime.now().isoformat()
		days=getDays(now,PARAMS['dt'])
		if days is not 0:
			forecast = True
	elif date_period is not '':	
		days=getDays(startDate=date_period["startDate"],
			endDate = date_period["endDate"])
		forecast = True
		PARAMS['days'] = str(days)
	else:
		now = datetime.now().isoformat()
		PARAMS['dt'] = now.split('T')[0]
	data = requests.get(url= Apixu_Request, params= PARAMS).json()
	if not forecast:
		speech = "{}, with a feel of {}°{}".format(getNested(data,"current","condition","text"),
			getNested(data,"current",("feelslike_c" if unit=='C' else "feelslike_f")), unit)
	else:
		forecast_data = data["forecast"]["forecastday"]
		speech=''
		for x in range(len(forecast_data)):
			date= datetime.strptime(forecast_data[x]['date'],'%Y-%m-%d').strftime("%A, %B %d")
			temp_max = forecast_data[x]['day'][("maxtemp_c" if unit=='C' else "maxtemp_f")]
			temp_min = forecast_data[x]['day'][("mintemp_c" if unit=='C' else "mintemp_f")]
			condition= forecast_data[x]['day']['condition']['text']
			speech+='{} is {}, with a maximum of {}°{} and a min of {}°{}.\n'.format(date,condition,
																temp_max,unit,temp_min,unit)
	return speech
