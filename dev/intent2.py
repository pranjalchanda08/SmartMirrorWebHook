'''**********************************************************************************************
  * Imports
 **********************************************************************************************'''
import common as cm
import requests
from newsapi import NewsApiClient

'''**********************************************************************************************
  * Global Declarations
 **********************************************************************************************'''
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
	URL = "https://newsapi.org/v1/articles"
	parameters = {
	"apiKey":"4674be24a28241968c5077dc28ab1727",
	"source":"bbc-news",
	"sortBy":"top"
	}
	data = requests.get(url= URL, params= parameters).json()
	my_article = data["articles"]
	my_results = []
	speech = "The top news is as follows: \n"
	disp = ""
	for ar in my_article:
		my_results.append(ar["title"])
		for i in range(len(my_results)):
			# print(i + 1, my_results[i])
			speech += "{}. \n".format(my_results[i])
			disp += "{}. {}.\n".format(i + 1, my_results[i])
	return disp,speech

'''**********************************************************************************************
  * @brief	This function is responsible for handling Time intent
  *
  * @param		 request 			request dictionary from request server
 **********************************************************************************************'''
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
	speech = "The time is {} {} {} right now".format(hour,minute,ampm)
	dispresp = "{}:{} {}".format(hour,minute,ampm)
	return dispresp,speech

'''**********************************************************************************************
  * Main Block
 **********************************************************************************************'''
if __name__ == '__main__':
	cm.exportJson(modules)