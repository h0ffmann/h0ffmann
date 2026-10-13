//// The HTML document around the application.

import lustre/attribute
import lustre/element.{type Element}
import lustre/element/html

/// Where the site is published. A link preview needs whole addresses, not relative ones.
pub const address = "https://h0ffmann.github.io/h0ffmann/"

pub fn document(body: Element(msg)) -> Element(msg) {
  let meta = fn(name, value) {
    html.meta([attribute.name(name), attribute.content(value)])
  }
  let property = fn(name, value) {
    html.meta([attribute.attribute("property", name), attribute.content(value)])
  }
  let stylesheet = fn(href) {
    html.link([attribute.rel("stylesheet"), attribute.href(href)])
  }
  let title = "h0ffmann: matheus hoffmann, the aquatic prometheus"
  let description =
    "the art of the maintenance of apps. open research on wave modelling, game theory and self-improving apps, from an ex kid athlete."
  html.html([attribute.lang("en")], [
    html.head([], [
      html.meta([attribute.charset("utf-8")]),
      meta("viewport", "width=device-width, initial-scale=1"),
      html.title([], title),
      meta("description", description),
      meta("author", "Matheus Hoffmann"),
      // The page is the owner's story: all rights reserved (LICENSE, REUSE.md).
      meta(
        "rights",
        "© Matheus Hoffmann. All rights reserved. Cite it; do not copy it.",
      ),
      // The link preview (LinkedIn, WhatsApp, Slack): without og:image and og:url, LinkedIn says
      // "we couldn't load a preview for this link". The picture is site/static/og.png, 1200 by
      // 627, made from site/og/card.html.
      html.link([attribute.rel("canonical"), attribute.href(address)]),
      property("og:title", title),
      property("og:description", description),
      property("og:type", "website"),
      property("og:url", address),
      property("og:site_name", "h0ffmann"),
      property("og:image", address <> "og.png"),
      property("og:image:secure_url", address <> "og.png"),
      property("og:image:type", "image/png"),
      property("og:image:width", "1200"),
      property("og:image:height", "627"),
      property(
        "og:image:alt",
        "h0ffmann, the aquatic prometheus: the art of the maintenance of apps. wave modelling, game theory, self-improving apps.",
      ),
      meta("twitter:card", "summary_large_image"),
      meta("twitter:title", title),
      meta("twitter:description", description),
      meta("twitter:image", address <> "og.png"),
      html.link([
        attribute.rel("icon"),
        attribute.href("icons/favicon.svg"),
        attribute.type_("image/svg+xml"),
      ]),
      html.link([
        attribute.rel("preconnect"),
        attribute.href("https://fonts.googleapis.com"),
      ]),
      html.link([
        attribute.rel("preconnect"),
        attribute.href("https://fonts.gstatic.com"),
        attribute.crossorigin(""),
      ]),
      stylesheet(
        "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+JP:wght@600&display=swap",
      ),
      stylesheet("style.css"),
      // A module script is deferred, so <body> is parsed before the app mounts on it.
      html.script([attribute.type_("module"), attribute.src("app.js")], ""),
    ]),
    html.body([], [body]),
  ])
}
