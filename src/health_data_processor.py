import json, re, requests
from datetime import date, timedelta

from src.configuraton import BASE_URL, CONFIG, OURA_FIRST_DAY, RING_CONFIG_URL, URL_PATTERN
from src.helper import recursive_fun, write_csv_from_dicts


def wrapper(method:str, endpoint:str, **kwargs) -> json:
    """ Basic api wrapper """
    try:
        kwargs["params"]
    except KeyError:
        pass

    headers = {'Authorization': f'Bearer {CONFIG["token"]}'}
    return requests.request(method, BASE_URL + endpoint, headers=headers).json()

def api_specification() -> dict:  
    """ Returns the openapi spec in a dict object """
    with open("docs/json/openapi-1.23.json", "r+", encoding="utf-8") as file:
        return json.loads(file.read())

def extract_unique_urls() -> set:
    data = api_specification()
    urls = set(re.search(URL_PATTERN, path).group() for path in recursive_fun(data["paths"]) if re.search(URL_PATTERN, path))
    urls.remove(RING_CONFIG_URL)
    return urls

def load_tracker(fieldnames=None):
    try:
        with open("data_tracker.json", "r+", encoding="utf-8") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        data = {file: {} for file in fieldnames}
        with open("data_tracker.json", "w+", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))
    
def save_tracker(updated_data):
    with open("data_tracker.json", "w+", encoding="utf-8") as file:
        file.write(json.dumps(updated_data, indent=4))

def initial_data_pull():
    url_to_filename = {file: re.search(r'[^/]+$', file).group() for file in extract_unique_urls()}
    tracker = load_tracker(url_to_filename.values())
    for url, filename in url_to_filename.items():
        print(f"{url}start_date?{OURA_FIRST_DAY}")
        tracker[filename]["endpoint"] = url
        tracker[filename]["last_indexed"] = str(date.today()-timedelta(2))
        formatted_url = f"{url}?start_date={OURA_FIRST_DAY}&end_date={str(date.today()-timedelta(2))}"
        try:
            res = wrapper("GET", formatted_url)
            keys = res["data"][0].keys()
            write_csv_from_dicts(res["data"], keys, f"docs/csv/test/{filename}.csv")
            tracker[filename]["status"] = "Init data pull complete"
        except Exception as e:
            tracker[filename]["last_indexed"] = OURA_FIRST_DAY
            tracker[filename]["status"] = "No data found"

    save_tracker(tracker)

def process_new_data():
    tracker = load_tracker()
    for key, value in tracker.items():
        last_indexed = tracker[key]["last_indexed"]
        year, month, day = map(int, last_indexed.split("-"))
        date_obj = date(year, month, day)
        date_to_collect_from = date_obj + timedelta(1)
        endpoint = tracker[key]["endpoint"]
        try:
            res = wrapper("GET", f"{endpoint}?start_date={str(date_obj)}&end_date={str(date_to_collect_from)}")
            data_keys = res["data"][0].keys()
            file_path = f"docs/csv/test/{key}.csv"
            write_csv_from_dicts(res["data"], data_keys, file_path)
            tracker[key]["last_indexed"] = str(date_to_collect_from)
            tracker[key]["status"] = "data pulled"
        except Exception as e:
            print(e)
            tracker[key]["last_indexed"] = None
            tracker[key]["status"] = "Incomplete pull"

    save_tracker(tracker)

if __name__ == "__main__":
    initial_data_pull()
    # process_new_data()
	# print(extract_unique_urls())
