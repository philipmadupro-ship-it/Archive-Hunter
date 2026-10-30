from __future__ import annotations

from .adapters import SourceAdapter
from .models import Condition, Opportunity
from .scoring import DEFAULT_CONDITIONS, score_listing


def discover_opportunities(adapter: SourceAdapter, conditions: frozenset[Condition] = DEFAULT_CONDITIONS) -> list[Opportunity]:
    opportunities = [
        score_listing(listing, adapter.fetch_price_evidence(listing))
        for listing in adapter.fetch_listings()
        if listing.condition in conditions
    ]
    return sorted(opportunities, key=lambda item: item.opportunity_score, reverse=True)
