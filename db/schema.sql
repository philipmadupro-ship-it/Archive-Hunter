-- PostgreSQL foundation. Market observations are append-only for auditability.
CREATE TYPE listing_condition AS ENUM ('good', 'very_good', 'new_with_tags', 'other');
CREATE TYPE price_evidence_kind AS ENUM ('sold', 'asking');
CREATE TYPE authenticity_status AS ENUM ('unverified', 'signals_present', 'authenticated', 'rejected');

CREATE TABLE source_adapters (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  access_method TEXT NOT NULL,
  terms_reviewed_at TIMESTAMPTZ,
  enabled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE listings (
  id UUID PRIMARY KEY,
  source_adapter_id UUID NOT NULL REFERENCES source_adapters(id),
  external_id TEXT NOT NULL,
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  brand TEXT,
  country_code CHAR(2) NOT NULL,
  asking_price_cents INTEGER NOT NULL CHECK (asking_price_cents >= 0),
  currency CHAR(3) NOT NULL DEFAULT 'EUR',
  condition listing_condition NOT NULL,
  authenticity authenticity_status NOT NULL DEFAULT 'unverified',
  observed_at TIMESTAMPTZ NOT NULL,
  UNIQUE (source_adapter_id, external_id)
);

CREATE TABLE price_evidence (
  id UUID PRIMARY KEY,
  listing_id UUID REFERENCES listings(id),
  source_adapter_id UUID NOT NULL REFERENCES source_adapters(id),
  source_reference TEXT NOT NULL,
  kind price_evidence_kind NOT NULL,
  price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
  currency CHAR(3) NOT NULL DEFAULT 'EUR',
  observed_at TIMESTAMPTZ NOT NULL,
  comparable_confidence NUMERIC(4,3) NOT NULL CHECK (comparable_confidence BETWEEN 0 AND 1),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX price_evidence_sold_lookup ON price_evidence (kind, observed_at DESC);
