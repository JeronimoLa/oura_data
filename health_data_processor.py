import csv, json, requests, time, os, re
from configuraton import BASE_URL, CONFIG, OURA_FIRST_DAY, RING_CONFIG_URL
from helper import recursive_fun, write_csv_from_dicts


def wrapper(method:str, endpoint:str, **kwargs) -> requests:
    """ Basic api wrapper """
    try: 
	    kwargs["params"]
    except KeyError:
	    pass

    headers = { 'Authorization': f'Bearer {CONFIG["token"]}' }   
    return requests.request(method, BASE_URL + endpoint, headers=headers).json()

def api_specification() -> dict:
	""" Returns the openapi spec in a dict object """
	with open("docs/json/openapi-1.23.json", "r+") as file:
		return json.loads(file.read())

def extract_unique_urls() -> set:
    data = api_specification()
    pattern = r'\/v2\/sandbox\/usercollection\/[^\s/{}]+'
    urls = set(re.search(pattern, path).group() for path in recursive_fun(data["paths"]) if re.search(pattern, path))
    urls.remove(RING_CONFIG_URL)
    return urls

def load_tracker() -> dict:
    try:
        with open("data_tracker.json", "r+") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        open("data_tracker.json", "x")
        return {}

def save_tracker(files, date_last_pulled): pass 

def process_new_data(): pass 

def daily_pull(): pass

def initial_data_pull():
    filenames = [ re.search(r'[^/]+$', file).group() for file in extract_unique_urls() ]
    tracker = load_tracker()

    print(f"{url}start_date?{OURA_FIRST_DAY}")
    for filename in filenames:
        res = wrapper("GET", f"{url}?start_date={OURA_FIRST_DAY}")
        keys = res["data"][0].keys()
        new_data = process_new_data(res["data"])
        write_csv_from_dicts(new_data, keys, f"docs/csv/test/{filename}.csv")
        time.sleep(500)

if __name__ == "__main__":
    # print(extract_unique_urls())
    initial_data_pull()