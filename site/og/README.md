# The link preview

`site/static/og.png` is the picture that a link to the site shows in a chat or a feed (LinkedIn,
WhatsApp, Slack). `card.html` is its source. It follows [`DESIGN.md`](../../DESIGN.md).

The page names it with whole addresses (`site/src/h0ffmann_site/page.gleam`): `og:image`,
`og:url`, the picture's size, and a card for X. Without `og:image` and `og:url`, LinkedIn says
"We couldn't load a preview for this link".

## The limits it keeps

| Limit | This file |
|---|---|
| 1200 by 627, the size LinkedIn asks for a link | 1200 by 627 |
| PNG or JPG | PNG |
| a whole `https` address | `https://h0ffmann.github.io/h0ffmann/og.png` |

Every word is in the left two thirds, so a crop to a square loses only the drawing.

## After a change

A site keeps the old preview of a link for some days. To make LinkedIn read the page again, give
the address to its Post Inspector: `https://www.linkedin.com/post-inspector/` (it needs a
login, so it is written here as code).

## Make it again

```sh
python3 -m http.server 8782 &
google-chrome --headless=new --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,800 --virtual-time-budget=9000 --screenshot=raw.png \
  http://localhost:8782/site/og/card.html
```

Then cut `raw.png` to its top 1200 by 627 and save it as `site/static/og.png`. The window is
taller than the picture because Chrome's new headless mode gives a page less height than the
window has.
