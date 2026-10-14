import gleam/int
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

pub fn the_page_says_who_he_is_in_the_readmes_words_test() {
  let html = page()
  assert content.me != ""
  assert string.contains(html, "the aquatic prometheus")
  assert string.contains(html, "the art of the maintenance of apps")
  assert string.contains(
    content.me,
    "wave modelling, game theory and self-improving apps",
  )
}

pub fn every_mark_of_the_timeline_is_on_the_page_test() {
  let html = page()
  assert content.timeline != []
  assert list.all(content.timeline, fn(e) { string.contains(html, e.when) })
  // Every mark names where its fact was read, and every era has a name.
  assert list.all(content.timeline, fn(e) { e.source != "" })
  assert list.all(content.timeline, fn(e) {
    list.any(app.eras, fn(era) { era.0 == e.era })
  })
  // One big mark, and a logo is never a file of this repository.
  assert list.count(content.timeline, fn(e) { e.mark == "big" }) == 1
  assert list.all(content.timeline, fn(e) {
    e.logo == "" || string.starts_with(e.logo, "https://")
  })
}

pub fn every_tie_joins_two_works_that_exist_test() {
  let ids = list.map(content.works, fn(w) { w.id })
  assert content.edges != []
  assert list.all(content.edges, fn(e) {
    list.contains(ids, e.from) && list.contains(ids, e.to) && e.source != ""
  })
}

pub fn every_work_is_a_node_and_a_line_of_the_list_test() {
  let html = page()
  assert list.all(content.works, fn(w) {
    string.contains(html, ">" <> w.name <> "<")
    && string.contains(html, app.standing(w))
  })
  // Each DOI of a work opens doi.org.
  assert list.all(content.works, fn(w) {
    w.doi == "" || string.contains(html, "https://doi.org/" <> w.doi)
  })
}

pub fn a_topic_lights_its_works_and_dims_the_rest_test() {
  let #(model, _) = app.update(app.initial(), app.Light("water"))
  let html = model |> app.view |> element.to_string
  assert string.contains(html, "node topic-ideas kind-own is-dim")
  assert string.contains(html, "class=\"node topic-water kind-own\"")
  // A second press lights every work again.
  let #(again, _) = app.update(model, app.Light("water"))
  assert again == app.initial()
}

pub fn the_notice_is_on_the_page_test() {
  let html = page()
  assert string.contains(html, "all rights are reserved")
  assert string.contains(html, "/blob/main/REUSE.md")
}

pub fn every_public_repository_is_indexed_test() {
  let html = page()
  assert list.length(content.repos) >= 40
  assert list.all(content.repos, fn(r) {
    string.contains(html, "href=\"" <> r.href <> "\"")
  })
  // Each one has one of the four colours of the page.
  assert list.all(content.repos, fn(r) {
    list.any(app.topics, fn(t) { t.0 == r.topic })
  })
  assert list.all(content.works, fn(w) {
    list.any(app.topics, fn(t) { t.0 == w.topic })
  })
}

pub fn the_arc_has_its_kanji_its_medal_and_its_prophecy_test() {
  let html = page()
  assert string.contains(html, ">名残</span>")
  assert string.contains(html, "Oceanman 10 km")
  assert list.any(content.timeline, fn(e) {
    e.mark == "prophecy" && e.when == "2027"
  })
}

pub fn the_numbers_come_from_the_metrics_cards_test() {
  let html = page()
  assert content.commits > 0
  assert content.contributed_to > 0
  assert content.languages != []
  assert string.contains(html, ">" <> int.to_string(content.commits) <> "<")
  assert list.all(content.languages, fn(l) { string.contains(html, l.0) })
  assert list.all(app.checks, fn(c: app.Check) {
    string.contains(html, "/actions/workflows/" <> c.file <> "\"")
  })
}

pub fn the_page_names_its_own_doi_test() {
  assert string.starts_with(content.doi, "10.5281/zenodo.")
  assert string.contains(page(), "https://doi.org/" <> content.doi)
}

pub fn the_three_areas_of_research_are_on_the_page_test() {
  let html = page()
  // The README names them, and the page gives each its light and its home.
  assert list.all(app.questions, fn(q: app.Question) {
    string.contains(content.me, q.name)
    && string.contains(html, "href=\"" <> q.href <> "\"")
  })
  assert string.contains(
    html,
    "<li class=\"topic-ouroboric\"><h3>self-improving apps</h3>",
  )
  assert string.contains(html, "https://github.com/ouroboric-dev\"")
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
  assert string.contains(html, "property=\"og:image:width\"")
  assert string.contains(html, "summary_large_image")
}

// The two friends' logos are found by name, and a name may have a flag after it on the arc.
pub fn the_logos_of_marola_and_ouroboric_stand_with_the_friends_test() {
  let html = page()
  assert string.contains(html, "alt=\"marola\"")
  assert string.contains(html, "alt=\"Ouroboric\"")
}

// One source, and a table for each other language: a sentence is looked up by its English.
pub fn a_sentence_is_translated_by_its_source_test() {
  assert app.translate("pt-BR", "the arc") == "a trajetória"
  assert app.translate("en", "the arc") == "the arc"
  // A sentence with no row is shown in English, and an unknown language is English.
  assert app.translate("pt-BR", "a sentence with no row")
    == "a sentence with no row"
  assert app.translate("xx", "the arc") == "the arc"
}

// The page is rendered in English at build time, and offers the two languages.
pub fn the_page_offers_its_languages_test() {
  let html = page()
  assert string.contains(html, ">português</button>")
  assert string.contains(html, "aria-pressed=\"true\"")
  assert string.contains(html, "the aquatic prometheus")
}

// The forks: every one on the page, and PUBLIC in capitals, the one exception to lower case.
pub fn every_fork_is_listed_as_public_test() {
  let html = page()
  assert content.forks != []
  assert string.contains(html, "forks, a PUBLIC inventory")
  assert list.all(content.forks, fn(f) { string.contains(html, f.href) })
}

// The topics of his stars are drawn, the most common first, with the date of their count.
pub fn the_stars_are_drawn_by_topic_test() {
  let html = page()
  assert content.stars > 0
  assert content.star_topics != []
  assert list.all(content.star_topics, fn(t) { string.contains(html, t.0) })
}

// A book has a star before its name, on the graph and in the list.
pub fn a_book_has_a_star_test() {
  let html = page()
  assert list.any(content.works, fn(w) { w.book })
  assert list.all(content.works, fn(w) {
    !w.book || string.contains(html, "★ " <> w.name)
  })
}
