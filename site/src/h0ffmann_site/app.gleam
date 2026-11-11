//// The page of Matheus Hoffmann: one short page, in piabrota's colours (the owner, 11 November
//// 2026: "minimal like https://exitnode.dev/ but with piabrota colors"; DESIGN.md). Every fact
//// comes from `content.gleam`, which site/content writes from README.md and site/data/.

import gleam/list
import gleam/string
import h0ffmann_site/content.{type Work}
import lustre/attribute.{type Attribute}
import lustre/effect.{type Effect}
import lustre/element.{type Element}
import lustre/element/html
import lustre/event

/// The language of the page, kept outside the model as well, so that every sentence can ask for
/// it where it is drawn (lang_ffi.mjs). "en" when the page is rendered at build time.
@external(javascript, "./lang_ffi.mjs", "get")
fn language() -> String

@external(javascript, "./lang_ffi.mjs", "set")
fn speak(lang: String) -> String

/// A sentence in the reader's language. The key is the English sentence itself: there is one
/// source, and a table for each other language (TRANSLATIONS.md). A sentence with no row in the
/// table is shown in English.
pub fn t(source: String) -> String {
  translate(language(), source)
}

pub fn translate(lang: String, source: String) -> String {
  case lang {
    "pt-BR" ->
      case list.key_find(content.pt_br, source) {
        Ok(target) -> target
        Error(_) -> source
      }
    _ -> source
  }
}

fn tx(source: String) -> Element(msg) {
  html.text(t(source))
}

pub type Model {
  Model(lang: String)
}

pub type Msg {
  /// The reader chose a language.
  Speak(String)
}

pub fn initial() -> Model {
  Model(lang: language())
}

pub fn init(_: Nil) -> #(Model, Effect(Msg)) {
  #(initial(), effect.none())
}

pub fn update(_model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
  case msg {
    Speak(lang) -> #(Model(lang: speak(lang)), effect.none())
  }
}

fn external(href: String, label: String) -> Element(msg) {
  html.a([attribute.href(href), attribute.rel("noopener")], [tx(label)])
}

fn a(name: String, value: String) -> Attribute(msg) {
  attribute.attribute(name, value)
}

fn button(href: String, label: String, class: String) -> Element(msg) {
  html.a(
    [
      attribute.class("button " <> class),
      attribute.href(href),
      attribute.rel("noopener"),
    ],
    [tx(label)],
  )
}

pub fn view(model: Model) -> Element(Msg) {
  html.div([], [
    top(model),
    html.main([attribute.class("wrap")], [
      cards(),
      works_section(),
      reading_section(),
      song_section(),
      links_section(),
    ]),
    footer(),
  ])
}

/// The two languages of the page. Each button names its language in that language.
fn tongues(model: Model) -> Element(Msg) {
  let choice = fn(lang: String, name: String) {
    html.button(
      [
        attribute.class("tongue"),
        a("lang", lang),
        a("aria-pressed", case model.lang == lang {
          True -> "true"
          False -> "false"
        }),
        event.on_click(Speak(lang)),
      ],
      [html.text(name)],
    )
  }
  html.div([attribute.class("tongues"), a("aria-label", "language")], [
    choice("en", "english"),
    choice("pt-BR", "português"),
  ])
}

fn top(model: Model) -> Element(Msg) {
  html.header([attribute.class("top")], [
    html.div([attribute.class("wrap bar")], [
      html.a([attribute.class("brand"), attribute.href("#")], [
        html.text("h0ffmann"),
      ]),
      html.nav([attribute.class("nav")], [
        html.a([attribute.href("#now")], [tx("now")]),
        html.a([attribute.href("#works")], [tx("works")]),
        html.a([attribute.href("#reading")], [tx("reading")]),
        tongues(model),
      ]),
    ]),
    html.div([attribute.class("wrap hero")], [
      html.div([], [
        html.p([attribute.class("eyebrow")], [
          tx("matheus hoffmann / rio de janeiro"),
        ]),
        html.h1([], [tx("h0ffmann")]),
        html.p([attribute.class("motto")], [
          tx("the art of the maintenance of apps"),
        ]),
        html.p([attribute.class("lede")], [tx(content.me)]),
        html.p(
          [attribute.class("actions")],
          list.flatten([
            // The CVs the README links (its first line).
            list.map(content.cvs, fn(cv) {
              button(
                content.repo <> "/blob/main/" <> cv.1,
                "cv, " <> cv.0,
                "primary",
              )
            }),
            // Only the CVs the README links (the owner, 11 November 2026).
            [button(content.repo, "the readme on GitHub", "quiet")],
          ]),
        ),
      ]),
      html.span(
        [attribute.class("drawing prometheus"), a("aria-hidden", "true")],
        [],
      ),
    ]),
  ])
}

