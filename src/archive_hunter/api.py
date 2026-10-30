from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .adapters import FixtureAdapter
from .review import build_review_queue
from .service import discover_opportunities

app = FastAPI(title="ARCHIVE HUNTER", version="0.1.0")
WEB_ROOT = Path(__file__).resolve().parents[2] / "web"


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(WEB_ROOT / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "fixture"}


@app.get("/opportunities")
def opportunities() -> list[dict]:
    return [asdict(item) for item in discover_opportunities(FixtureAdapter())]


@app.get("/review-queue")
def review_queue() -> list[dict]:
    return [asdict(item) for item in build_review_queue(discover_opportunities(FixtureAdapter()))]
