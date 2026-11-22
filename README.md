# La Porta Homes — direct-booking website

Round 1 of the La Porta Homes site: one static page (`index.html`) with the 13 homes that are listed on Airbnb, their photos, and a request form.

## What is in this repo

| Path | What it is |
| --- | --- |
| `index.html` | The whole site: home, stays with filters, a page per home (`#u-<id>`), owners section. No build step. |
| `img/` | 78 photos, 6 per home, compressed to 1200 px. File name = last 6 digits of the Airbnb listing id + photo number. |
| `data/units.json` | Listing ids, titles, guests and photo files as pulled on 22 Nov 2026. |
| `tools/scrape.py` | Pulls the public listing pages and photos again (run on the Mac). |
| `tools/test_site.py` | Opens the page in WebKit at phone and desktop width, checks overflow, broken images, filter, unit page, request form. |

## Run it locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Still open before launch

- Real logo files (the header uses a text wordmark and a drawn arch for now).
- Domain, WhatsApp number, legal company name.
- Direct-booking prices, cancellation policy and payment method.
- Compound of the 3-bedroom villa (877272); the beachfront 1-bedroom (516096) is in Hurghada.

## Rules

- Do not link from Airbnb listings or Airbnb messages to this site (Airbnb Off-Platform policy).
- Photos and text are La Porta Homes' own; do not add third-party photos.