/// What he does now, in the README's words: two cards, the studio and the research.
fn cards() -> Element(msg) {
  html.section([attribute.class("cards"), attribute.id("now")], [
    html.p([attribute.class("label")], [tx("now")]),
    html.div([attribute.class("grid")], [
      html.article([attribute.class("card")], [
        html.h2([], [tx(content.studio_title)]),
        html.ul(
          [attribute.class("sites")],
          list.map(content.studio, fn(item) {
            let #(name, href, text) = item
            case href {
              "" -> html.li([], [html.span([], [tx(text)])])
              _ ->
                html.li([], [external(href, name), html.span([], [tx(text)])])
            }
          }),
        ),
      ]),
      html.article([attribute.class("card")], [
        html.h2([], [tx(content.research_title)]),
        // The README's line of DOIs is the list of works below, with each DOI as a link.
        ..list.filter(content.research, fn(r) {
          !string.starts_with(r, "My works with a DOI")
        })
        |> list.map(fn(r) { html.p([], [tx(r)]) })
      ]),
    ]),
  ])
}

/// A book has a star before its name (site/data/works.tsv, `form`).
pub fn starred(w: Work) -> String {
  case w.book {
    True -> "★ " <> w.name
    False -> w.name
  }
}

/// The works with a DOI, each with its DOI as a link (AGENTS.md, hard rule 2).
fn works_section() -> Element(msg) {
  let works = list.filter(content.works, fn(w: Work) { w.doi != "" })
  html.section([attribute.class("cards"), attribute.id("works")], [
    html.p([attribute.class("label")], [tx("works with a DOI")]),
    html.ul(
      [attribute.class("works")],
      list.map(works, fn(w: Work) {
        html.li([], [
          case w.href {
            "" -> html.strong([], [tx(starred(w))])
            href -> external(href, starred(w))
          },
          html.span([], [tx(w.text)]),
          external("https://doi.org/" <> w.doi, w.doi),
        ])
      }),
    ),
  ])
}

/// How he reads: the README's picture of his library (media/, copied into the site by `just site`).
fn reading_section() -> Element(msg) {
  let #(src, alt) = content.reading
  case src {
    "" -> element.none()
    _ ->
      html.section([attribute.class("cards"), attribute.id("reading")], [
        html.p([attribute.class("label")], [tx("how i read")]),
        html.img([
          attribute.class("shelf"),
          attribute.src(src),
          attribute.alt(alt),
          a("loading", "lazy"),
        ]),
      ])
  }
}

/// The song (site/data/music.tsv), in Spotify's own player. Browsers do not start sound on their
/// own, so it plays when the reader presses play.
fn song_section() -> Element(msg) {
  case content.song {
    "" -> element.none()
    track ->
      html.section([attribute.class("cards"), attribute.id("song")], [
        html.p([attribute.class("label")], [tx("a song")]),
        html.iframe([
          attribute.class("song"),
          attribute.src(
            "https://open.spotify.com/embed/track/" <> track <> "?theme=0",
          ),
          a("title", "Spotify"),
          a("height", "152"),
          a("loading", "lazy"),
          a(
            "allow",
            "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
          ),
        ]),
      ])
  }
}

/// The README's badges, as plain links.
fn links_section() -> Element(msg) {
  html.section([attribute.class("cards")], [
    html.p([attribute.class("label")], [tx("elsewhere")]),
    html.p(
      [attribute.class("links")],
      list.map(content.badges, fn(b) { external(b.1, b.0) }),
    ),
  ])
}

fn footer() -> Element(msg) {
  html.footer([attribute.class("foot")], [
    html.div([attribute.class("wrap")], [
      html.p([], [
        tx(
          "this page is one person's story. all rights are reserved: cite it with a link, do not copy it (",
        ),
        external(content.repo <> "/blob/main/REUSE.md", "REUSE.md"),
        tx(")."),
        case content.doi {
          "" -> element.none()
          doi ->
            html.span([], [
              tx(" cite this page as doi "),
              external("https://doi.org/" <> doi, doi),
              tx("."),
            ])
        },
      ]),
      html.p([], [
        tx("© matheus hoffmann. built from "),
        external(
          content.repo <> "/commit/" <> content.revision,
          "commit " <> content.revision,
        ),
        tx(", with Gleam and Lustre and tools pinned by Nix from "),
        external("https://github.com/h0ffmann/picasso", "picasso"),
        tx(". the colours are piabrota's."),
      ]),
    ]),
  ])
}
