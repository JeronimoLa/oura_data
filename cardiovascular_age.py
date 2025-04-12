from datetime import date, timedelta

from helper import to_html, request
from configuraton import CONFIG, OURA_FIRST_DAY

def frequency_tracker(data:list) -> dict:
    frequency = {}
    for date in data:
        if date["vascular_age"] not in frequency:
            frequency[date["vascular_age"]] = [1, [date["day"]]]
            continue
        frequency[date["vascular_age"]][0] += 1 
        frequency[date["vascular_age"]][1].append(date["day"]) 
    return frequency # ex 23: [occurrences, [dates]]

def metrics():
    url = "https://api.ouraring.com/v2/usercollection/daily_cardiovascular_age"
    todays_date = date.today()
    delta_time = todays_date-timedelta(6)
    data = request("GET", url, delta_time, todays_date)
    print(f"Cardiovascular average this past week: {delta_time} to {todays_date}")    
    print(to_html(data))
    
    print(f"Cardiovascular age frequency chart from: {OURA_FIRST_DAY} to {todays_date}")    
    all_data = request("GET", url, OURA_FIRST_DAY, todays_date)
    stats = frequency_tracker(all_data)
    for k, v in sorted(stats.items()):
        print(f"{k}: {v[0]}")

if __name__ == "__main__":
    metrics()
    



