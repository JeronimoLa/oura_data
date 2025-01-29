import csv, json, requests, time, os, re
from configuraton import BASE_URL, CONFIG, OURA_FIRST_DAY, RING_CONFIG_URL
from helper import recursive_fun


def wrapper(method:str, endpoint:str, **kwargs) -> requests:
    """ Basic api wrapper """
    try: 
	    kwargs["params"]
    except KeyError:
	    pass

    headers = { 'Authorization': f'Bearer {CONFIG["token"]}' }   
    return requests.request(method, BASE_URL + endpoint, headers=headers).json()

def api_specification() -> json:
	""" Returns the openapi spec in a dict object """
	with open("docs/json/openapi-1.23.json", "r+") as file:
		return json.loads(file.read())

def extract_unique_urls() -> set:
    data = api_specification()
    pattern = r'\/v2\/sandbox\/usercollection\/[^\s/{}]+'
    urls = set(re.search(pattern, path).group() for path in recursive_fun(data["paths"]) if re.search(pattern, path))
    urls.remove(RING_CONFIG_URL)
    return urls

def load_tracker(): pass

def create_tracker(): pass 

def save_tracker(tracker): pass 

def process_new_data(): pass 


def initial_data_pull():
    for index, url in enumerate(list(urls), start=1):
        filename = re.search(r'[^/]+$', url).group()
        from main import wrapper, write_csv_from_dicts
        print(f"{url}start_date?{OURA_FIRST_DAY}")
        res = wrapper("GET", f"{url}?start_date={OURA_FIRST_DAY}")
        keys = res["data"][0].keys()
        print(res["data"])
        write_csv_from_dicts(res["data"], list(keys), f"docs/csv/test/{filename}.csv")
        time.sleep(3)
    print(len(urls))


if __name__ == "__main__":
    print(extract_unique_urls())