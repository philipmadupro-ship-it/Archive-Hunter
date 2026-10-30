# Delivery roadmap

## Next after this slice

1. Provision PostgreSQL and apply \`db/schema.sql\`; add repository implementations and migration tooling.
2. Add a reviewed brand/reference catalogue and a manual comparable-review queue.
3. Connect approved European sources one at a time through \`SourceAdapter\`; retain source terms and evidence metadata.
4. Add an FX provider with timestamped EUR conversions and duplicate detection.
5. Add authentication, saved searches, and a proper dashboard UI.
6. Implement Telegram transport after the bot token, target chat ID, and delivery rules are supplied; alerts should link to the source and show risk labels.

## Explicitly blocked pending access

- No live marketplace inventory or sold-history feed is connected.
- No authenticated price database, image-authentication service, FX API, PostgreSQL instance, or Telegram bot credentials are configured.
- Authenticity remains an uncertainty flag until reviewed evidence or a qualified authenticator is connected.
