from __future__ import annotations

from .models import AuthenticityStatus, Opportunity, ReviewItem, ReviewSeverity


def build_review_queue(opportunities: list[Opportunity]) -> list[ReviewItem]:
    queue: list[ReviewItem] = []
    for opportunity in opportunities:
        reasons: list[str] = []
        severity = ReviewSeverity.REQUIRED
        if opportunity.listing.authenticity is not AuthenticityStatus.AUTHENTICATED:
            reasons.append("Authenticity is not independently confirmed.")
        if opportunity.sold_comparable_count < 3:
            reasons.append("Fewer than three sold comparables support the resale reference.")
        if opportunity.fair_value_eur is None:
            reasons.append("No sold-only resale reference is available.")
            severity = ReviewSeverity.BLOCKING
        if not opportunity.resale_floor_met:
            reasons.append("Estimated resale is below €50 or cannot yet be estimated.")
        if reasons:
            queue.append(ReviewItem(opportunity.listing.id, severity, tuple(reasons)))
    return queue
