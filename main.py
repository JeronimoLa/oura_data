import json
import time
from configuraton import BASE_URL, CONFIG


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
	with open("openapi-1.23.json", "r+") as file:
		return json.loads(file.read())

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

def wrapper(method:str, endpoint:str): pass

def main():
	data = openapi_spec()
	result = recursive_fun(data)
	print(json.dumps(result, indent=4))
	with open("new_format.json", "w+") as file:
		file.write(json.dumps(result, indent=4))

if __name__ == "__main__":
	main()
