# Raíz — Wellness & Food Toxin Scanner

Raíz is a full-stack FastAPI web app that helps users identify potentially harmful ingredients in packaged foods, supplements, and beverages, then suggests natural whole-food/herbal alternatives.

## Features

- Barcode lookup using Open Food Facts (`/api/product/{barcode}`)
- Ingredient list analyzer with toxin flagging (`/api/analyze-ingredients`)
- Single ingredient/chemical/supplement search (`/api/search?query=`)
- SQLite toxin database seeded on startup with 50+ entries
- Wellness-themed responsive frontend (lavender/beige/orange)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open: `http://127.0.0.1:8000`

## Example API calls

### 1) Product lookup by barcode

```bash
curl http://127.0.0.1:8000/api/product/737628064502
```

### 2) Analyze ingredients list

```bash
curl -X POST http://127.0.0.1:8000/api/analyze-ingredients \
  -H "Content-Type: application/json" \
  -d '{"ingredients":"water, high fructose corn syrup, red 40, sodium benzoate"}'
```

### 3) Single ingredient search

```bash
curl "http://127.0.0.1:8000/api/search?query=glyphosate"
```

## Project structure

- `app/main.py` — FastAPI app + API routes
- `app/database.py` — SQLite init + toxin seed data + queries
- `static/index.html` — frontend
- `static/styles.css` — theme and responsive design
- `static/app.js` — browser interactions with API
- `raiz.db` — auto-created SQLite DB

## Notes

- Database is seeded at application startup.
- Risk indicators:
  - **High** = red
  - **Medium** = orange
  - **Low** = green
