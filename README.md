# Raíz — Wellness & Food Toxin Scanner

Raíz is a full-stack web app that helps users identify potentially harmful ingredients in packaged foods, supplements, and beverages, then suggests natural whole-food and herbal alternatives.

> **Project status:** MVP complete — actively improving documentation and features.

🔗 **Live App:** [raiz-ghvy.onrender.com](https://raiz-ghvy.onrender.com)  
📖 **API Docs:** [raiz-ghvy.onrender.com/docs](https://raiz-ghvy.onrender.com/docs)

---

## Features

- Barcode lookup using Open Food Facts — scan any packaged product automatically
- Ingredient list analyzer — paste a full ingredient list and get a toxin report
- Single ingredient/chemical/supplement search — look up any chemical by name
- SQLite toxin database with 50+ entries including food dyes, heavy metals, pesticides, and supplement fillers
- Each flagged toxin shows: risk level, plain English description, organs affected, safe consumption threshold, and natural alternatives (whole foods, herbs, teas)
- Wellness-themed responsive frontend (lavender/beige/orange)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Data & ORM | SQLite, SQLAlchemy |
| External API | Open Food Facts |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

---

## Project Structure

```text
.
├── app/
│   ├── main.py        — FastAPI app + API routes
│   └── database.py    — SQLite init + toxin seed data + queries
├── static/
│   ├── index.html     — frontend
│   ├── styles.css     — theme and responsive design
│   └── app.js         — browser interactions with API
└── requirements.txt
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open: `http://127.0.0.1:8000`

---

## Example API Calls

### Product lookup by barcode

```bash
curl http://127.0.0.1:8000/api/product/737628064502
```

### Analyze an ingredient list

```bash
curl -X POST http://127.0.0.1:8000/api/analyze-ingredients \
  -H "Content-Type: application/json" \
  -d '{"ingredients":"water, high fructose corn syrup, red 40, sodium benzoate"}'
```

### Single ingredient search

```bash
curl "http://127.0.0.1:8000/api/search?query=glyphosate"
```

---

## Notes

- Database is seeded automatically at startup
- Risk levels: **High** = red · **Medium** = orange · **Low** = green
