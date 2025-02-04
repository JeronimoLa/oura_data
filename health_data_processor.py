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

def load_tracker(fieldnames) -> dict:
    try:
        with open("data_tracker.json", "r+") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        data = {file: {} for file in fieldnames}
        with open("data_tracker.json", "w+") as file:
            file.write(json.dumps(data, indent=4))
    

def save_tracker(files, date_last_pulled):
    with open("data_tracker.json", "w+") as file:
        file.write(json.dumps(files, indent=4))


def initial_data_pull():
    url_to_filename = { file: re.search(r'[^/]+$', file).group() for file in extract_unique_urls() }
    tracker = load_tracker(url_to_filename.values())
    for url, filename in url_to_filename.items():
        print(f"{url}start_date?{OURA_FIRST_DAY}")
        tracker[filename]["endpoint"] = url 
        tracker[filename]["last_indexed"] = OURA_FIRST_DAY
        res = wrapper("GET", f"{url}?start_date={OURA_FIRST_DAY}")
        keys = res["data"][0].keys()
        write_csv_from_dicts(res["data"], keys, f"docs/csv/test/{filename}.csv")

    save_tracker(tracker, OURA_FIRST_DAY)
    




def process_new_data(): pass 


if __name__ == "__main__":
    initial_data_pull()
