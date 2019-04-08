import json
entity = []
with open('state-city.json') as file:
	data = json.load(file)
	for state, cities in data.items():
		ent = dict(value = state, synonyms= [state])
		entity.append(ent)
	with open('state_entity.json', 'w') as outfile:
		json.dump(entity,outfile,indent=4)
	