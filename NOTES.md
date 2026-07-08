# If I had one more week

Priority order, and why:

1. **Swap TF-IDF for real embeddings** (OpenAI/Voyage/Anthropic-compatible)
   and add a vector index. This is the single highest-leverage change to
   match quality, and the codebase is already structured so it's a contained
   change to one function (`matching._text_similarity`), not a rewrite.

2. **Manufacturer/investor self-service submission forms** with LLM-assisted
   auto-tagging (sector, sub-specialty, certifications extracted from free-text
   descriptions or uploaded company decks). This removes the dependency on
   manually curated seed data and is the real unlock for scaling beyond China.

3. **Match rationale generation** — a short LLM-written paragraph explaining
   *why* a specific investor/manufacturer pair scored well, ready to drop into
   an outreach email. This turns the matching engine from an internal ranking
   tool into something the matchmaking team can act on immediately.

4. **Precomputed/scheduled matching** — move from computing scores on every
   request to a background job that recomputes and stores scores in the
   `matches` table (already in the schema), triggered on new-profile creation
   or on a schedule. Needed once manufacturer/investor counts grow past a few
   hundred.

5. **Feedback loop** — log which suggested matches actually turned into real
   conversations/deals, and use that signal to tune the scoring weights
   (currently a fixed 35/35/15/15 split) instead of guessing at the right
   balance.

6. **Auth + basic CRM view** — investor/manufacturer accounts, saved matches,
   simple deal-stage tracking. Necessary before this becomes a real multi-user
   product, but deliberately out of scope for validating the matching core.

7. **Expand beyond China** — the schema already supports this (country is a
   plain field, not hardcoded), so this is primarily a data-sourcing and
   validation effort rather than an engineering one.
