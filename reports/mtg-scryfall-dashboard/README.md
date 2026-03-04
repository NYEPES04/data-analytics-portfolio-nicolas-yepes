# MTG Market Intelligence Dashboard (Scryfall API + Power BI)

This project is a personal market intelligence dashboard for *Magic: The Gathering*, built to analyze:
- Price dynamics and USD concentration by set/expansion
- Rarity-driven value distribution
- Deck portfolio composition and value exposure
- Card mix analysis (CMC distribution, categories, colors)

It demonstrates end-to-end analytics: API ingestion → data modeling → dashboards for executive-style insights.

## What you can see in the dashboard

### 1) Expansion USD concentration (Treemap)
Shows how total USD value concentrates across expansions/sets and highlights top value drivers.
![Expansion USD concentration](./screenshots/01_expansion_usd_treemap.png)

### 2) Deck value concentration (Treemap + bar)
Compares deck value distribution and how value concentrates by deck and rarity.
![Deck value concentration](./screenshots/02_deck_value_treemap.png)

### 3) Deck composition (Categories + CMC distribution)
Breaks down deck composition by functional category (ramp, removal, draw, etc.) and CMC distribution by color.
![Deck composition](./screenshots/03_deck_categories_cmc.png)

## Data source
- Scryfall API (cards endpoint): used to retrieve card identifiers, set metadata, pricing fields (usd / usd_foil), and image URLs.
- Deck lists (Archidekt export): used to connect personal deck composition with Scryfall IDs (via `scryfall_id` / `oracle_id`).

## Power Query (M) ingestion
The Power Query script used to paginate the Scryfall API and build the cards table is included here:
- `./powerbi/scryfall_query.m`

Highlights:
- Pagination via `next_page`
- Filters out digital-only cards
- Extracts `usd` and `usd_foil`
- Builds a robust `image_normal` field
- Removes heavy nested image fields to reduce model size

## Key outputs (analytics focus)
- Concentration insights (which expansions drive most of the value)
- Rarity impact (how mythics/rares shape total USD)
- Portfolio thinking applied to decks (value exposure by deck and by category)
- Repeatable ingestion pattern suitable for scheduled refresh (with caution on API limits)

## Notes
This is a personal analytics project built for learning and portfolio demonstration. Card prices can vary over time and reflect Scryfall’s latest available pricing fields.
