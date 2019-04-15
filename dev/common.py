import sys
import json
from datetime import datetime
def getObject(module, objectName):
	return getattr(sys.modules[module],objectName)

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

def exportJson(dictionary=None):
	x={}
	keys = ''
	path = '../json/fnReg.json'
	with open(path,'r') as jFile:
		x = json.load(jFile)
		for key in x: 
			keys += key + ''	
		for key in dictionary:
			if key in keys:
				return 'Key already exist. Try changing the key name'
		x = {**x,**dictionary}
	with open(path,'w') as jFile:
		json.dump(x,jFile,indent=2)
	return 'Successfully Updated Json'