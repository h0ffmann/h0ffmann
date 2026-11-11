import gleam/list
import gleam/string
import gleeunit
import h0ffmann_site/app
import h0ffmann_site/content
import h0ffmann_site/page
import lustre/element

pub fn main() -> Nil {
  gleeunit.main()
}

fn page() -> String {
  app.initial() |> app.view |> element.to_string
}

fn escaped(s: String) -> String {
  s |> string.replace("&", "&amp;") |> string.replace("'", "&#39;")
}

pub fn the_page_says_who_he_is_in_his_words_test() {
  let html = page()
  assert content.me != ""
  assert string.contains(html, escaped(content.me))
  assert string.starts_with(content.me, "staff software engineer")
  assert !string.contains(content.me, "jr. researcher")
  assert string.contains(
    content.me,
    "wave modelling, game theory and self-improving apps",
  )
  assert string.contains(html, "the art of the maintenance of apps")
  assert !string.contains(html, "aquatic prometheus")
}

pub fn the_readmes_studio_research_and_badges_are_on_the_page_test() {
  let html = page()
  assert content.studio != []
  assert list.all(content.studio, fn(i) {
    i.1 == "" || string.contains(html, "href=\"" <> i.1 <> "\"")
  })
  assert content.research != []
  assert content.badges != []
  assert list.all(content.badges, fn(b) {
    string.contains(html, "href=\"" <> b.1 <> "\"")
  })
  assert content.cvs != []
  assert list.all(content.cvs, fn(cv) {
    string.contains(html, "/blob/main/" <> cv.1 <> "\"")
  })
}

pub fn every_work_with_a_doi_is_linked_test() {
  let html = page()
  let dois = list.filter(content.works, fn(w) { w.doi != "" })
  assert list.length(dois) >= 6
  assert list.all(dois, fn(w) {
    string.contains(html, "https://doi.org/" <> w.doi)
  })
  assert list.all(dois, fn(w) {
    !w.book || string.contains(html, "★ " <> w.name)
  })
}

pub fn the_library_and_the_song_are_on_the_page_test() {
  let html = page()
  assert string.starts_with(content.reading.0, "media/")
  assert string.contains(html, "src=\"" <> content.reading.0 <> "\"")
  assert content.song != ""
  assert string.contains(
    html,
    "https://open.spotify.com/embed/track/" <> content.song,
  )
}

pub fn the_notice_and_its_doi_are_on_the_page_test() {
  let html = page()
  assert string.contains(html, "all rights are reserved")
  assert string.contains(html, "/blob/main/REUSE.md")
  assert string.starts_with(content.doi, "10.5281/zenodo.")
  assert string.contains(html, "https://doi.org/" <> content.doi)
}

pub fn a_link_to_the_site_has_a_preview_test() {
  let html =
    app.initial() |> app.view |> page.document |> element.to_document_string
  // LinkedIn needs a picture and an address, both as whole addresses.
  assert string.contains(
    html,
    "content=\"" <> page.address <> "og.png\" property=\"og:image\"",
  )
  assert string.contains(
    html,
    "content=\"" <> page.address <> "\" property=\"og:url\"",
  )
  assert string.contains(html, "summary_large_image")
}

// One source, and a table for each other language: a sentence is looked up by its English.
pub fn a_sentence_is_translated_by_its_source_test() {
  assert app.translate("pt-BR", "now") == "agora"
  assert app.translate("en", "now") == "now"
  assert app.translate("pt-BR", "a sentence with no row")
    == "a sentence with no row"
  assert app.translate("xx", "now") == "now"
}

pub fn the_page_offers_its_languages_test() {
  let html = page()
  assert string.contains(html, ">português</button>")
  assert string.contains(html, "aria-pressed=\"true\"")
  let #(model, _) = app.update(app.initial(), app.Speak("pt-BR"))
  assert model.lang == "pt-BR"
  // The language is one value for the page: put English back for the other tests.
  let #(back, _) = app.update(model, app.Speak("en"))
  assert back.lang == "en"
}
