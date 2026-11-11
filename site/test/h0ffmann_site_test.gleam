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

pub fn think_is_piabrota_test() {
  let html = page()
  assert content.studio != []
  assert list.all(content.studio, fn(i) {
    i.1 == "" || string.contains(html, "href=\"" <> i.1 <> "\"")
  })
  assert string.contains(html, "href=\"https://github.com/piabrota\"")
  assert content.cvs != []
  assert list.all(content.cvs, fn(cv) {
    string.contains(html, "/blob/main/" <> cv.1 <> "\"")
  })
  assert !string.contains(html, "cv-water")
}

// The owner, 11 November 2026: write is the two aiXiv papers and the DOIs of marola and closed
// source, and no other DOI.
pub fn write_is_two_papers_and_two_dois_test() {
  let html = page()
  let papers =
    list.filter(content.badges, fn(b) { string.starts_with(b.0, "aiXiv") })
  assert list.length(papers) == 2
  assert list.all(papers, fn(b) {
    string.contains(html, "href=\"" <> b.1 <> "\"")
  })
  list.each(content.works, fn(w) {
    case w.doi {
      "" -> Nil
      doi -> {
        let shown = string.contains(html, "https://doi.org/" <> doi)
        assert shown == list.contains(app.written, w.id)
      }
    }
  })
  assert list.length(app.written) == 2
}

pub fn read_is_goodreads_and_the_song_plays_test() {
  let html = page()
  assert string.contains(html, "goodreads.com/user/show/")
  assert !string.contains(html, "substack")
  assert content.song != ""
  assert string.contains(
    html,
    "https://open.spotify.com/embed/" <> content.song,
  )
  assert string.starts_with(content.song, "album/")
  assert string.contains(html, "id=\"hear\"")
  assert string.starts_with(content.lyrics, "https://genius.com/")
  assert !string.contains(html, ">a song<")
}

pub fn have_fun_is_the_diver_and_the_swims_test() {
  let html = page()
  assert content.fun
    == [#("PADI diver", "5 courses"), #("water marathons", "2")]
  assert string.contains(html, "id=\"fun\"")
  assert string.contains(html, ">5 courses<")
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
  assert app.translate("pt-BR", "think") == "penso"
  assert app.translate("en", "think") == "think"
  assert app.translate("pt-BR", "a sentence with no row")
    == "a sentence with no row"
  assert app.translate("xx", "think") == "think"
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
