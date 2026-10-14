//// profile_content: write `site/src/h0ffmann_site/content.gleam` from the files of this
//// repository, so the site never repeats a fact by hand. It reads README.md (the sentence about
//// the owner, the certificates), me/ways-of-working.md (its headings) and the tables of
//// site/data/ (the timeline, the works, their ties, every repository, the README's history, the
//// friends).
////
////     gleam run     # from site/content; `just site` does it
////
//// It is its own package, because the site cannot compile before its content exists.
//// The shape is that of marola-dev/marola-research's tools/content, by the same author.

import gleam/float
import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string

@external(javascript, "./profile_content_ffi.mjs", "read")
fn read(path: String) -> String

@external(javascript, "./profile_content_ffi.mjs", "write")
fn write(path: String, text: String) -> Nil

@external(javascript, "./profile_content_ffi.mjs", "revision")
fn revision() -> String

@external(javascript, "./profile_content_ffi.mjs", "readme_commits")
fn readme_commits() -> String

/// The words of an SVG card (the metrics cards), tags out.
@external(javascript, "./profile_content_ffi.mjs", "card_text")
fn card_text(path: String) -> String

/// The whole number just before `word` in a card's text: "4140 Commits" gives 4140. 0 when the
/// word is not there.
pub fn number_before(text: String, word: String) -> Int {
  let words = string.split(text, " ")
  list.window_by_2(words)
  |> list.find_map(fn(pair) {
    case pair.1 == word {
      True -> int.parse(pair.0)
      False -> Error(Nil)
    }
  })
  |> result.unwrap(0)
}

/// The languages of the languages card, the largest share first: #(name, share). The card writes, after
/// the word "commits", a name, a size, a unit and a share for each language.
pub fn languages(text: String) -> List(#(String, String)) {
  let after = case string.split_once(text, " commits ") {
    Ok(#(_, rest)) -> rest
    Error(_) -> ""
  }
  string.split(after, " ")
  |> list.fold(#([], []), fn(acc, word) {
    let #(done, current) = acc
    case string.ends_with(word, "%") {
      // current is the share's line in reverse: unit, size, then the name's words.
      True ->
        case current {
          [_unit, _size, ..name] if name != [] -> #(
            [#(string.join(list.reverse(name), " "), word), ..done],
            [],
          )
          _ -> #(done, [])
        }
      False -> #(done, [word, ..current])
    }
  })
  |> fn(acc) { list.reverse(acc.0) }
  // The largest share first.
  |> list.sort(fn(a, b) { float.compare(share(b.1), share(a.1)) })
}

fn share(percent: String) -> Float {
  let digits = string.drop_end(percent, 1)
  case float.parse(digits) {
    Ok(f) -> f
    Error(_) -> int.to_float(result.unwrap(int.parse(digits), 0))
  }
}

/// The rows of a table of site/data: tab-separated, a line that starts with "#" is a comment.
pub fn rows(tsv: String) -> List(List(String)) {
  string.split(tsv, "\n")
  |> list.filter(fn(l) { l != "" && !string.starts_with(l, "#") })
  |> list.map(string.split(_, "\t"))
}

/// Markdown marks out: bold, emphasis, code marks, and a link becomes its words.
pub fn plain(s: String) -> String {
  s
  |> string.replace("**", "")
  |> string.replace("`", "")
  |> unlink
  |> string.replace("*", "")
  |> string.trim
}

