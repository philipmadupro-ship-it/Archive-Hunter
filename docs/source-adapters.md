# Source adapter policy

Every live adapter must use one of these inputs: an official API, a written partner/affiliate feed, a user-authorized data export, or a manual-review import. Before enabling an adapter, record its permitted access method, terms review date, regional scope, rate limits, and required attribution.

Adapters must not scrape pages where permission is absent, impersonate users, automate login, bypass rate limits, solve CAPTCHAs, evade bot detection, or reuse marketplace data outside its allowed purpose. A source that cannot establish a compliant access path remains disabled.

The adapter boundary intentionally exposes only \`fetch_listings()\` and \`fetch_price_evidence()\`. Price evidence must state \`sold\` or \`asking\`; listings cannot be labelled sold merely because a price is present.
