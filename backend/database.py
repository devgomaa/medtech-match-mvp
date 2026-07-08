import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "platform.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT,
    sector TEXT NOT NULL,
    sub_specialty TEXT,
    description TEXT,
    tags TEXT,                 -- comma-separated keywords
    certifications TEXT,
    target_markets TEXT,       -- comma-separated
    company_size TEXT,         -- startup / medium / large
    stage TEXT,                -- early / growth / established
    annual_revenue_usd_m REAL
);

CREATE TABLE IF NOT EXISTS investors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,        -- Investor / Strategic Partner / Distributor
    country TEXT NOT NULL,
    sectors_of_interest TEXT,  -- comma-separated, matches manufacturers.sector values
    description TEXT,
    geographic_focus TEXT,     -- comma-separated regions
    stage_focus TEXT,          -- comma-separated: early / growth / established
    ticket_size_usd_m TEXT
);

-- Persisted match results (recomputed on demand, cached here for the UI/API)
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    investor_id INTEGER NOT NULL,
    score REAL NOT NULL,
    sector_score REAL,
    text_similarity_score REAL,
    geography_score REAL,
    stage_score REAL,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (investor_id) REFERENCES investors(id)
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(reset=False):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def seed_if_empty():
    from seed_data import get_manufacturers, get_investors

    conn = get_connection()
    cur = conn.execute("SELECT COUNT(*) AS c FROM manufacturers")
    if cur.fetchone()["c"] == 0:
        for m in get_manufacturers():
            conn.execute(
                """INSERT INTO manufacturers
                (name, country, city, sector, sub_specialty, description, tags,
                 certifications, target_markets, company_size, stage, annual_revenue_usd_m)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (m["name"], m["country"], m["city"], m["sector"], m["sub_specialty"],
                 m["description"], m["tags"], m["certifications"], m["target_markets"],
                 m["company_size"], m["stage"], m["annual_revenue_usd_m"]),
            )
        for i in get_investors():
            conn.execute(
                """INSERT INTO investors
                (name, type, country, sectors_of_interest, description,
                 geographic_focus, stage_focus, ticket_size_usd_m)
                VALUES (?,?,?,?,?,?,?,?)""",
                (i["name"], i["type"], i["country"], i["sectors_of_interest"],
                 i["description"], i["geographic_focus"], i["stage_focus"], i["ticket_size_usd_m"]),
            )
        conn.commit()
    conn.close()
