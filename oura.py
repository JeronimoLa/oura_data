import json
from datetime import datetime, date, timedelta

from helper import to_html, request

def find_weekday(object:dict) -> str:
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = datetime.strptime(object["day"], '%Y-%m-%d').date().weekday()
    return days_of_week[weekday]

def transform_daily_sleep_data(data) -> list:
    metrics = [
        {
            "day": find_weekday(obj),
            "date": obj["day"],
            "sleep score": obj["score"],
            **obj["contributors"]
        }
        for obj in data
    ]
    return metrics

def find_averages(records) -> dict:    
    sum_values = {}
    for record in records:
        for k, v in record.items():
            if isinstance(v, int):
                if k in sum_values:
                    sum_values[k] += v
                else:
                    sum_values[k] = v
    averages = { k: round(value/len(records),2) for k, value in sum_values.items() } 
    return averages    

def find_smallest(data) -> list:
    minimums = []
    weakest_state = {}
    for obj in data:
        minimum = float("inf")
        current_key = None
        date = obj["date"].replace("'", '"') 
        # print(date)
        for k, v in obj.items():
            if isinstance(v, int):
                if int(v) < minimum:
                    minimum = v
                    current_key = k
        weakest_state[date] = {}
        weakest_state[date] = {current_key: obj.get(current_key)}
        minimums.append(weakest_state)
        weakest_state = {}
    return minimums

def output_stats(metrics_data):
    print(to_html(metrics_data))
    averages = find_averages(metrics_data)
    print(f"<p>Averages: <p>\n")
    for key, val in averages.items():
        print(f"<p>{key}: {val}<p>")

    print(json.dumps(find_smallest(metrics_data), indent=4))

if __name__ == "__main__":
    todays_date = date.today()
    delta_time = todays_date-timedelta(7)
    # data = request("GET", "https://api.ouraring.com/v2/usercollection/daily_sleep", delta_time, todays_date)
    # cleaned_data = transform_daily_sleep_data(data)
    # output_stats(cleaned_data)

    # url = "https://api.ouraring.com/v2/usercollection/sleep_time"
    url = "https://api.ouraring.com/v2/usercollection/sleep"
    sleep_data = request("GET", url, delta_time)
    print(json.dumps(sleep_data, indent=4))