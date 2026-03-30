import re
from typing import Any

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.database import fetch_all_toxins, fetch_toxin_by_query, init_db

app = FastAPI(title="Raíz API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class IngredientAnalyzeRequest(BaseModel):
    ingredients: str | list[str] = Field(..., description="Ingredient list as text or array")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def home() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/api/product/{barcode}")
def get_product_by_barcode(barcode: str) -> dict[str, Any]:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to reach Open Food Facts API.")

    payload = response.json()
    if payload.get("status") != 1:
        raise HTTPException(status_code=404, detail="Product not found for this barcode.")

    product = payload.get("product", {})
    ingredients_text = product.get("ingredients_text") or ""
    ingredients_tags = [i.get("text", "") for i in product.get("ingredients", []) if i.get("text")]
    parsed = split_ingredients(ingredients_text) if ingredients_text else ingredients_tags

    return {
        "barcode": barcode,
        "product_name": product.get("product_name", "Unknown product"),
        "brands": product.get("brands", "Unknown brand"),
        "ingredients": parsed,
        "raw_ingredients_text": ingredients_text,
    }


@app.post("/api/analyze-ingredients")
def analyze_ingredients(request: IngredientAnalyzeRequest) -> dict[str, Any]:
    ingredients = request.ingredients
    if isinstance(ingredients, str):
        ingredient_list = split_ingredients(ingredients)
    else:
        ingredient_list = [item.strip() for item in ingredients if item and item.strip()]

    flagged = []
    for ingredient in ingredient_list:
        matches = fetch_toxin_by_query(ingredient)
        for match in matches:
            flagged.append(format_toxin_record(match, ingredient))

    unique_flagged = dedupe_flagged(flagged)
    return {
        "input_ingredients": ingredient_list,
        "flagged_count": len(unique_flagged),
        "flagged_toxins": unique_flagged,
    }


@app.get("/api/search")
def search_single_ingredient(query: str) -> dict[str, Any]:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Please provide a valid ingredient query.")

    matches = [format_toxin_record(row, query) for row in fetch_toxin_by_query(query)]
    return {"query": query, "results": matches, "total": len(matches)}


@app.get("/api/toxins")
def list_toxins() -> dict[str, Any]:
    rows = [format_toxin_record(row, row["name"]) for row in fetch_all_toxins()]
    return {"total": len(rows), "toxins": rows}


def split_ingredients(raw: str) -> list[str]:
    cleaned = re.sub(r"[\n\r]", " ", raw)
    parts = re.split(r"[,;]|\bcontains\b|\band\b", cleaned, flags=re.IGNORECASE)
    return [p.strip(" .()[]{}\t").lower() for p in parts if p.strip()]


def format_toxin_record(row: Any, matched_on: str) -> dict[str, Any]:
    alternatives = [item.strip() for item in row["natural_alternatives"].split(",")]
    return {
        "name": row["name"],
        "aliases": row["aliases"],
        "description": row["description"],
        "risk_level": row["risk_level"],
        "safe_threshold": row["safe_threshold"],
        "organs_affected": [part.strip() for part in row["organs_affected"].split(",")],
        "natural_alternatives": alternatives,
        "category": row["category"],
        "matched_on": matched_on,
    }


def dedupe_flagged(flagged: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    unique = []
    for item in flagged:
        if item["name"] in seen:
            continue
        seen.add(item["name"])
        unique.append(item)
    return sorted(unique, key=lambda x: (risk_sort(x["risk_level"]), x["name"]))


def risk_sort(level: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(level, 3)
