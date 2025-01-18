import json
import time
from configuraton import BASE_URL, CONFIG


def openapi_spec():
	""" Returns the openapi spec in a dict object """
	with open("openapi-1.23.json", "r+") as file:
		return json.loads(file.read())


def wrapper(method:str, endpoint:str): pass


def example():

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


def recursive_fun(spec:dict, result=None, path=None):
	""" TODO Recursive function to consolidate all the keys 
	Ex. {
			user_info : type_str,
			info : {
				"title": str,
				"description": str,
				"termsOfService": str,
				"version": str,
				"x-logo": {
					"url": str
   				}
			}
			other : type_list <- list of what str/tuples/dict 
		} """
	if result == None:
		result = {}

	if path == None:
		path = []
	
	for key, value in spec.items():
		if isinstance(spec[key], dict):
			if path:
				path.append(key)
				if len(path) <= 1:
					string = "".join(path)
					result[string] = {}
				result[path[-1]] = {}
			else:
				result[key] = {}
				path.append(key)
			recursive_fun(spec[key], result, path)
		else:
			path = []
	return result


def exploration():
	data = openapi_spec()
	paths = data["paths"]

	for path in paths:
		print(f"PATH: {path}")
		if isinstance(paths[path], dict):
			for key, value in paths[path].items():
				print(key)


def main():
	exploration()

	# RECURSION FUNCTION
	# data = openapi_spec()
	# result = {}
	# howdy = recursive_fun(data, result)
	# print(json.dumps(howdy, indent=4))


if __name__ == "__main__":
	main()
