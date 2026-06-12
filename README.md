# On This Day

A web app that shows historical events, births, and deaths that happened on today's date. Each visit surfaces 7 curated facts spanning different centuries, displayed as a swipeable carousel.

**Live:** https://on-this-day-nocv.onrender.com

## Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** Vanilla JavaScript, HTML, CSS
- **Data:** Wikipedia "On This Day" API
- **Hosting:** Render

## Run Locally

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start the server
cd backend
uvicorn main:app --reload
```

Then open http://localhost:8000
