# Raíz — Ingredient & Toxin Scanner

Raíz analyzes ingredient labels from packaged foods, supplements, and beverages to identify harmful chemicals — and suggests safer, whole-food and herbal alternatives rooted in nature.

## Live Deployments

| Version | URL | Description |
|---|---|---|
| **Portfolio** | [keila0323.github.io/Raiz](https://keila0323.github.io/Raiz) | Redesigned editorial frontend — split layout, instant load |
| **Full App** | [raiz-ghvy.onrender.com](https://raiz-ghvy.onrender.com) | Full-stack deployment with FastAPI backend |

## Features

- **Barcode Search** — enter a product barcode to fetch ingredients from Open Food Facts automatically
- **Ingredient List Analysis** — paste a full ingredient list from any product label and run a toxin scan
- **Single Ingredient Search** — search a specific ingredient, chemical, or supplement additive by name
- **Risk Scoring** — each flagged ingredient is rated low / medium / high with organ impact details
- **Natural Alternatives** — curated whole-food and herbal substitutes for flagged ingredients

## Tech Stack

- **Backend:** Python, FastAPI, SQLite
- **AI:** OpenAI GPT-4o
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Data:** Open Food Facts API
- **Deployment:** Render (backend), GitHub Pages (frontend)
