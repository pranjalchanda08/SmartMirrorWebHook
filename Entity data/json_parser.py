import json
entity = []
with open('state-city.json') as file:
	data = json.load(file)
	for state, cities in data.items():
		for city in cities:
			ent = dict(value = city, synonyms= [city,city.upper(),city.lower()])
			entity.append(ent)
	with open('city_entity1.json', 'w') as outfile:
		json.dump(entity,outfile,indent=4)
	