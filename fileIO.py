import json

def jsonSave(data, fileName, indent=True, sort=False, oneLine=False):
	f = open(fileName, 'w')


	if indent:
		f.write(json.dumps(data, indent=4, sort_keys=sort))
	else:
		f.write(json.dumps(data, sort_keys=sort))

	f.close()

def jsonLoad(fileName):
	try:
		file = open(fileName)
		t=file.read()
		file.close()
		return json.loads(t)
	except:
		return {}