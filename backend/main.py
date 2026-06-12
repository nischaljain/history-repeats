import random
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

    facts = curate_facts(data)

    return {
        "date": today.isoformat(),
        "month": today.month,
        "day": today.day,
        "facts": facts,
    }


def curate_facts(data):
    # Pool all events, births, and deaths into one list
    all_items = []
    for category in ("events", "births", "deaths"):
        for item in data.get(category, []):
            if "year" in item and "text" in item:
                all_items.append({
                    "year": item["year"],
                    "text": item["text"],
                    "type": category,
                })

    # Group by century: year 1812 → century 19, year 450 → century 5
    by_century = {}
    for item in all_items:
        century = (item["year"] // 100) + 1
        if century not in by_century:
            by_century[century] = []
        by_century[century].append(item)

    # Pick one random fact from each century
    picks = []
    for century in sorted(by_century.keys()):
        picks.append(random.choice(by_century[century]))

    # Cap at 7 facts, spread evenly if we have more than 7 centuries
    if len(picks) > 7:
        step = len(picks) / 7
        picks = [picks[int(i * step)] for i in range(7)]

    return picks


# Serve frontend static files — must be last so it doesn't shadow API routes
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
