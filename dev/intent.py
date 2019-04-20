import common as cm
import requests
from datetime import datetime
import os
import json
import time
import paho.mqtt.client as mqtt

pdi = "dev.intent"
modules = {
	"pdi":{
		"import" : pdi,
		"intents" : {
  			"weather":{
  				"func" : "Weather",
  				"module" : pdi,
  				"include": True,
  				"alias"  : "getWeather"
  			},
  			"device_status":{
  				"func" : "DeviceStatus",
  				"module" : pdi,
  				"include": True,
  				"alias"  : "getDeviceStatus"
  			}
		}
	}
}

broker = "18.218.53.189"
client = mqtt.Client("DeviceStatus")
client.username_pw_set(username= 'dave', password= 'Pranjal')
	
def Weather(request,unit='C'):
	Apixu_KEY = "69d1cf64bfe445a7831103122190404"
	Apixu_Request = "http://api.apixu.com/v1/forecast.json"
	forecast = False
	PARAMS = dict(key=Apixu_KEY)
	parameters = cm.getNested(request, "queryResult", "parameters")
	location = cm.getNested(parameters, "location")
	results = ''
	for  loc in location 			: results += loc+' '
	if   'city' in results			: city= location['city']		
	elif 'subadmin-area' in results	: city= location['subadmin-area']		
	elif 'admin-area'    in results	: city= location['admin-area']		
	elif 'country'       in results	: city= location['country']		
	elif 'island'        in results	: city= location['island']		
	elif 'business-name' in results	: city= location['business-name']		
	elif 'shortcut'      in results	: city= location['shortcut']		
	elif 'street-address'in results : city= location['street-address']		
	elif 'zip-code'      in results	: city= location['zip-code']			
	else							: city= 'auto:ip' 		
	PARAMS['q']=city
	date = cm.getNested(parameters, "date")
	date_period = cm.getNested(parameters, "date-period")
	duration =  cm.getNested(parameters, "duration")
	if date is not '':
		PARAMS['dt'] = date.split('T')[0]
		now = datetime.now().isoformat()
		days=cm.getDays(now,PARAMS['dt'])
		if days is not 0: forecast = True
	elif date_period is not '':	
		days=cm.getDays(startDate=date_period["startDate"],
			endDate = date_period["endDate"])
		forecast = True
		PARAMS['days'] = str(days)
	elif duration is not '': PARAMS['days'] = str(cm.getNested(duration, "amount"))
	else:
		now = datetime.now().isoformat()
		PARAMS['dt'] = now.split('T')[0]
	data = requests.get(url= Apixu_Request, params= PARAMS).json()
	if not forecast:
		speech = "{} is {}, with a feel of {}°{}".format(cm.getNested(data,"location","name"),
			cm.getNested(data,"current","condition","text"),
			cm.getNested(data,"current",("feelslike_c" if unit=='C' else "feelslike_f")), unit)
	else:
		forecast_data = data["forecast"]["forecastday"]
		speech = 'For {}, '.format(cm.getNested(data,"location","name"))
		for x in range(len(forecast_data)):
			date= datetime.strptime(forecast_data[x]['date'],'%Y-%m-%d').strftime("%A, %B %d")
			temp_max = forecast_data[x]['day'][("maxtemp_c" if unit=='C' else "maxtemp_f")]
			temp_min = forecast_data[x]['day'][("mintemp_c" if unit=='C' else "mintemp_f")]
			condition= forecast_data[x]['day']['condition']['text']
			speech+='{} will be {}, with a maximum of {}°{} and a min of {}°{}.\n'.format(date,condition,
					temp_max,unit,temp_min,unit)
	return speech

def DeviceStatus(request,client=client):
	def onPublish(client, userdata, mid):
		print("publish done")

	def getPublish(parameters):
		print(parameters)
		ret = []
		if 'light' in parameters['device']:
			if parameters['number'] is not '':
				topic = 'device/light/dim'
				speed = parameters['number']
				ret.append(dict(topic=topic, payload = speed))
			if parameters['status']  is not '':
				topic ='device/light/status'
				status = parameters['status']
				ret.append(dict(topic=topic, payload=status))
		if 'fan' in parameters['device']:
			topic = 'device/fan'
			if parameters['number'] is not '':
				topic = 'device/fan/speed'
				speed = parameters['number']
				ret.append(dict(topic=topic, payload = speed))
			if parameters['status']  is not '':
				topic ='device/fan/status'
				status = parameters['status']
				ret.append(dict(topic=topic, payload=status))
		print('ret= {}'.format(ret))
		return ret
	def onConnect(client,userdata,flags,rc):
		if rc==0:
			parameters = cm.getNested(request, "queryResult", "parameters")
			ret = getPublish(parameters)
			for element in ret:
				client.publish(topic=element['topic'], payload=element['payload'])			
		else:
			print("Connection Failed, "+ mqtt.connack_string(rc))

	client.connect(broker)
	client.loop_start()
	client.on_connect = onConnect
	client.on_publish = onPublish
	
if __name__ == '__main__':
	cm.exportJson(modules)