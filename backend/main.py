import random
from datetime import date
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

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
        resp = await client.get(url, headers={"User-Agent": "OnThisDay/1.0 (https://github.com/nischaljain/history-repeats; nischaljain@github)"})
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
                text = item["text"]
                if category == "births":
                    text = text + " is born."
                elif category == "deaths":
                    text = text + " dies."

                all_items.append({
                    "year": item["year"],
                    "text": text,
                })

    # Pick up to 7 distinct random facts from the whole pool so every
    # refresh produces a visibly different set, then order them
    # chronologically so the carousel reads as a timeline.
    picks = random.sample(all_items, min(7, len(all_items)))
    picks.sort(key=lambda item: item["year"])

    return picks


# Serve frontend static files — must be last so it doesn't shadow API routes
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
