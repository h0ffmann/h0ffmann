//// The HTML document around the application.

import lustre/attribute
import lustre/element.{type Element}
import lustre/element/html

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
      property("og:title", title),
      property("og:description", description),
      property("og:type", "profile"),
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
        "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap",
      ),
      stylesheet("style.css"),
      // A module script is deferred, so <body> is parsed before the app mounts on it.
      html.script([attribute.type_("module"), attribute.src("app.js")], ""),
    ]),
    html.body([], [body]),
  ])
}
