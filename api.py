from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from datetime import date, timedelta

from helper import request
from oura import transform_daily_sleep_data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]  # You can restrict this to specific origins for better security
)

@app.get("/metrics")
async def root():
    todays_date = date.today()
    delta_time = todays_date-timedelta(30)
    response = request("GET", "https://api.ouraring.com/v2/usercollection/daily_sleep", delta_time, todays_date)
    cleaned_data = transform_daily_sleep_data(response)
    collection, dates, keys = [], [], []
    for days in cleaned_data:
        for key, value in days.items():
            if isinstance(value, int):
                if key in keys:
                    index = keys.index(key)
                    collection[index]["data"].append(value)
                else:
                    keys.append(key)
                    value = days.get(key)
                    collection.append({
                        "name": key,
                        "data": [value]
                    })
        dates.append(days["date"])           
    return JSONResponse({"series": collection, "categories": dates})



