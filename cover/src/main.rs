//! The LinkedIn cover: the public repositories that h0ffmann pins on GitHub, as an Archify architecture diagram.
//!
//!     cover json <login> <out.json>     read the pinned repositories with `gh`, write Archify's input
//!     cover frame <in.html> <out.html>  keep only the drawing, sized for a 1584x396 capture
use serde_json::{json, Value};
use std::process::{exit, Command};
use std::{env, fs};

const QUERY: &str = "query($login: String!, $year: DateTime!, $month: DateTime!) { user(login: $login) { login name createdAt
  thisYear: contributionsCollection(from: $year) { contributionCalendar { totalContributions } }
  lastMonth: contributionsCollection(from: $month) { commitContributionsByRepository(maxRepositories: 100) {
    repository { isPrivate primaryLanguage { name } } contributions { totalCount } } }
  pinnedItems(first: 6, types: REPOSITORY) { nodes { ... on Repository {
    nameWithOwner isPrivate primaryLanguage { name }
    repositoryTopics(first: 10) { nodes { topic { name } } } } } } } }";

// The canvas, in Archify's units: small, so that Archify's own type comes out about 2.6 times
// larger when Chrome stretches it to 1584x396, and LinkedIn's profile page (about 800 px wide)
// still shows the names at some 19 px. The pins take a grid of 3x2 on the right; the user's box
// sits top left, above where LinkedIn puts the profile photo.
const COLS: i64 = 3;
const CELL_W: i64 = 128;
const CELL_H: i64 = 60;
const GAP: i64 = 10;
const USER_W: i64 = 186;
const GRID_X: i64 = USER_W + 2 * GAP;
const LANGUAGES: usize = 3;
// The skills share the sublabel line of a box: 9px type, 5.4 units a character (Archify's
// authoring defaults), less the box's padding.
const SKILL_CHARS: usize = 20;

/// Every public pin, as GitHub lists it, with a licence or without.
fn public(repo: &Value) -> bool {
    !repo["isPrivate"].as_bool().unwrap_or(true)
}

/// The skills of a pin: its language, then its GitHub topics in GitHub's order, as many as fit in
/// SKILL_CHARS characters.
fn skills(repo: &Value) -> Vec<String> {
    let topics = repo["repositoryTopics"]["nodes"].as_array().into_iter().flatten();
    repo["primaryLanguage"]["name"].as_str().into_iter().map(str::to_lowercase)
        .chain(topics.filter_map(|t| t["topic"]["name"].as_str().map(String::from)))
        .fold(vec![], |mut kept: Vec<String>, s| {
            if kept.iter().map(|k| k.chars().count() + 3).sum::<usize>() + s.chars().count() <= SKILL_CHARS {
                kept.push(s);
            }
            kept
        })
}

/// The languages of the last 30 days: the main language of each public repository committed to,
/// weighed by its commits, the most first.
fn languages(user: &Value) -> Vec<String> {
    let mut count: Vec<(String, i64)> = vec![];
    for c in user["lastMonth"]["commitContributionsByRepository"].as_array().into_iter().flatten() {
        let Some(lang) = c["repository"]["primaryLanguage"]["name"].as_str() else { continue };
        if c["repository"]["isPrivate"].as_bool().unwrap_or(true) {
            continue;
        }
        let n = c["contributions"]["totalCount"].as_i64().unwrap_or(0);
        match count.iter_mut().find(|(l, _)| l == lang) {
            Some((_, total)) => *total += n,
            None => count.push((lang.to_string(), n)),
        }
    }
    count.sort_by(|a, b| b.1.cmp(&a.1));
    count.into_iter().take(LANGUAGES).map(|(l, _)| l.to_lowercase()).collect()
}

/// Whole years from `since` to `today`, both "YYYY-MM-DD...".
fn years(since: &str, today: &str) -> i64 {
    let year = |d: &str| d.get(..4).and_then(|y| y.parse::<i64>().ok()).unwrap_or(0);
    year(today) - year(since) - i64::from(today.get(5..10) < since.get(5..10))
}

