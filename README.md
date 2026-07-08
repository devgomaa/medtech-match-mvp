# MedTech Global Connect — MVP Prototype

An AI-assisted matching platform connecting medical-sector manufacturers
(Pharmaceuticals, Nutraceuticals, Consumer Health, Medical Supplies, Medical
Devices, MedTech) — starting with China — to global investors and
distribution partners.

Built as a take-home technical challenge. **All data is synthetic** (no real
companies, people, or investors are represented).

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the system design, MVP scope
decisions, matching methodology, and the AI upgrade roadmap. See
[`NOTES.md`](./NOTES.md) for the "what I'd do with one more week" note.

## What this MVP does

- Stores structured profiles for manufacturers and investors/partners
- Scores every manufacturer × investor pair on 4 weighted factors (sector fit,
  text/semantic similarity via TF-IDF + cosine similarity, geographic focus,
  investment-stage alignment)
- Shows a ranked, explainable match list per manufacturer (dashboard + detail
  view), with the score breakdown visible — not just a black-box number
- Exposes the same logic via a small REST API for reuse by any future client

## Tech stack

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Matching**: scikit-learn (TF-IDF vectorizer + cosine similarity) + rule-based scoring
- **Storage**: SQLite (zero-setup for review; swappable to PostgreSQL, see ARCHITECTURE.md)
- **Frontend**: Server-rendered HTML (Jinja2) + minimal CSS — no JS framework, to keep the MVP fast to build and easy to review
- **Data**: Synthetic seed data (`backend/seed_data.py`) — 8 manufacturers, 6 investors/partners

## How AI was used to build this

- Used an AI coding assistant (Claude) to scaffold the FastAPI project
  structure, generate the synthetic dataset, and implement/debug the matching
  engine and templates within the time-boxed window — the kind of
  AI-accelerated workflow this role is evaluating for.
- The **product itself** also uses AI/ML (TF-IDF + cosine similarity for
  semantic matching) as a deliberately simple, offline-runnable stand-in for
  an embeddings-based production pipeline — see `ARCHITECTURE.md` §5 for the
  exact upgrade path to LLM/embedding APIs.

## Project structure

```
medtech-platform/
├── README.md
├── ARCHITECTURE.md
├── NOTES.md
├── schema.sql                  # standalone reference copy of the DB schema
├── backend/
│   ├── main.py                 # FastAPI app: routes + API
│   ├── database.py             # SQLite connection, schema, seeding
│   ├── matching.py             # matching engine (scoring logic)
│   ├── seed_data.py            # synthetic manufacturers & investors
│   └── requirements.txt
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── manufacturer_detail.html
├── static/                     # static assets (placeholder)
└── data/                       # SQLite DB file is created here at runtime
```

## Running it locally

Requirements: Python 3.10+

```bash
cd medtech-platform
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

cd backend
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000** for the dashboard.

The SQLite database is created automatically on first run and seeded with
synthetic data — no manual setup step needed.

### API endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Dashboard — all manufacturers with top-3 matches each |
| `GET /manufacturer/{id}` | Detail page — full match breakdown vs. every investor/partner |
| `GET /api/manufacturers` | JSON list of all manufacturers |
| `GET /api/investors` | JSON list of all investors/partners |
| `GET /api/matches/{manufacturer_id}?top_n=3` | JSON ranked matches for one manufacturer |

## Notes

- Only synthetic data is used, per the challenge instructions.
- Code quality/decisions are explained inline as comments and in
  `ARCHITECTURE.md`, rather than optimizing for line count or feature count.
