

import requests 
from configuraton import BASE_URL, CONFIG

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


if __name__ == "__main__":
    example()
