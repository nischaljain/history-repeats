from datetime import date

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

WIKIPEDIA_API = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"


@app.get("/api/events")
async def get_events():
    today = date.today()
    url = f"{WIKIPEDIA_API}/all/{today.month:02d}/{today.day:02d}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"User-Agent": "HistoryRepeats/1.0"})
        resp.raise_for_status()
        data = resp.json()

    return {
        "date": today.isoformat(),
        "month": today.month,
        "day": today.day,
        "events": data.get("events", []),
        "births": data.get("births", []),
        "deaths": data.get("deaths", []),
        "holidays": data.get("holidays", []),
    }


# Serve frontend static files — must be last so it doesn't shadow API routes
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
