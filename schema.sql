-- MedTech Global Connect — Database Schema (MVP)
-- SQLite syntax (production target: PostgreSQL — see ARCHITECTURE.md)

CREATE TABLE manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT,
    sector TEXT NOT NULL,             -- one of: Pharmaceuticals, Nutraceuticals,
                                       -- Consumer Health Products, Medical Supplies,
                                       -- Medical Devices, MedTech
    sub_specialty TEXT,
    description TEXT,
    tags TEXT,                        -- comma-separated keywords (used by matching engine)
    certifications TEXT,              -- comma-separated (GMP, ISO 13485, CE, FDA 510k...)
    target_markets TEXT,              -- comma-separated regions the manufacturer wants to reach
    company_size TEXT,                -- startup / medium / large
    stage TEXT,                       -- early / growth / established
    annual_revenue_usd_m REAL
);

CREATE TABLE investors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,               -- Investor / Strategic Partner / Distributor
    country TEXT NOT NULL,
    sectors_of_interest TEXT,         -- comma-separated, matches manufacturers.sector values
    description TEXT,                 -- investment thesis / partnership focus (free text)
    geographic_focus TEXT,            -- comma-separated regions
    stage_focus TEXT,                 -- comma-separated: early / growth / established
    ticket_size_usd_m TEXT            -- free text range, e.g. "1-5", or "N/A" for distributors
);

-- Cached/persisted match results (recomputed on demand; this table lets the
-- roadmap add scheduled re-scoring, manual overrides, and match history later)
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(id),
    investor_id INTEGER NOT NULL REFERENCES investors(id),
    score REAL NOT NULL,              -- 0-100 overall weighted score
    sector_score REAL,                -- 0-100
    text_similarity_score REAL,       -- 0-100 (TF-IDF/cosine today, embeddings in v2)
    geography_score REAL,             -- 0-100
    stage_score REAL                  -- 0-100
);

-- Indexes to support the dashboard/detail queries
CREATE INDEX idx_manufacturers_sector ON manufacturers(sector);
CREATE INDEX idx_investors_sectors ON investors(sectors_of_interest);
CREATE INDEX idx_matches_manufacturer ON matches(manufacturer_id);
CREATE INDEX idx_matches_investor ON matches(investor_id);
