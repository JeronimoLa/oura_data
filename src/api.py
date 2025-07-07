import asyncio, json

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List

from src.oura import format_weekly_sleep_data, get_sleep_chart_data, get_sleep_radial_data

app = FastAPI()

api_app = FastAPI(title="api app")

app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="public",html = True), name="index")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/sleep-chart")
async def sleep_chart():
    resp = JSONResponse(content=get_sleep_chart_data())
    resp.headers["Cache-Control"] = "public, max-age=600"
    return resp

@api_app.get("/sleep-radials")
async def sleep_radials():
    return get_sleep_radial_data()

@api_app.get("/weekly-sleep-data")
async def weekly_sleep_data():
    weekly_data = format_weekly_sleep_data()
    resp = JSONResponse(content=weekly_data)
    resp.headers["Cache-Control"] = "public, max-age=600"
    return resp

active_connections: List[WebSocket] = []

engine_vals = [25, 65, 57, 30, 38, 40, 84, 43, 69, 93, 19, 77, 6, 29, 60, 1, 95, 97, 34, 24, 54, 52, 3, 91, 72, 96, 35, 95, 89, 96, 2, 39, 32, 65, 29, 99, 22, 81, 48, 50, 66, 7, 37, 85, 47, 100, 39, 56, 78, 19, 79, 16, 2, 67, 50, 86, 67, 14, 3, 94, 59, 78, 51, 31, 1, 6, 23, 27, 86, 21, 62, 60, 29, 100, 9, 75, 17, 55, 58, 32, 35, 86, 85, 87, 45, 39, 63, 38, 68, 35, 7, 14, 42, 70, 51, 69, 37, 50, 94, 98]
torpedo_vals = [11, 87, 41, 4, 74, 8, 92, 73, 70, 49, 52, 2, 8, 26, 6, 58, 45, 91, 86, 90, 83, 61, 24, 90, 66, 87, 69, 70, 44, 64, 99, 86, 71, 70, 41, 82, 52, 6, 86, 73, 65, 83, 42, 97, 19, 47, 62, 27, 14, 56, 7, 74, 76, 16, 92, 22, 60, 47, 95, 81, 97, 96, 53, 45, 29, 19, 73, 38, 29, 43, 23, 17, 21, 20, 100, 69, 77, 7, 89, 44, 11, 55, 67, 40, 80, 69, 27, 92, 17, 27, 84, 77, 93, 83, 100, 5, 52, 32, 92, 94]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        for e, t in zip(engine_vals, torpedo_vals):
            await websocket.send_text(json.dumps({
                "Engine": e,
                "Torpedo": t
            }))
            await asyncio.sleep(0.5)
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await websocket.close()