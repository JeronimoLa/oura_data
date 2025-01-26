
import json

def example():
	""" Example of hitting the api endpoint """
	url = 'https://api.ouraring.com/v2/usercollection/personal_info' 
	params={ 
		'start_date': '2021-11-01', 
		'end_date': '2025-1-06' 
	}
	headers = { 
		'Authorization': f'Bearer {CONFIG["token"]}' 
	}   
	response = requests.request('GET', url, headers=headers, params=params) 
	print(response.text)

def openapi_spec():
	""" Returns the openapi spec in a dict object """
	with open("docs/json/openapi-1.23.json", "r+") as file:
		return json.loads(file.read())

def recursive_enchancement(spec:dict, target="name", result=None):
	if isinstance(spec, dict): # sometimes its a list 
		if result == None:
			result = {}
		for key, value in spec.items():
			# if target == key:
				# print(value)
				# yield result =  
				# print(json.dumps(value, indent=4))
			if isinstance(value, dict):
				result[key] = recursive_fun(value)
				
			elif isinstance(value, list):
				for v in value:
					if isinstance(v, dict):
						keys = v.keys()
						for key in keys:
							# print(key)
							value_of_key = v.get(key)
							if isinstance(value_of_key, dict):
								print(type(value_of_key))
								print(value_of_key)
								result[key] = recursive_fun(value_of_key)
						# recursive_fun(v.get(v))
						# result[key] = value

			else:
				result[key] = type(value).__name__			
	return result

def recursive_fun(spec:dict, result=None, path=None):
    if isinstance(spec, dict): # sometimes its a list 
        if result == None:
            result = {}
        for key, value in spec.items():
            if isinstance(value, dict):
                result[key] = recursive_fun(value)
            else:
                result[key] = type(value).__name__
    return result

def main():
    data = openapi_spec()
    result = recursive_fun(data["paths"])
    for path in result.keys():
        print(path)
    # print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()