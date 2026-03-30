import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "raiz.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS toxins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    aliases TEXT,
    description TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    safe_threshold TEXT NOT NULL,
    organs_affected TEXT NOT NULL,
    natural_alternatives TEXT NOT NULL,
    category TEXT NOT NULL
);
"""

TOXIN_SEED_DATA: list[dict[str, Any]] = [
    {
        "name": "Red 40",
        "aliases": "allura red,fd&c red no. 40",
        "description": "A synthetic colorant linked to hyperactivity and possible inflammatory stress in sensitive people.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 7 mg/kg body weight per day.",
        "organs_affected": "brain,hormones",
        "natural_alternatives": "Beetroot powder (cook or blend), pomegranate juice (drink diluted), hibiscus petals (brew as tea)",
        "category": "food additive",
    },
    {
        "name": "BHA",
        "aliases": "butylated hydroxyanisole",
        "description": "A preservative that may disrupt hormones and has shown tumor-promoting effects in animal studies.",
        "risk_level": "high",
        "safe_threshold": "Avoid frequent intake; keep as close to zero as possible.",
        "organs_affected": "hormones,cancer risk,liver",
        "natural_alternatives": "Rosemary extract (cook with oils), vitamin E-rich sunflower seeds (eat raw), green tea (brew)",
        "category": "food additive",
    },
    {
        "name": "BHT",
        "aliases": "butylated hydroxytoluene",
        "description": "A synthetic preservative associated with oxidative stress and endocrine concerns at high intake.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 0.25 mg/kg body weight per day.",
        "organs_affected": "liver,hormones",
        "natural_alternatives": "Turmeric root (cook), rosemary herb (infuse in oil), almonds (eat raw)",
        "category": "food additive",
    },
    {
        "name": "High Fructose Corn Syrup",
        "aliases": "hfcs,corn syrup",
        "description": "A concentrated sweetener associated with insulin resistance and fatty liver when consumed regularly.",
        "risk_level": "high",
        "safe_threshold": "Limit added sugars to under 25 g daily (women) or 36 g daily (men).",
        "organs_affected": "liver,hormones,heart",
        "natural_alternatives": "Whole dates (blend into paste), ripe banana (mash), baked apple puree (cook)",
        "category": "sweetener",
    },
    {
        "name": "Sodium Nitrite",
        "aliases": "nitrite,e250",
        "description": "A curing agent that can form nitrosamines, compounds linked to higher cancer risk.",
        "risk_level": "high",
        "safe_threshold": "Keep under 0.07 mg/kg body weight per day.",
        "organs_affected": "cancer risk,heart",
        "natural_alternatives": "Celery powder (cook in broths), beet juice concentrate (cook), rosemary (cook)",
        "category": "preservative",
    },
    {
        "name": "Carrageenan",
        "aliases": "e407",
        "description": "A seaweed-derived thickener that may trigger gut inflammation in sensitive individuals.",
        "risk_level": "medium",
        "safe_threshold": "No formal ADI; avoid daily use if you have GI sensitivity.",
        "organs_affected": "gut,immune system",
        "natural_alternatives": "Chia seeds (soak), flaxseed gel (blend), agar agar (cook)",
        "category": "thickener",
    },
    {
        "name": "Aspartame",
        "aliases": "e951",
        "description": "An artificial sweetener that may cause headaches or mood effects in susceptible people.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 40 mg/kg body weight per day.",
        "organs_affected": "brain,hormones",
        "natural_alternatives": "Monk fruit (powder), stevia leaf (brew or powder), cinnamon (sprinkle)",
        "category": "sweetener",
    },
    {
        "name": "MSG",
        "aliases": "monosodium glutamate,e621",
        "description": "A flavor enhancer that can trigger headaches and flushing in sensitive individuals.",
        "risk_level": "low",
        "safe_threshold": "Keep occasional servings under 1.5 g.",
        "organs_affected": "brain,nervous system",
        "natural_alternatives": "Mushroom powder (cook), tomato paste (cook), kombu seaweed (simmer)",
        "category": "flavor enhancer",
    },
    {
        "name": "TBHQ",
        "aliases": "tertiary butylhydroquinone",
        "description": "A preservative used in oils and snacks that may stress immune and liver systems at higher levels.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 0.7 mg/kg body weight per day.",
        "organs_affected": "liver,immune system",
        "natural_alternatives": "Vitamin E rich sunflower seeds (eat raw), rosemary extract (cook), oregano (cook)",
        "category": "preservative",
    },
    {
        "name": "Titanium Dioxide",
        "aliases": "e171",
        "description": "A whitening pigment with nanoparticle concerns for DNA and gut health.",
        "risk_level": "high",
        "safe_threshold": "Best avoided; several regions have restricted food use.",
        "organs_affected": "gut,cancer risk",
        "natural_alternatives": "Rice flour (bake), coconut flour (bake), arrowroot powder (cook)",
        "category": "color/whitener",
    },
    {
        "name": "Sodium Benzoate",
        "aliases": "e211,benzoate",
        "description": "A preservative that may form benzene in some acidic beverages when paired with vitamin C and heat.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 5 mg/kg body weight per day.",
        "organs_affected": "liver,hormones",
        "natural_alternatives": "Lemon juice (fresh squeeze), apple cider vinegar (dilute), refrigeration with glass storage",
        "category": "preservative",
    },
    {
        "name": "Potassium Bromate",
        "aliases": "e924",
        "description": "A flour improver linked to kidney and thyroid toxicity in animal studies.",
        "risk_level": "high",
        "safe_threshold": "No safe dietary threshold recommended; avoid.",
        "organs_affected": "kidneys,hormones,cancer risk",
        "natural_alternatives": "Sourdough fermentation (bake), vitamin C powder from acerola (bake), unbleached whole flour",
        "category": "baking additive",
    },
    {
        "name": "Propyl Gallate",
        "aliases": "e310",
        "description": "An antioxidant preservative with potential endocrine-disrupting effects.",
        "risk_level": "medium",
        "safe_threshold": "Keep under 1.4 mg/kg body weight per day.",
        "organs_affected": "hormones,liver",
        "natural_alternatives": "Rosemary extract (cook), mixed tocopherols from seeds (eat raw), green tea polyphenols (brew)",
        "category": "preservative",
    },
    {
        "name": "Brominated Vegetable Oil",
        "aliases": "bvo",
        "description": "An emulsifier linked to thyroid and neurological accumulation concerns with chronic use.",
        "risk_level": "high",
        "safe_threshold": "Avoid routine intake; many products have phased it out.",
        "organs_affected": "brain,hormones",
        "natural_alternatives": "Citrus zest oils (blend), acacia gum (mix), fresh fruit infusions (brew)",
        "category": "emulsifier",
    },
    {
        "name": "Lead",
        "aliases": "pb",
        "description": "A heavy metal contaminant that can impair neurological and kidney function over time.",
        "risk_level": "high",
        "safe_threshold": "No safe blood level for children; keep exposure as low as possible.",
        "organs_affected": "brain,kidneys,blood",
        "natural_alternatives": "Quinoa (cook), hemp seeds (eat raw), black beans (cook)",
        "category": "heavy metal",
    },
    {
        "name": "Arsenic",
        "aliases": "as",
        "description": "A toxic metalloid linked to skin, cardiovascular, and cancer outcomes with chronic ingestion.",
        "risk_level": "high",
        "safe_threshold": "Drinking water guideline is 10 ppb; minimize supplemental exposure.",
        "organs_affected": "skin,heart,cancer risk",
        "natural_alternatives": "Amaranth (cook), lentils (cook), pumpkin seeds (eat raw)",
        "category": "heavy metal",
    },
    {
        "name": "Cadmium",
        "aliases": "cd",
        "description": "A heavy metal that accumulates in kidneys and bones and can damage filtration over time.",
        "risk_level": "high",
        "safe_threshold": "Keep weekly intake under 2.5 µg/kg body weight.",
        "organs_affected": "kidneys,bones",
        "natural_alternatives": "Chickpeas (cook), tempeh (cook), sesame seeds (eat raw)",
        "category": "heavy metal",
    },
    {
        "name": "Mercury",
        "aliases": "hg,methylmercury",
        "description": "A neurotoxic heavy metal that can affect brain development and nerve signaling.",
        "risk_level": "high",
        "safe_threshold": "Keep under 0.1 µg/kg body weight per day for methylmercury.",
        "organs_affected": "brain,nervous system,kidneys",
        "natural_alternatives": "Walnuts (eat raw), chia seeds (soak), algae-derived omega-3 oil",
        "category": "heavy metal",
    },
    {
        "name": "Magnesium Stearate",
        "aliases": "stearic acid magnesium salt",
        "description": "A supplement flow agent that may reduce dissolution speed in some low-quality tablets.",
        "risk_level": "low",
        "safe_threshold": "Generally recognized as low risk below 2500 mg/day.",
        "organs_affected": "gut",
        "natural_alternatives": "Whole-food magnesium from spinach (cook), pumpkin seeds (eat raw), cacao nibs (eat)",
        "category": "supplement filler",
    },
    {
        "name": "Silicon Dioxide",
        "aliases": "silica",
        "description": "An anti-caking additive with low dietary toxicity but unnecessary in many supplements.",
        "risk_level": "low",
        "safe_threshold": "No established ADI; keep occasional use.",
        "organs_affected": "lungs",
        "natural_alternatives": "Whole-food mineral blends: oats (cook), nettle leaf tea (brew), cucumber (eat raw)",
        "category": "supplement filler",
    },
    {
        "name": "Maltodextrin",
        "aliases": "modified starch",
        "description": "A rapidly absorbed starch that may spike blood sugar and alter gut microbiota balance.",
        "risk_level": "medium",
        "safe_threshold": "Keep added refined carbs minimal, especially with insulin resistance.",
        "organs_affected": "hormones,gut",
        "natural_alternatives": "Mashed sweet potato (cook), cooked oats, banana flour (cook)",
        "category": "supplement filler",
    },
    {
        "name": "Artificial Flavors",
        "aliases": "flavoring",
        "description": "A broad additive category that can hide solvent residues and sensitizing compounds.",
        "risk_level": "medium",
        "safe_threshold": "No single threshold; reduce frequent intake from ultra-processed foods.",
        "organs_affected": "liver,hormones",
        "natural_alternatives": "Vanilla bean (infuse), citrus peel (zest), cinnamon sticks (brew)",
        "category": "supplement filler",
    },
    {
        "name": "Soy Lecithin",
        "aliases": "lecithin,e322",
        "description": "An emulsifier that may bother people with soy sensitivity or digestive issues.",
        "risk_level": "low",
        "safe_threshold": "Generally low risk in small quantities.",
        "organs_affected": "gut,immune system",
        "natural_alternatives": "Sunflower lecithin (powder), chia gel (soak), flax gel (blend)",
        "category": "supplement filler",
    },
    {
        "name": "Glyphosate",
        "aliases": "roundup residue",
        "description": "A herbicide residue that may affect gut bacteria and cellular oxidative balance.",
        "risk_level": "high",
        "safe_threshold": "US EPA chronic reference dose is 1.75 mg/kg/day; aim for far lower.",
        "organs_affected": "gut,liver,cancer risk",
        "natural_alternatives": "Organic loose-leaf matcha (brew), organic green tea (brew), tulsi tea (brew)",
        "category": "pesticide",
    },
    {
        "name": "Chlorpyrifos",
        "aliases": "organophosphate",
        "description": "A neurotoxic pesticide associated with developmental and cognitive harm.",
        "risk_level": "high",
        "safe_threshold": "No safe exposure for children is widely accepted; avoid.",
        "organs_affected": "brain,nervous system,hormones",
        "natural_alternatives": "Organic mint tea (brew), organic tulsi tea (brew), ginger tea (brew)",
        "category": "pesticide",
    },
]

ADDITIONAL_TOXINS = [
    ("Acesulfame Potassium", "ace-k", "Artificial sweetener with uncertain long-term metabolic effects.", "medium", "Keep under 15 mg/kg/day.", "hormones,gut", "Stevia leaf (powder), monk fruit (powder), apple slices (eat raw)", "sweetener"),
    ("Sucralose", "splenda", "Non-nutritive sweetener that may alter gut microbiome in frequent use.", "medium", "Keep under 5 mg/kg/day.", "gut,hormones", "Cinnamon (sprinkle), date paste (blend), pear puree (cook)", "sweetener"),
    ("Saccharin", "e954", "Artificial sweetener sometimes linked to glucose intolerance.", "low", "Keep under 5 mg/kg/day.", "hormones,gut", "Stewed fruit (cook), licorice root tea (brew), monk fruit (powder)", "sweetener"),
    ("Sodium Phosphate", "phosphates", "Excess phosphate additives can burden kidneys and blood vessels.", "medium", "Limit total phosphate additives in renal risk groups.", "kidneys,heart", "Sesame seeds (eat raw), kale (cook), moringa tea (brew)", "mineral additive"),
    ("Disodium EDTA", "edta", "Chelating preservative that may affect mineral absorption with high intake.", "low", "Avoid frequent high-dose exposure.", "kidneys,gut", "Lemon juice (fresh), rosemary (cook), refrigeration methods", "preservative"),
    ("Polysorbate 80", "e433", "Emulsifier tied to gut barrier concerns in animal models.", "medium", "No clear ADI; reduce routine intake.", "gut,immune system", "Sunflower lecithin (powder), chia gel (soak), olive oil emulsions (blend)", "emulsifier"),
    ("Carboxymethylcellulose", "cmc", "Thickener associated with microbiome disruption in sensitive users.", "medium", "No specific ADI; avoid daily high intake.", "gut,immune system", "Pectin from apples (cook), chia gel (soak), okra broth (cook)", "thickener"),
    ("Yellow 5", "tartrazine", "Synthetic dye linked to behavioral reactions and allergies in some individuals.", "medium", "Keep under 7.5 mg/kg/day.", "brain,immune system", "Turmeric (cook), saffron (brew), carrot juice (drink)", "food additive"),
    ("Yellow 6", "sunset yellow", "Synthetic food dye with sensitivity and inflammation concerns.", "medium", "Keep under 3.75 mg/kg/day.", "brain,immune system", "Annatto (cook), paprika (cook), mango puree (blend)", "food additive"),
    ("Blue 1", "brilliant blue", "Artificial dye potentially linked to hypersensitivity.", "low", "Keep under 6 mg/kg/day.", "immune system", "Butterfly pea flower (brew), blueberry puree (blend), purple cabbage extract (cook)", "food additive"),
    ("Blue 2", "indigotine", "Synthetic dye with limited long-term safety data.", "low", "Keep under 2.5 mg/kg/day.", "immune system", "Butterfly pea flower (brew), blackberry juice (drink), spirulina (powder)", "food additive"),
    ("Sulfites", "sulfur dioxide", "Preservatives that can trigger asthma and headaches.", "medium", "Keep under 0.7 mg/kg/day.", "lungs,immune system", "Lemon juice (fresh), refrigeration, rosemary (cook)", "preservative"),
    ("Sodium Metabisulfite", "e223", "Sulfite preservative associated with respiratory irritation.", "medium", "Included in sulfite total under 0.7 mg/kg/day.", "lungs,immune system", "Vinegar pickling (cook), lemon juice (fresh), celery seed (cook)", "preservative"),
    ("Nitrates", "sodium nitrate", "Curing agents that can form nitrosamines during high-heat cooking.", "medium", "Keep processed meat intake low.", "cancer risk,heart", "Beetroot (cook), celery powder (cook), rosemary (cook)", "preservative"),
    ("Propylene Glycol", "e1520", "Solvent additive that can burden kidneys in excessive intake.", "low", "Keep under 25 mg/kg/day.", "kidneys,liver", "Vegetable glycerin from natural sources (minimal), coconut water (drink), aloe vera juice (drink)", "solvent"),
    ("Potassium Sorbate", "e202", "Preservative that may irritate skin and mucosa in sensitive users.", "low", "Keep under 25 mg/kg/day.", "immune system,skin", "Fermentation (cook), refrigeration, lemon peel oils (infuse)", "preservative"),
    ("Calcium Disodium EDTA", "e385", "Preservative/chelator that may influence mineral balance.", "low", "Keep under 2.5 mg/kg/day.", "kidneys,gut", "Lemon juice (fresh), rosemary (cook), glass storage", "preservative"),
    ("Azodicarbonamide", "ada", "Dough conditioner with respiratory concerns in occupational exposure.", "high", "Avoid whenever possible.", "lungs,cancer risk", "Sourdough starter (bake), unbleached flour, psyllium husk (bake)", "baking additive"),
    ("DATEM", "diacetyl tartaric acid esters", "Emulsifier that may increase gut inflammation in sensitive individuals.", "medium", "No clear ADI; reduce frequent use.", "gut", "Lecithin from sunflower (powder), egg yolk (cook), flax gel (blend)", "emulsifier"),
    ("Monocalcium Phosphate", "mcp", "Leavening acid that contributes to phosphate load.", "low", "Moderate intake if kidney disease risk.", "kidneys,bones", "Lemon juice + baking soda (bake), cream of tartar (bake), sourdough", "baking additive"),
    ("Aluminum Silicate", "aluminosilicate", "Anti-caking agent with cumulative aluminum exposure concerns.", "medium", "Minimize cumulative aluminum additives.", "brain,bones", "Arrowroot powder (cook), rice flour (bake), tapioca starch (cook)", "anti-caking"),
    ("Aluminum Lake Dyes", "lake colors", "Pigmented dyes containing aluminum compounds.", "medium", "Avoid frequent intake in children.", "brain,immune system", "Beet powder (blend), turmeric (cook), spirulina (powder)", "color additive"),
    ("Butylated Starch", "modified food starch", "Highly processed starch that may spike glucose.", "low", "Use occasionally; avoid overreliance.", "hormones,gut", "Cooked oats, mashed yam (cook), cassava (cook)", "starch additive"),
    ("Polydextrose", "synthetic fiber", "Bulking fiber that can cause bloating in high amounts.", "low", "Limit if GI symptoms occur.", "gut", "Chia seeds (soak), flax meal (mix), pear (eat raw)", "fiber additive"),
    ("Hydrogenated Oils", "trans fat", "Industrial fats associated with inflammation and heart disease.", "high", "Keep trans fats as close to zero as possible.", "heart,liver", "Extra-virgin olive oil (cook low heat), avocado (eat raw), walnuts (eat raw)", "fat additive"),
    ("Partially Hydrogenated Oil", "pho", "Primary source of artificial trans fats in processed foods.", "high", "No safe level established.", "heart,cancer risk", "Olive oil (cook), sesame oil (cook), ground flaxseed (mix)", "fat additive"),
    ("Corn Syrup Solids", "glucose syrup solids", "Concentrated sugar solids with metabolic burden.", "medium", "Limit added sugars under 10% of calories.", "liver,hormones", "Baked fruit puree (cook), date paste (blend), whole berries (eat raw)", "sweetener"),
    ("Sodium Aluminum Phosphate", "salp", "Leavening additive contributing sodium and aluminum load.", "medium", "Avoid frequent use.", "kidneys,brain", "Sourdough fermentation, cream of tartar (bake), lemon+baking soda", "baking additive"),
    ("Benzoic Acid", "e210", "Preservative precursor that may contribute to benzene formation with heat and vitamin C.", "medium", "Combined benzoate intake under 5 mg/kg/day.", "liver", "Lemon juice (fresh), vinegar (pickle), refrigeration", "preservative"),
    ("Sodium Erythorbate", "e316", "Curing accelerator often used with nitrites.", "low", "Generally low risk but reduce processed meats.", "heart,cancer risk", "Rosemary extract (cook), celery powder (cook), beetroot (cook)", "preservative"),
]


for item in ADDITIONAL_TOXINS:
    TOXIN_SEED_DATA.append(
        {
            "name": item[0],
            "aliases": item[1],
            "description": item[2],
            "risk_level": item[3],
            "safe_threshold": item[4],
            "organs_affected": item[5],
            "natural_alternatives": item[6],
            "category": item[7],
        }
    )


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()
        seed_toxins(conn)


def seed_toxins(conn: sqlite3.Connection) -> None:
    count = conn.execute("SELECT COUNT(*) FROM toxins").fetchone()[0]
    if count >= len(TOXIN_SEED_DATA):
        return

    for toxin in TOXIN_SEED_DATA:
        conn.execute(
            """
            INSERT OR IGNORE INTO toxins
            (name, aliases, description, risk_level, safe_threshold, organs_affected, natural_alternatives, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                toxin["name"],
                toxin["aliases"],
                toxin["description"],
                toxin["risk_level"],
                toxin["safe_threshold"],
                toxin["organs_affected"],
                toxin["natural_alternatives"],
                toxin["category"],
            ),
        )
    conn.commit()


def fetch_toxin_by_query(query: str) -> list[sqlite3.Row]:
    pattern = f"%{query.lower()}%"
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT * FROM toxins
            WHERE lower(name) LIKE ?
               OR lower(aliases) LIKE ?
            ORDER BY CASE risk_level
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3 END, name ASC
            """,
            (pattern, pattern),
        ).fetchall()


def fetch_all_toxins() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM toxins ORDER BY name ASC").fetchall()