fn unlink(s: String) -> String {
  case string.split_once(s, "](") {
    Error(_) -> s
    Ok(#(before, after)) ->
      case string.split_once(after, ")") {
        Error(_) -> s
        Ok(#(_, rest)) ->
          case list.reverse(string.split(before, "[")) {
            [words, ..head] ->
              string.join(list.reverse(head), "[") <> words <> unlink(rest)
            [] -> s
          }
      }
  }
}

/// The first paragraph under a README heading that starts with `start` ("## 👋 me").
pub fn paragraph(readme: String, start: String) -> String {
  string.split(readme, "\n")
  |> list.drop_while(fn(l) { !string.starts_with(l, start) })
  |> list.drop(1)
  |> list.drop_while(fn(l) { string.trim(l) == "" })
  |> list.take_while(fn(l) {
    string.trim(l) != "" && !string.starts_with(l, "<")
  })
  |> string.join(" ")
  |> plain
}

/// The `### ` headings of a page, in order.
pub fn headings(page: String) -> List(String) {
  string.split(page, "\n")
  |> list.filter_map(fn(l) {
    case l {
      "### " <> title -> Ok(string.trim(title))
      _ -> Error(Nil)
    }
  })
}

/// A Gleam string literal.
pub fn lit(s: String) -> String {
  "\""
  <> s
  |> string.replace("\\", "\\\\")
  |> string.replace("\"", "\\\"")
  |> string.replace("\n", "\\n")
  <> "\""
}

fn lits(items: List(String)) -> String {
  "[\n" <> string.concat(list.map(items, fn(i) { "  " <> i <> ",\n" })) <> "]"
}

fn record(name: String, fields: List(#(String, String))) -> String {
  name
  <> "("
  <> string.join(list.map(fields, fn(f) { f.0 <> ": " <> f.1 }), ", ")
  <> ")"
}

fn number(s: String) -> String {
  int.to_string(result.unwrap(int.parse(s), 0))
}

pub fn main() -> Nil {
  // From site/content, the repository's root is two levels up.
  let readme = read("../../README.md")
  let events =
    rows(read("../data/timeline.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [when, era, mark, glyph, title, text, logo, href, source] ->
          Ok(
            record("Event", [
              #("when", lit(when)),
              #("era", lit(era)),
              #("mark", lit(mark)),
              #("glyph", lit(glyph)),
              #("title", lit(title)),
              #("text", lit(text)),
              #("logo", lit(logo)),
              #("href", lit(href)),
              #("source", lit(source)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let works =
    rows(read("../data/works.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [id, name, topic, kind, doi, href, licence, x, y, text] ->
          Ok(
            record("Work", [
              #("id", lit(id)),
              #("name", lit(name)),
              #("topic", lit(topic)),
              #("kind", lit(kind)),
              #("doi", lit(doi)),
              #("href", lit(href)),
              #("licence", lit(licence)),
              #("x", number(x)),
              #("y", number(y)),
              #("text", lit(text)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let edges =
    rows(read("../data/edges.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [from, to, relation, source] ->
          Ok(
            record("Edge", [
              #("from", lit(from)),
              #("to", lit(to)),
              #("relation", lit(relation)),
              #("source", lit(source)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let history =
    rows(read("../data/history.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [date, sha, headline, stack] ->
          Ok(
            record("Snapshot", [
              #("date", lit(date)),
              #("sha", lit(sha)),
              #("headline", lit(headline)),
              #("stack", lit(stack)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let repos =
    rows(read("../data/repos.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [owner, name, topic, year, description, href] ->
          Ok(
            record("Repo", [
              #("owner", lit(owner)),
              #("name", lit(name)),
              #("topic", lit(topic)),
              #("year", lit(year)),
              #("description", lit(description)),
              #("href", lit(href)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let base = card_text("../../metrics.base.svg")
  let langs =
    languages(card_text("../../metrics.languages.svg"))
    |> list.map(fn(l) { "#(" <> lit(l.0) <> ", " <> lit(l.1) <> ")" })
  // One table for each language: the source sentence, and the same sentence in that language
  // (site/data/translations/, TRANSLATIONS.md). The page looks a sentence up by its source.
  let pt_br =
    rows(read("../data/translations/pt-BR.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [source, target, ..] if target != "" ->
          Ok("#(" <> lit(source) <> ", " <> lit(target) <> ")")
        _ -> Error(Nil)
      }
    })
  let self = rows(read("../data/self.tsv"))
  let own = fn(key: String) {
    list.find_map(self, fn(r) {
      case r {
        [k, v] if k == key -> Ok(v)
        _ -> Error(Nil)
      }
    })
    |> result.unwrap("")
  }
  let friends =
    rows(read("../data/friends.tsv"))
    |> list.filter_map(fn(r) {
      case r {
        [name, what, href] ->
          Ok(
            record("Friend", [
              #("name", lit(name)),
              #("what", lit(what)),
              #("href", lit(href)),
            ]),
          )
        _ -> Error(Nil)
      }
    })
  let #(commits, first) = case string.split_once(readme_commits(), " ") {
    Ok(#(n, date)) -> #(number(n), date)
    Error(_) -> #("0", "")
  }
  let out = "../src/h0ffmann_site/content.gleam"
  let text =
    "//// Generated by site/content (`just site`) from README.md, me/ and site/data/; do not edit.

/// One mark on the timeline.
pub type Event {
  Event(
    when: String,
    era: String,
    mark: String,
    glyph: String,
    title: String,
    text: String,
    logo: String,
    href: String,
    source: String,
  )
}

/// One work of the knowledge graph, placed by hand on a 1000 by 620 canvas.
pub type Work {
  Work(
    id: String,
    name: String,
    topic: String,
    kind: String,
    doi: String,
    href: String,
    licence: String,
    x: Int,
    y: Int,
    text: String,
  )
}

/// One tie between two works, as an index or a file states it.
pub type Edge {
  Edge(from: String, to: String, relation: String, source: String)
}

/// How the README described its owner at one commit.
pub type Snapshot {
  Snapshot(date: String, sha: String, headline: String, stack: String)
}

pub type Friend {
  Friend(name: String, what: String, href: String)
}

/// One public repository, as GitHub listed it on the date of record of site/data/repos.tsv.
pub type Repo {
  Repo(
    owner: String,
    name: String,
    topic: String,
    year: String,
    description: String,
    href: String,
  )
}

pub const repo = \"https://github.com/h0ffmann/h0ffmann\"

pub const revision = "
    <> lit(revision())
    <> "

/// The page in Brazilian Portuguese: each source sentence with its translation
/// (site/data/translations/pt-BR.tsv). A sentence that is not here is shown in English.
pub const pt_br: List(#(String, String)) = "
    <> lits(pt_br)
    <> "

/// This repository's own DOI (site/data/self.tsv): the one that always opens its latest
/// release. Empty before the first release.
pub const doi = "
    <> lit(own("doi"))
    <> "

/// The numbers of metrics.base.svg, which the metrics workflow makes each day; 0 when the card
/// was not there.
pub const commits = "
    <> int.to_string(number_before(base, "Commits"))
    <> "

pub const contributed_to = "
    <> int.to_string(number_before(base, "repositories"))
    <> "

pub const pull_requests = "
    <> int.to_string(number_before(base, "Pull"))
    <> "

/// The languages of metrics.languages.svg, the largest share first: #(name, share).
pub const languages: List(#(String, String)) = "
    <> lits(langs)
    <> "

/// The README's own sentence about its owner (the section \"me\").
pub const me = "
    <> lit(paragraph(readme, "## 👋 me"))
    <> "

/// The README's line of certificates.
pub const certs = "
    <> lit(paragraph(readme, "## 🏅 certs"))
    <> "

/// The headings of me/ways-of-working.md.
pub const ways = "
    <> lits(list.map(headings(read("../../me/ways-of-working.md")), lit))
    <> "

/// How many commits changed README.md; 0 when the build had no Git history.
pub const readme_commits = "
    <> commits
    <> "

/// The date of the first commit of README.md; empty when the build had no Git history.
pub const readme_first = "
    <> lit(first)
    <> "

pub const timeline = "
    <> lits(events)
    <> "

pub const works = "
    <> lits(works)
    <> "

pub const edges = "
    <> lits(edges)
    <> "

pub const history = "
    <> lits(history)
    <> "

pub const friends = "
    <> lits(friends)
    <> "

/// Every public source repository, newest first.
pub const repos = "
    <> lits(repos)
    <> "
"
  write(out, text)
  io.println("profile_content: wrote site/src/h0ffmann_site/content.gleam")
}