/// The user's box top left, the pins in a grid of three columns to its right, in GitHub's order.
/// No lines: on a cover every box is read on its own, and six lines from one box are noise.
fn diagram(user: &Value, today: &str, claude: i64) -> Value {
    let login = user["login"].as_str().unwrap_or("");
    let repos: Vec<&Value> = user["pinnedItems"]["nodes"].as_array().into_iter().flatten().filter(|r| public(r)).collect();
    let mut components = vec![json!({
        "id": "user", "type": "external",
        "label": format!("{login} · {} years", years(user["createdAt"].as_str().unwrap_or(today), today)),
        "sublabel": format!("{} contribs · {claude} w/ claude",
            user["thisYear"]["contributionCalendar"]["totalContributions"].as_i64().unwrap_or(0)),
        "tag": format!("{} · 30d: {}", &today[..4], languages(user).join(" · ")),
        "pos": [GAP, GAP], "size": [USER_W, CELL_H],
    })];
    for (i, r) in repos.iter().enumerate() {
        let (col, row) = (i as i64 % COLS, i as i64 / COLS);
        let name = r["nameWithOwner"].as_str().unwrap_or("");
        components.push(json!({
            "id": format!("repo-{i}"), "type": "backend",
            "label": name.rsplit('/').next(),
            "sublabel": skills(r).join(" · "),
            "pos": [GRID_X + col * (CELL_W + GAP), GAP + row * (CELL_H + GAP)], "size": [CELL_W, CELL_H],
        }));
    }
    json!({
        "schema_version": 1, "diagram_type": "architecture",
        "meta": { "title": format!("{login}: pinned repositories, read from GitHub on {today}"),
                  "output": "cover.html", "quality_profile": "showcase" },
        "components": components,
    })
}

/// This year's commits by `login` with the official trailer, "Co-Authored-By: Claude ...
/// <noreply@anthropic.com>": GitHub's commit search, which covers the default branches of public
/// repositories only.
fn claude(login: &str, year: &str) -> i64 {
    let q = format!("author:{login} author-date:>={year}-01-01 \"noreply@anthropic.com\"");
    let got = Command::new("gh").args(["api", "-X", "GET", "search/commits", "-f", &format!("q={q}"), "-f", "per_page=1", "--jq", ".total_count"])
        .output().expect("cover: gh is not on PATH");
    if !got.status.success() {
        eprintln!("cover: gh search: {}", String::from_utf8_lossy(&got.stderr));
        exit(1);
    }
    String::from_utf8_lossy(&got.stdout).trim().parse().expect("cover: gh search did not answer a count")
}

/// picasso's look (h0ffmann/picasso, site/static/style.css: the ouroboric-dev tokens): its dark
/// palette, one orange accent for the owner's box, Fjalla One for names and Inter for the rest.
/// Archify keeps the geometry; the type is set larger here than Archify's own, since a cover is
/// read from afar and Fjalla One is narrow enough to fit.
const PICASSO: &str = "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Fjalla+One&family=Inter:wght@400;600&display=block\">\
    <style>\
    html,body{background:radial-gradient(60rem 20rem at 10% -40%,color-mix(in srgb,#FF4F00 22%,transparent),transparent 70%),#0B0D12!important}\
    body *{visibility:hidden!important}\
    .diagram-container svg,.diagram-container svg *{visibility:visible!important}\
    .diagram-container svg [data-legend],.diagram-container svg [data-legend] *,\
    .diagram-container svg .semantic-sigil,.diagram-container svg .semantic-sigil *{visibility:hidden!important}\
    .diagram-container svg [fill=\"url(#grid)\"]{display:none}\
    .diagram-container svg [data-detail]{opacity:1!important}\
    .diagram-container svg{position:fixed!important;left:0;top:0;width:100vw!important;height:100vh!important;background:none!important}\
    .diagram-container svg rect.c-mask{fill:#14171F!important}\
    .diagram-container svg rect[class^=c-]:not(.c-mask){fill:#14171F!important;stroke:#2A303C!important;rx:5px}\
    .diagram-container svg rect.c-external:not(.c-mask):not(.c-grid){stroke:#FF4F00!important}\
    .diagram-container svg text.t-primary{font:400 17px 'Fjalla One',sans-serif!important;fill:#EDEFF3!important}\
    .diagram-container svg text.t-muted{font:400 10.5px Inter,sans-serif!important;fill:#9AA3B2!important}\
    .diagram-container svg text.t-external{font:600 8px Inter,sans-serif!important;fill:#FF4F00!important}\
    </style>";

/// The drawing's own bounds, cut to 4:1: Archify will not draw a canvas under 240 units high,
/// and leaves room for its legend below the boxes.
const CROP: (i64, i64) = (GRID_X + COLS * (CELL_W + GAP) + GAP, (GRID_X + COLS * (CELL_W + GAP) + GAP) / 4);

