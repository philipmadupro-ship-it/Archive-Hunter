from archive_hunter.adapters import FixtureAdapter
from archive_hunter.models import EvidenceKind
from archive_hunter.scoring import score_listing
from archive_hunter.service import discover_opportunities


def test_fixture_vertical_slice_uses_only_sold_comparables_for_value() -> None:
    adapter = FixtureAdapter()
    listing = adapter.fetch_listings()[0]
    opportunity = score_listing(listing, adapter.fetch_price_evidence(listing))

    assert opportunity.fair_value_eur == 365.0
    assert opportunity.sold_comparable_count == 3
    assert opportunity.asking_comparable_count == 1
    assert opportunity.resale_floor_met is True
    assert opportunity.opportunity_score > 0


def test_asking_evidence_does_not_create_a_resale_reference() -> None:
    adapter = FixtureAdapter()
    listing = adapter.fetch_listings()[0]
    asking_only = [item for item in adapter.fetch_price_evidence(listing) if item.kind is EvidenceKind.ASKING]

    opportunity = score_listing(listing, asking_only)

    assert opportunity.fair_value_eur is None
    assert opportunity.resale_floor_met is False


def test_default_condition_filter_is_not_a_profit_or_roi_filter() -> None:
    opportunities = discover_opportunities(FixtureAdapter())
    assert len(opportunities) == 1
