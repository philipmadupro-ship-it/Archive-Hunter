from __future__ import annotations

from statistics import median

from .models import AuthenticityStatus, Condition, EvidenceKind, Listing, Opportunity, PriceEvidence

RESALE_FLOOR_EUR = 50.0
DEFAULT_CONDITIONS = frozenset({Condition.GOOD, Condition.VERY_GOOD, Condition.NEW_WITH_TAGS})


def _weighted_sold_reference(evidence: list[PriceEvidence]) -> float | None:
    sold = [item for item in evidence if item.kind is EvidenceKind.SOLD]
    if not sold:
        return None
    expanded_prices = [item.price_eur for item in sold for _ in range(max(1, round(item.comparable_confidence * 10)))]
    return round(median(expanded_prices), 2)


def _liquidity_score(sold_count: int) -> int:
    return min(100, sold_count * 25)


def _authenticity_note(status: AuthenticityStatus) -> str:
    return {
        AuthenticityStatus.AUTHENTICATED: "Authenticated evidence is recorded; verify scope and issuer.",
        AuthenticityStatus.SIGNALS_PRESENT: "Signals are present, but authentication remains unconfirmed.",
        AuthenticityStatus.UNVERIFIED: "No authentication conclusion is available; manual review required.",
        AuthenticityStatus.REJECTED: "Authenticity concern recorded; do not proceed without expert review.",
    }[status]


def score_listing(listing: Listing, evidence: list[PriceEvidence]) -> Opportunity:
    fair_value = _weighted_sold_reference(evidence)
    sold_count = sum(item.kind is EvidenceKind.SOLD for item in evidence)
    asking_count = sum(item.kind is EvidenceKind.ASKING for item in evidence)
    liquidity = _liquidity_score(sold_count)
    condition_points = {Condition.GOOD: 8, Condition.VERY_GOOD: 10, Condition.NEW_WITH_TAGS: 12}.get(listing.condition, 0)
    authenticity_points = {
        AuthenticityStatus.AUTHENTICATED: 10,
        AuthenticityStatus.SIGNALS_PRESENT: 4,
        AuthenticityStatus.UNVERIFIED: 0,
        AuthenticityStatus.REJECTED: -20,
    }[listing.authenticity]
    discount_points = 0 if fair_value is None else max(0, min(45, round((fair_value - listing.asking_price_eur) / fair_value * 100)))
    score = max(0, min(100, discount_points + round(liquidity * 0.35) + condition_points + authenticity_points))
    rationale = [f"{sold_count} sold comparables; asking comparables are excluded from resale valuation."]
    if fair_value is not None:
        rationale.append(f"Sold-only resale reference: €{fair_value:.2f}; current ask: €{listing.asking_price_eur:.2f}.")
    else:
        rationale.append("No sold comparables yet; price opportunity is not estimated.")
    rationale.append(_authenticity_note(listing.authenticity))
    return Opportunity(
        listing=listing,
        fair_value_eur=fair_value,
        sold_comparable_count=sold_count,
        asking_comparable_count=asking_count,
        liquidity_score=liquidity,
        opportunity_score=score,
        resale_floor_met=fair_value is not None and fair_value >= RESALE_FLOOR_EUR,
        authenticity_note=_authenticity_note(listing.authenticity),
        rationale=tuple(rationale),
    )
