from datetime import datetime, date, timedelta
from helper import to_html, request

def find_weekday(object:dict) -> str:
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = datetime.strptime(object["day"], '%Y-%m-%d').date().weekday()
    return days_of_week[weekday]

def date_range_from_today(days: int):
    return 	{ 
        'start_date': (date.today()-timedelta(days)).strftime("%Y-%m-%d"),
        'end_date': date.today().strftime("%Y-%m-%d")
    }

def transform_daily_sleep_data(data:list) -> list:
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

def vasular_age_frequency_tracker(num_of_days:int) -> dict:
    time_frame = date_range_from_today(num_of_days)
    print(f"Cardiovascular average from: {time_frame["start_date"]} to {time_frame["end_date"]}")    
    data = request("GET", "/v2/usercollection/daily_cardiovascular_age", today_date_range=time_frame)
    frequency = {}
    for date in data:
        if date["vascular_age"] not in frequency:
            frequency[date["vascular_age"]] = [1, [date["day"]]]
            continue
        frequency[date["vascular_age"]][0] += 1 
        frequency[date["vascular_age"]][1].append(date["day"]) 
    # print(frequency) # <- [occurrence, [date where it occured]] this is a list does it make sense for it to be a dictionary and leave the list with dates
    for k, v in sorted(frequency.items()):
        print(f"{k}: {v[0]}")
    return frequency

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
    print(metrics_data)
    print(to_html(metrics_data))
    averages = find_averages(metrics_data)
    print(f"<p>Averages: <p>\n")
    for key, val in averages.items():
        print(f"<p>{key}: {val}<p>")
    # print(json.dumps(find_smallest(metrics_data), indent=4))

def total_sleep(sleep_data):
    date = "2025-04-01"
    for i in range(len(sleep_data)):
        # print(type(sleep_data[i]["day"]))
        if sleep_data[i]["day"] == date:
            for k, v in sleep_data[i].items():
                print(f"{k} = {v}")
            # print(sleep_data[i])
            
    print(sleep_data[0]["day"])
    for day in sleep_data:
        if day["type"] == "long_sleep":
            # temp = {}
            # for key, value in day.items():
                # temp[key] = isinstance(value) # find out what the value type is to store in a database for daily updates and calls
            # print(temp)
            ds = datetime.strptime(day["bedtime_start"], "%Y-%m-%dT%H:%M:%S%z")
            de = datetime.strptime(day["bedtime_end"], "%Y-%m-%dT%H:%M:%S%z")
            duration = de - ds
            formatted_time_ds = ds.strftime("%I:%M:%S %p")
            formatted_time_de = de.strftime("%I:%M:%S %p")
            print(f"In bed from {formatted_time_ds} to {formatted_time_de} on {day["day"]}")
            print(f"duration -> {duration}")
            print(day["time_in_bed"])


def main():
    #### Debugging Daily High-level Sleep Data ####
    todays_date = date.today()
    delta_time = todays_date-timedelta(30)

    data = request("GET", "/v2/usercollection/daily_sleep", start_date=delta_time, end_date=todays_date)
    cleaned_data = transform_daily_sleep_data(data)
    # output_stats(cleaned_data)
    # print(cleaned_data)
    

    #### Investigating detailed sleep metrics ####
    #url = "https://api.ouraring.com/v2/usercollection/sleep"
    # sleep_data = request("GET", url, delta_time)
    # print(sleep_data)
    # total_sleep(sleep_data)
    # print(json.dumps(sleep_data, indent=4))

    #### Cardiovascular Age ####
    vasular_age_frequency_tracker(30)

if __name__ == "__main__":
    main()