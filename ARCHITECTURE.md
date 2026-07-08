# Architecture — MedTech Global Connect (MVP)

## 1. Problem & Goal

Connect Chinese medical-sector manufacturers (Pharma, Nutraceuticals, Consumer
Health, Medical Supplies, Medical Devices, MedTech) with the right investors
and distribution partners globally, based on sector fit, product/company
profile, geography, and investment stage — with the platform designed to
scale to more countries and manufacturer sources later.

## 2. What I built first, and what I deliberately deferred

### Built now (MVP core loop)
- Structured data model for manufacturers and investors/partners (see `schema.sql`)
- A working **matching engine** that scores every manufacturer against every
  investor/partner on four dimensions and returns ranked recommendations
- A minimal web UI (dashboard + detail view) to browse manufacturers and see
  their top matches with a transparent score breakdown
- A REST API (`/api/manufacturers`, `/api/investors`, `/api/matches/{id}`)
  so the matching logic is reusable by a future frontend, CRM integration, or
  outreach-automation workflow
- Synthetic seed data covering all 6 sectors and both investor/partner types

### Deferred on purpose (with reasoning)
| Deferred | Why it's safe to defer for an MVP |
|---|---|
| User accounts / auth / roles | Not needed to validate the core matching value proposition |
| Manual profile submission forms | Seed data proves the schema; forms are a straightforward CRUD addition once the schema is validated with real users |
| Real LLM/embeddings-based semantic matching | TF-IDF/cosine already proves the *architecture* of the scoring pipeline; swapping in embeddings is a contained, low-risk upgrade (see §5) |
| Multi-country expansion beyond China | The schema already stores `country` per manufacturer, so this is a data-population task, not a redesign |
| Outreach/CRM workflow (intro emails, deal tracking) | High value, but a distinct product surface — belongs in v2 once matching quality is validated |
| Admin dashboard for manually re-weighting the scoring formula | Useful, but premature before we have real feedback on which factor should be weighted higher |

The guiding principle: **prove the matching loop end-to-end with real
structure and a real (if simple) scoring algorithm**, rather than polishing
any single layer in isolation.

## 3. System Architecture (MVP)

```
┌─────────────────────────────┐
│        Browser (UI)          │  Jinja2-rendered dashboard + detail pages
└──────────────┬───────────────┘
               │ HTTP
┌──────────────▼───────────────┐
│      FastAPI application      │  main.py — routes for pages + JSON API
│  ┌──────────────────────────┐ │
│  │   Matching Engine         │ │  matching.py — sector / text / geo / stage
│  │  (TF-IDF + cosine + rules)│ │  scoring, weighted composite score
│  └──────────────────────────┘ │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│         SQLite database       │  manufacturers, investors, matches
└───────────────────────────────┘
```

Single deployable service for the MVP — deliberately monolithic. This keeps
the 24-hour build realistic and testable end-to-end, while every layer
(routing, matching, storage) is already separated cleanly enough to extract
into services later without a rewrite.

## 4. Matching Methodology

Each manufacturer × investor pair gets a weighted composite score (0-100):

| Factor | Weight | Method |
|---|---|---|
| Sector overlap | 35% | Categorical match: is the manufacturer's sector in the investor's stated sectors of interest? |
| Text/semantic similarity | 35% | TF-IDF vectorization of manufacturer description+tags vs. investor thesis, scored by cosine similarity |
| Geographic focus | 15% | Overlap between manufacturer's target markets and investor's geographic focus |
| Stage alignment | 15% | Does the manufacturer's stage (early/growth/established) match the investor's stated stage focus? |

The score breakdown (not just the final number) is exposed in the API and UI
so a human reviewer can see *why* a match was suggested — important for a
brokered introduction, where "black box" scores would undermine trust with a
matchmaking team.

## 5. AI Roadmap (production upgrade path)

The MVP already uses a real (if simple) AI/ML technique — TF-IDF + cosine
similarity — for the semantic-matching component, chosen deliberately over
calling an external LLM/embedding API so the prototype runs fully offline,
deterministically, and free of API-key/cost dependencies for review.

The upgrade path to a production-grade AI layer is a **contained swap**, not
a redesign, because the matching engine already isolates the text-similarity
step behind one function (`_text_similarity` in `matching.py`):

1. **v1.1 — Embeddings-based similarity**: replace TF-IDF with embeddings
   (e.g. OpenAI/Voyage/Anthropic-compatible embedding models) for manufacturer
   and investor text, stored in a vector index (pgvector or a dedicated vector
   DB) for fast top-K retrieval as the manufacturer/investor count grows.
2. **v1.2 — LLM-assisted profile enrichment**: use an LLM to normalize and
   enrich free-text manufacturer submissions (auto-tag sector/sub-specialty,
   flag missing certifications) so match quality doesn't depend on manual data
   entry discipline.
3. **v1.3 — LLM-generated match rationale**: instead of only a score
   breakdown, generate a short natural-language explanation of *why* a given
   investor is a strong fit — useful directly in outreach emails.
4. **v2 — Feedback-driven re-weighting**: once matches are actually acted on,
   log outcomes (intro accepted/declined/deal closed) and use that signal to
   learn better feature weights than the fixed 35/35/15/15 split used today.

## 6. Scalability Notes

- SQLite → PostgreSQL is a one-line connection-string change; the schema uses
  no SQLite-specific features.
- The matching computation is O(manufacturers × investors); at MVP scale
  (dozens to low hundreds of records) this is instant. Beyond a few thousand
  records, matches should be precomputed on a schedule (or on write) and
  served from the `matches` table instead of computed per request — the table
  already exists in the schema for this reason.
- Sector/geography values are currently free-text-with-convention; a
  production version should move them to reference tables/enums to guarantee
  clean matching as more countries and sectors are added.
