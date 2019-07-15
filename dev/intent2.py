import common as cm
import requests

pde = "dev.intent2"
modules = {
	"pde":{
		"import" : pde,
		"intents" : {
  			"news":{
  				"func" : "news",
  				"module" : pde,
  				"include": False,
  				"alias"  : "getNews"
  			},  			
  			"time":{
  				"func" : "Time",
  				"module" : pde,
  				"include": True,
  				"alias"  : "getTime"
  			}
		}
	}
}

def news(request):
	pass

def Time(request):
	location = request['queryResult']['parameters']['geo-country']
	URL = "http://api.apixu.com/v1/current.json"
	if location is "":
		location = "Mysore"
	parameters = {
	"Key": "9d1f70c72a19491f996153026191407",
	"q":location
	}
	data = requests.get(url= URL, params= parameters).json()
	local_time = data['location']['localtime']
	local_time = local_time.split(" ")[1]
	hour = local_time.split(":")[0]
	ampm="am"
	if int(hour)>=12:
		ampm= "pm"
	hour =int(hour)%12
	if hour==0:
		hour = 12
	minute = local_time.split(":")[1]
	response = "The time is {} {} {} right now".format(hour,minute,ampm)
	return response

if __name__ == '__main__':
	cm.exportJson(modules)