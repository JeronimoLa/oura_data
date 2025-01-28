
import json, re, time
from configuraton import OURA_FIRST_DAY

pattern = r'\/v2\/sandbox\/usercollection\/[^\s/{}]+'

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
	

	paths = [ re.search(pattern, path).group() for path in result.keys() if re.search(pattern, path) ]
	urls = set(paths)

	for index, url in enumerate(list(urls), start=1):
		from main import wrapper, write_csv_from_dicts
		print(f"{url}start_date?{OURA_FIRST_DAY}")
		res = wrapper("GET", f"{url}?start_date={OURA_FIRST_DAY}")
		keys = res["data"][0].keys()
		write_csv_from_dicts(res["data"], list(keys), f"docs/csv/{index}.csv")
		time.sleep(5)
	print(len(urls))


if __name__ == "__main__":
    main()
