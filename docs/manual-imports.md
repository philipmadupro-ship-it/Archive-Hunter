# Manual CSV imports

Use this adapter only for data you are entitled to export, receive, or record. Retain the original export and source terms outside the application. Do not paste data collected through prohibited scraping or account automation.

\`listings.csv\` columns:

\`\`\`text
external_id,url,title,brand,country_code,asking_price_eur,condition,authenticity,observed_at
\`\`\`

\`evidence.csv\` columns:

\`\`\`text
listing_external_id,source_reference,kind,price_eur,observed_at,comparable_confidence
\`\`\`

\`kind\` must be exactly \`sold\` or \`asking\`. Asking prices are never used as sold evidence. \`country_code\` must be a European ISO 3166-1 alpha-2 code, \`observed_at\` must be ISO 8601, and \`comparable_confidence\` must be between \`0\` and \`1\`.

Every imported opportunity still enters the review queue when authenticity is not independently confirmed, there are fewer than three sold comparables, or there is no sold-only reference. The system does not send a buy instruction.
