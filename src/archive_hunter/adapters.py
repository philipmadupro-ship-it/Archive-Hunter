from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from .models import AuthenticityStatus, Condition, EvidenceKind, Listing, PriceEvidence


class SourceAdapter(ABC):
    """Contract for approved APIs, partner feeds, user exports, or manual review."""

    name: str

    @abstractmethod
    def fetch_listings(self) -> list[Listing]:
        raise NotImplementedError

    @abstractmethod
    def fetch_price_evidence(self, listing: Listing) -> list[PriceEvidence]:
        raise NotImplementedError


class FixtureAdapter(SourceAdapter):
    """Local demonstration data; it makes no network calls and represents no marketplace."""

    name = "fixture"

    def fetch_listings(self) -> list[Listing]:
        return [
            Listing(
                id="listing-001",
                source=self.name,
                external_id="fixture-001",
                url="https://example.invalid/listings/fixture-001",
                title="1998 Helmut Lang Astro Biker Jacket",
                brand="Helmut Lang",
                country_code="FR",
                asking_price_eur=180.0,
                condition=Condition.VERY_GOOD,
                authenticity=AuthenticityStatus.SIGNALS_PRESENT,
                observed_at=datetime(2026, 10, 30, tzinfo=timezone.utc),
            )
        ]

    def fetch_price_evidence(self, listing: Listing) -> list[PriceEvidence]:
        observed_at = datetime(2026, 10, 30, tzinfo=timezone.utc)
        return [
            PriceEvidence("sold-1", self.name, "sold-1", EvidenceKind.SOLD, 365.0, observed_at, 0.95),
            PriceEvidence("sold-2", self.name, "sold-2", EvidenceKind.SOLD, 340.0, observed_at, 0.92),
            PriceEvidence("sold-3", self.name, "sold-3", EvidenceKind.SOLD, 390.0, observed_at, 0.88),
            PriceEvidence("asking-1", self.name, "asking-1", EvidenceKind.ASKING, 475.0, observed_at, 0.80),
        ]
