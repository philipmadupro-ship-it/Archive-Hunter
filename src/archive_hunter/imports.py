from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO
from urllib.parse import urlparse

from .adapters import SourceAdapter
from .models import AuthenticityStatus, Condition, EvidenceKind, Listing, PriceEvidence

EUROPE_COUNTRY_CODES = frozenset({
    "AL", "AD", "AM", "AT", "AZ", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK",
    "EE", "FI", "FR", "GE", "DE", "GR", "HU", "IS", "IE", "IT", "KZ", "XK", "LV",
    "LI", "LT", "LU", "MT", "MD", "MC", "ME", "NL", "MK", "NO", "PL", "PT", "RO",
    "RU", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "TR", "UA", "GB", "VA",
})


class ImportValidationError(ValueError):
    """Raised when an authorized export cannot be safely normalized."""


def _required(row: dict[str, str], field: str, row_number: int) -> str:
    value = row.get(field, "").strip()
    if not value:
        raise ImportValidationError(f"Row {row_number}: {field} is required.")
    return value


def _price(value: str, field: str, row_number: int) -> float:
    try:
        price = float(value)
    except ValueError as error:
        raise ImportValidationError(f"Row {row_number}: {field} must be a number.") from error
    if price < 0:
        raise ImportValidationError(f"Row {row_number}: {field} cannot be negative.")
    return price


def _url(value: str, row_number: int) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ImportValidationError(f"Row {row_number}: url must be an absolute http(s) URL.")
    return value


class CsvImportAdapter(SourceAdapter):
    """Adapter for exports the operator is authorized to submit and use."""

    name = "manual_csv"

    def __init__(self, listings_csv: str, evidence_csv: str) -> None:
        self._listings = self._parse_listings(listings_csv)
        self._evidence_by_listing = self._parse_evidence(evidence_csv)

    def fetch_listings(self) -> list[Listing]:
        return list(self._listings)

    def fetch_price_evidence(self, listing: Listing) -> list[PriceEvidence]:
        return list(self._evidence_by_listing.get(listing.external_id, []))

    def _parse_listings(self, contents: str) -> list[Listing]:
        listings: list[Listing] = []
        seen_external_ids: set[str] = set()
        for row_number, row in enumerate(csv.DictReader(StringIO(contents)), start=2):
            external_id = _required(row, "external_id", row_number)
            if external_id in seen_external_ids:
                raise ImportValidationError(f"Row {row_number}: duplicate external_id {external_id!r}.")
            seen_external_ids.add(external_id)
            country_code = _required(row, "country_code", row_number).upper()
            if country_code not in EUROPE_COUNTRY_CODES:
                raise ImportValidationError(f"Row {row_number}: country_code must be within Europe.")
            try:
                condition = Condition(_required(row, "condition", row_number))
                authenticity = AuthenticityStatus(row.get("authenticity", "unverified").strip() or "unverified")
                observed_at = datetime.fromisoformat(_required(row, "observed_at", row_number).replace("Z", "+00:00"))
            except ValueError as error:
                raise ImportValidationError(f"Row {row_number}: invalid condition, authenticity, or observed_at.") from error
            listings.append(Listing(
                id=f"manual-{external_id}", source=self.name, external_id=external_id,
                url=_url(_required(row, "url", row_number), row_number),
                title=_required(row, "title", row_number), brand=_required(row, "brand", row_number),
                country_code=country_code, asking_price_eur=_price(_required(row, "asking_price_eur", row_number), "asking_price_eur", row_number),
                condition=condition, authenticity=authenticity, observed_at=observed_at,
            ))
        return listings

    def _parse_evidence(self, contents: str) -> dict[str, list[PriceEvidence]]:
        evidence_by_listing: dict[str, list[PriceEvidence]] = {}
        for row_number, row in enumerate(csv.DictReader(StringIO(contents)), start=2):
            listing_external_id = _required(row, "listing_external_id", row_number)
            try:
                kind = EvidenceKind(_required(row, "kind", row_number))
                observed_at = datetime.fromisoformat(_required(row, "observed_at", row_number).replace("Z", "+00:00"))
                confidence = float(_required(row, "comparable_confidence", row_number))
            except ValueError as error:
                raise ImportValidationError(f"Row {row_number}: invalid evidence kind, timestamp, or confidence.") from error
            if not 0 <= confidence <= 1:
                raise ImportValidationError(f"Row {row_number}: comparable_confidence must be between 0 and 1.")
            evidence_by_listing.setdefault(listing_external_id, []).append(PriceEvidence(
                id=f"manual-evidence-{row_number}", source=self.name,
                source_reference=_required(row, "source_reference", row_number), kind=kind,
                price_eur=_price(_required(row, "price_eur", row_number), "price_eur", row_number),
                observed_at=observed_at, comparable_confidence=confidence,
            ))
        return evidence_by_listing