/// Keep only the drawing, in picasso's look, cropped to CROP and fitted to the whole viewport; the
/// layout keeps the photo's corner free.
fn frame(html: &str) -> String {
    let html = html.replacen("</head>", &format!("{PICASSO}</head>"), 1);
    match html.find("<svg viewBox=\"") {
        Some(at) => {
            let start = at + "<svg viewBox=\"".len();
            let close = start + html[start..].find('"').unwrap();
            format!("{}0 0 {} {}{}", &html[..start], CROP.0, CROP.1, &html[close..])
        }
        None => html,
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.iter().map(String::as_str).collect::<Vec<_>>()[1..] {
        ["json", login, out] => {
            let date = |args: &[&str]| String::from_utf8(Command::new("date").args(args).output().unwrap().stdout).unwrap().trim().to_string();
            let today = date(&["-u", "+%F"]);
            let month = date(&["-u", "-d", "30 days ago", "+%FT%TZ"]);
            let got = Command::new("gh").args(["api", "graphql", "-f", &format!("query={QUERY}"), "-F", &format!("login={login}"),
                    "-F", &format!("year={}-01-01T00:00:00Z", &today[..4]), "-F", &format!("month={month}")])
                .output().expect("cover: gh is not on PATH");
            if !got.status.success() {
                eprintln!("cover: gh: {}", String::from_utf8_lossy(&got.stderr));
                exit(1);
            }
            let data: Value = serde_json::from_slice(&got.stdout).expect("cover: gh did not answer JSON");
            let user = &data["data"]["user"];
            if user.is_null() {
                eprintln!("cover: no GitHub user {login}");
                exit(1);
            }
            let d = diagram(user, &today, claude(login, &today[..4]));
            if d["components"].as_array().map_or(0, Vec::len) < 2 {
                eprintln!("cover: {login} pins no public repository");
                exit(1);
            }
            fs::write(out, serde_json::to_string_pretty(&d).unwrap() + "\n").unwrap();
        }
        ["frame", input, out] => fs::write(out, frame(&fs::read_to_string(input).unwrap())).unwrap(),
        _ => {
            eprintln!("usage: cover json <login> <out.json> | cover frame <in.html> <out.html>");
            exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn draws_every_public_pin_in_a_grid_with_the_skills_that_fit() {
        let user = json!({ "login": "a", "createdAt": "2016-02-24T00:00:00Z", "pinnedItems": { "nodes": [
            { "nameWithOwner": "a/open", "isPrivate": false, "primaryLanguage": { "name": "Rust" }, "repositoryTopics": { "nodes": [
                { "topic": { "name": "t1" } }, { "topic": { "name": "t2" } }, { "topic": { "name": "t3" } },
                { "topic": { "name": "t4" } }, { "topic": { "name": "t5" } } ] } },
            { "nameWithOwner": "a/none", "isPrivate": false },
            { "nameWithOwner": "a/other", "isPrivate": false },
            { "nameWithOwner": "b/fourth", "isPrivate": false },
            { "nameWithOwner": "a/hidden", "isPrivate": true },
        ] } });
        let d = diagram(&user, "2026-10-20", 7);
        let c = d["components"].as_array().unwrap();
        let labels: Vec<_> = c.iter().map(|c| c["label"].as_str().unwrap()).collect();
        assert_eq!(labels, ["a · 10 years", "open", "none", "other", "fourth"]);
        assert_eq!(c[0]["sublabel"], "0 contribs · 7 w/ claude");
        assert_eq!(c[1]["sublabel"], "rust · t1 · t2 · t3");
        assert_eq!(c[4]["pos"], json!([GRID_X, GAP + CELL_H + GAP]));
        assert!(d.get("connections").is_none());
    }

    #[test]
    fn languages_of_public_commits_weighed_by_count() {
        let repo = |lang: &str, private: bool, n: i64| json!({ "repository": { "isPrivate": private, "primaryLanguage": { "name": lang } }, "contributions": { "totalCount": n } });
        let user = json!({ "lastMonth": { "commitContributionsByRepository": [
            repo("Gleam", false, 5), repo("C++", false, 9), repo("Gleam", false, 6), repo("Scala", true, 99), repo("Nix", false, 1), repo("R", false, 2),
        ] } });
        assert_eq!(languages(&user), ["gleam", "c++", "r"]);
    }

    #[test]
    fn whole_years() {
        assert_eq!(years("2016-02-24T20:24:18Z", "2026-10-20"), 10);
        assert_eq!(years("2016-10-21T00:00:00Z", "2026-10-20"), 9);
    }

    #[test]
    fn skills_fit_the_box() {
        let topic = |n: &str| json!({ "topic": { "name": n } });
        let repo = json!({ "primaryLanguage": { "name": "Gleam" }, "repositoryTopics": { "nodes": [
            topic("research"), topic("reasearch-data-management"), topic("agents")] } });
        let got = skills(&repo).join(" · ");
        assert!(got.chars().count() <= SKILL_CHARS, "{got}");
        assert_eq!(got, "gleam · research");
    }

    #[test]
    fn frame_injects_once_and_crops_the_drawing() {
        let got = frame("<head></head><head></head><svg viewBox=\"0 0 646 208\" role=\"img\">");
        assert_eq!(got.matches("<style>").count(), 1);
        assert!(got.ends_with(&format!("<svg viewBox=\"0 0 {} {}\" role=\"img\">", CROP.0, CROP.1)), "{got}");
    }
}
