"""
Matching Engine — MedTech Global Connect
=========================================
Computes a compatibility score between a manufacturer and an investor/partner
using a weighted combination of:

  1. Sector overlap        (categorical)      weight 0.35
  2. Semantic text sim.     (TF-IDF + cosine)  weight 0.35
  3. Geographic focus match (categorical)      weight 0.15
  4. Stage alignment        (categorical)      weight 0.15

Why TF-IDF/cosine instead of calling an external LLM API for this prototype:
this keeps the MVP fully offline/deterministic/free-to-run for the reviewer,
while remaining architecturally identical to a production setup where the
`text_similarity` step is swapped for embeddings from an LLM/embedding API
(e.g. OpenAI/Anthropic/Voyage embeddings) — see ARCHITECTURE.md, section
"AI Roadmap", for the production upgrade path.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _set_overlap_score(a: str, b: str) -> float:
    """Score overlap between two comma-separated string sets, 0..1."""
    set_a = {x.strip().lower() for x in a.split(",") if x.strip()}
    set_b = {x.strip().lower() for x in b.split(",") if x.strip()}
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    if not intersection:
        return 0.0
    return len(intersection) / min(len(set_a), len(set_b))


def _text_similarity(text_a: str, text_b: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([text_a, text_b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
    except ValueError:
        # e.g. empty vocabulary after stop-word removal
        return 0.0


def score_pair(manufacturer: dict, investor: dict) -> dict:
    # 1. Sector overlap — manufacturer.sector must appear in investor.sectors_of_interest
    sector_score = 1.0 if manufacturer["sector"].lower() in investor["sectors_of_interest"].lower() else 0.0

    # 2. Text similarity between manufacturer profile and investor thesis
    mfg_text = f"{manufacturer['sub_specialty']} {manufacturer['description']} {manufacturer['tags'].replace(',', ' ')}"
    inv_text = f"{investor['description']} {investor['sectors_of_interest'].replace(',', ' ')}"
    text_score = _text_similarity(mfg_text, inv_text)

    # 3. Geography overlap
    geo_score = _set_overlap_score(manufacturer["target_markets"], investor["geographic_focus"])

    # 4. Stage alignment
    stage_score = 1.0 if manufacturer["stage"].lower() in investor["stage_focus"].lower() else 0.0

    final = (
        0.35 * sector_score +
        0.35 * text_score +
        0.15 * geo_score +
        0.15 * stage_score
    )

    return {
        "score": round(final * 100, 1),          # 0-100 scale for readability
        "sector_score": round(sector_score * 100, 1),
        "text_similarity_score": round(text_score * 100, 1),
        "geography_score": round(geo_score * 100, 1),
        "stage_score": round(stage_score * 100, 1),
    }


def compute_all_matches(manufacturers: list, investors: list, top_n: int = 3) -> dict:
    """Returns {manufacturer_id: [ {investor, score...}, ... top_n ] }"""
    results = {}
    for m in manufacturers:
        scored = []
        for inv in investors:
            s = score_pair(m, inv)
            scored.append({**s, "investor": inv})
        scored.sort(key=lambda x: x["score"], reverse=True)
        results[m["id"]] = scored[:top_n]
    return results
