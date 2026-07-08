import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import init_db, seed_if_empty, get_connection
from matching import compute_all_matches, score_pair

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = FastAPI(title="MedTech Global Connect — MVP Prototype")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.on_event("startup")
def startup():
    init_db(reset=False)
    seed_if_empty()


def _row_to_dict(row):
    return dict(row)


def _fetch_all(table):
    conn = get_connection()
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


@app.get("/api/manufacturers")
def api_manufacturers():
    return _fetch_all("manufacturers")


@app.get("/api/investors")
def api_investors():
    return _fetch_all("investors")


@app.get("/api/matches/{manufacturer_id}")
def api_matches(manufacturer_id: int, top_n: int = 3):
    conn = get_connection()
    m = conn.execute("SELECT * FROM manufacturers WHERE id=?", (manufacturer_id,)).fetchone()
    investors = conn.execute("SELECT * FROM investors").fetchall()
    conn.close()
    if not m:
        return JSONResponse({"error": "manufacturer not found"}, status_code=404)
    m = dict(m)
    scored = []
    for inv in investors:
        inv = dict(inv)
        s = score_pair(m, inv)
        scored.append({**s, "investor": inv})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return {"manufacturer": m, "matches": scored[:top_n]}


@app.get("/")
def dashboard(request: Request):
    manufacturers = _fetch_all("manufacturers")
    investors = _fetch_all("investors")
    all_matches = compute_all_matches(manufacturers, investors, top_n=3)
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "manufacturers": manufacturers,
            "investors": investors,
            "matches": all_matches,
        },
    )


@app.get("/manufacturer/{manufacturer_id}")
def manufacturer_detail(request: Request, manufacturer_id: int):
    conn = get_connection()
    m = conn.execute("SELECT * FROM manufacturers WHERE id=?", (manufacturer_id,)).fetchone()
    investors = conn.execute("SELECT * FROM investors").fetchall()
    conn.close()
    m = dict(m)
    scored = []
    for inv in investors:
        inv = dict(inv)
        s = score_pair(m, inv)
        scored.append({**s, "investor": inv})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return templates.TemplateResponse(
        request,
        "manufacturer_detail.html",
        {"manufacturer": m, "matches": scored},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
