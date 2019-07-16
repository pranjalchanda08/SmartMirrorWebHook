import requests
from datetime import datetime
request={
  "responseId": "7652846a-ffef-4b33-8479-bd5d4959fdf2-5b26cf67",
  "queryResult": {
    "queryText": "what is the time",
    "parameters": {
      "questions": "",
      "geo-country": "Delhi"
    },
    "allRequiredParamsPresent": True,
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "hi"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/stephenv1-0/agent/intents/10bf634a-997a-462d-9df2-ed4cc3e13896",
      "displayName": "Time"
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en"
  },
  "alternativeQueryResults": [
    {
      "queryText": "what is the time",
      "languageCode": "en"
    }
  ]
}

location = request['queryResult']['parameters']['geo-country']
#print(location)

def Time(request):
  location = request['queryResult']['parameters']['geo-country']
  URL = "http://api.apixu.com/v1/current.json"
  if location is "":
    #we need to fetch current location
    pass
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
  print(response)

if __name__ == '__main__':
  Time(request=request)