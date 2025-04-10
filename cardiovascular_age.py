import sys
import requests
from datetime import date, timedelta

from configuraton import CONFIG, OURA_FIRST_DAY

def vascular_age(start_date, end_date) -> list:
    url = "https://api.ouraring.com/v2/usercollection/daily_cardiovascular_age"

    params={ 
        'start_date': start_date, 
        'end_date': end_date 
    }
    headers = {'Authorization': f'Bearer {CONFIG["token"]}'}
    res = requests.request('GET', url, headers=headers, params=params).json()
    data = res["data"]
    return data

def to_html(data:list) -> str:
    html = """
    <style>
        p {
            margin: 0;
            padding: 0;
        }
        table, th, td {
            border:1px solid black;
        }
    </style> """
    html += '<table style="width:100%">\n'

    if isinstance(data, list):
        keys = data[0].keys()
        html += '<tr>\n'
        for key in keys:
            html += f'<th>{key}</th>\n'
        html += '</tr>\n'

        for item in data:
            values = list(item.values())
            html += f"<tr>"
            for i in range(len(values)):
                html += f'<td>{values[i]}</td>'
            html += f'</tr>\n'
        html += '</table>'

    elif isinstance(data, dict):
        pass
    else:
        print(f"Exiting...\nobj of type {type(data)} instead of list or dict")
        sys.exit()
    return html

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
    todays_date = date.today()
    delta_time = todays_date-timedelta(6)
    data = vascular_age(delta_time, todays_date)
    print(f"Cardiovascular average this past week: {delta_time} to {todays_date}")    
    print(to_html(data))
    
    print(f"Cardiovascular age frequency chart from: {OURA_FIRST_DAY} to {todays_date}")    
    all_data = vascular_age(OURA_FIRST_DAY, todays_date)
    stats = frequency_tracker(all_data)
    for k, v in sorted(stats.items()):
        print(f"{k}: {v[0]}")

if __name__ == "__main__":
    metrics()
    



