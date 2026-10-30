from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Condition(str, Enum):
    GOOD = "good"
    VERY_GOOD = "very_good"
    NEW_WITH_TAGS = "new_with_tags"
    OTHER = "other"


class AuthenticityStatus(str, Enum):
    UNVERIFIED = "unverified"
    SIGNALS_PRESENT = "signals_present"
    AUTHENTICATED = "authenticated"
    REJECTED = "rejected"


class EvidenceKind(str, Enum):
    SOLD = "sold"
    ASKING = "asking"


@dataclass(frozen=True)
class Listing:
    id: str
    source: str
    external_id: str
    url: str
    title: str
    brand: str
    country_code: str
    asking_price_eur: float
    condition: Condition
    authenticity: AuthenticityStatus
    observed_at: datetime


@dataclass(frozen=True)
class PriceEvidence:
    id: str
    source: str
    source_reference: str
    kind: EvidenceKind
    price_eur: float
    observed_at: datetime
    comparable_confidence: float


@dataclass(frozen=True)
class Opportunity:
    listing: Listing
    fair_value_eur: float | None
    sold_comparable_count: int
    asking_comparable_count: int
    liquidity_score: int
    opportunity_score: int
    resale_floor_met: bool
    authenticity_note: str
    rationale: tuple[str, ...]
