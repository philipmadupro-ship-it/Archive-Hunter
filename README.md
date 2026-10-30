# ARCHIVE HUNTER

Europe-wide sourcing intelligence for luxury, archive, and vintage resale.

The first vertical slice accepts normalized listings from a compliant adapter, keeps **sold** and **asking** price evidence separate, estimates a resale reference from sold evidence, and returns liquidity, condition, authenticity-uncertainty, and opportunity signals. It never auto-rejects an item for ROI or estimated profit.

## Product rules encoded today

- European market, with prices normalized to EUR.
- Estimated resale reference of at least **€50** is a visible eligibility signal, not a hard automated purchase rule.
- Default condition focus: \`good\`, \`very_good\`, and \`new_with_tags\`.
- Sold evidence is the only input to the resale estimate; asking evidence is display-only context.
- Authenticity uncertainty reduces confidence and is always surfaced to the buyer.
- Scoring ranks opportunities; it does not replace physical-condition, provenance, or authentication review.

## Run the vertical slice

\`\`\`bash
python -m venv .venv
. .venv/bin/activate
pip install '.[dev]'
pytest
uvicorn archive_hunter.api:app --reload
\`\`\`

Open \`http://127.0.0.1:8000/docs\` for the API and \`http://127.0.0.1:8000/\` for the lightweight operator dashboard. \`GET /opportunities\` returns the scored fixture opportunity.

## Architecture

\`\`\`text
Approved API / partner feed / user export / manual review
                         |
                  SourceAdapter
                         |
      normalized Listing + immutable PriceEvidence
                         |
  opportunity engine (sold-only pricing + liquidity + risk)
                         |
      API / dashboard / Telegram delivery interface
\`\`\`

See [docs/source-adapters.md](docs/source-adapters.md) for the compliance boundary, [docs/roadmap.md](docs/roadmap.md) for the next integrations, and \`db/schema.sql\` for the PostgreSQL-ready data model.

## Credentials and source access

No marketplace credentials, browser automation, scraping, or protection-bypass logic is included. To connect a live source, obtain its written permission or official API/partner/feed access, then implement an adapter that returns the internal normalized contract.
