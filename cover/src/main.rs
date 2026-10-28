//! The LinkedIn cover: the public repositories that h0ffmann pins on GitHub, as an Archify architecture diagram.
//!
//!     cover json <login> <out.json>     read the pinned repositories with `gh`, write Archify's input
//!                                       and the pills (pills.svg, beside it)
//!     cover frame <pills.svg> <in.html> <out.html>  keep only the drawing, sized for a 1584x396 capture
use serde_json::{json, Value};
use std::process::{exit, Command};
use std::collections::BTreeSet;
use std::path::Path;
use std::{env, fs};

const QUERY: &str = "query($login: String!, $year: DateTime!, $month: DateTime!) { user(login: $login) { login name createdAt
  thisYear: contributionsCollection(from: $year) { contributionCalendar { totalContributions } }
  lastMonth: contributionsCollection(from: $month) { commitContributionsByRepository(maxRepositories: 100) {
    repository { nameWithOwner isPrivate } } }
  pinnedItems(first: 6, types: REPOSITORY) { nodes { ... on Repository {
    nameWithOwner isPrivate stargazerCount primaryLanguage { name } owner { __typename login }
    defaultBranchRef { target { ... on Commit { history { totalCount } } } }
    repositoryTopics(first: 10) { nodes { topic { name } } } } } } } }";

// The canvas, in Archify's units: small, so that Archify's own type comes out about 2.2 times
// larger when Chrome stretches it to 1584x396, and LinkedIn's profile page (about 800 px wide)
// still shows the names at some 19 px. The pins take a grid of 3x2 on the right; the user's box
// sits top left, above where LinkedIn puts the profile photo.
const COLS: i64 = 3;
const CELL_W: i64 = 152;
const CELL_H: i64 = 60;
const GAP: i64 = 10;
// The rows sit further apart, for the pills astride a box's bottom edge.
const ROW_GAP: i64 = 16;
const USER_W: i64 = 204;
const GRID_X: i64 = USER_W + 2 * GAP;
const LANGUAGES: usize = 3;
// The skills share the sublabel line of a box: 9px type, 5.4 units a character (Archify's
// authoring defaults), less the box's padding.
const SKILL_CHARS: usize = 24;

/// Every public pin, as GitHub lists it, with a licence or without.
fn public(repo: &Value) -> bool {
    !repo["isPrivate"].as_bool().unwrap_or(true)
}

/// The pins the cover draws: every public one, and a private one the owner marked `lock`.
fn shown(repo: &Value) -> bool {
    public(repo) || marked(CHOSEN, repo["nameWithOwner"].as_str().unwrap_or(""), "lock")
}

/// The skills the owner chose, by repository (site/data/cover.tsv).
const CHOSEN: &str = include_str!("../../site/data/cover.tsv");

fn row<'a>(table: &'a str, repo: &str) -> Option<Vec<&'a str>> {
    table.lines().filter(|l| !l.starts_with('#')).map(|l| l.split('\t').collect::<Vec<_>>())
        .find(|cells| cells.first() == Some(&repo))
}

fn chosen(table: &str, repo: &str) -> Option<Vec<String>> {
    row(table, repo).and_then(|cells| cells.get(1).copied()).filter(|s| !s.is_empty())
        .map(|s| s.split(", ").map(String::from).collect())
}

/// Whether the owner put `mark` on a pin's box (site/data/cover.tsv, marks).
fn marked(table: &str, repo: &str, mark: &str) -> bool {
    row(table, repo).and_then(|cells| cells.get(2).copied()).is_some_and(|m| m.split(", ").any(|x| x == mark))
}

/// The works with their DOIs (site/data/works.tsv).
const WORKS: &str = include_str!("../../site/data/works.tsv");

/// The DOI of the work named like the repository, if it has one.
fn doi<'a>(works: &'a str, repo: &str) -> Option<&'a str> {
    row(works, repo.rsplit('/').next().unwrap_or("")).and_then(|cells| cells.get(4).copied()).filter(|d| !d.is_empty())
}

/// The skills of a pin: the owner's choice when site/data/cover.tsv has one, all of it; otherwise
/// its language, then its GitHub topics in GitHub's order, as many as fit in SKILL_CHARS characters.
fn skills(repo: &Value) -> Vec<String> {
    if let Some(mine) = chosen(CHOSEN, repo["nameWithOwner"].as_str().unwrap_or("")) {
        return mine;
    }
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

/// The programming language of a file, by its extension. Shell, Nix, Just, data and documents are
/// left out: they are glue around the code in every repository.
fn language(path: &str) -> Option<&'static str> {
    Some(match path.rsplit_once('.')?.1 {
        "c" => "c",
        "cpp" | "cc" | "cxx" | "hpp" | "hh" | "h" | "cu" => "c++",
        "gleam" => "gleam",
        "go" => "go",
        "hs" => "haskell",
        "java" => "java",
        "jl" => "julia",
        "js" | "mjs" | "cjs" | "jsx" => "javascript",
        "kt" => "kotlin",
        "py" => "python",
        "r" | "R" => "r",
        "rs" => "rust",
        "scala" | "sc" => "scala",
        "ts" | "tsx" => "typescript",
        "f" | "f90" | "F90" => "fortran",
        _ => return None,
    })
}

/// The languages of the last 30 days from `git log --name-only --format=@` of the owner's
/// commits: a commit counts once for each language of the files it changed, the most first.
fn ranked(log: &str) -> Vec<String> {
    let mut count: Vec<(&str, i64)> = vec![];
    for commit in log.split('@') {
        let langs: BTreeSet<&str> = commit.lines().filter_map(language).collect();
        for lang in langs {
            match count.iter_mut().find(|(l, _)| *l == lang) {
                Some((_, total)) => *total += 1,
                None => count.push((lang, 1)),
            }
        }
    }
    count.sort_by(|a, b| b.1.cmp(&a.1));
    count.into_iter().take(LANGUAGES).map(|(l, _)| l.to_string()).collect()
}

/// The owner's commits of the last 30 days in each public repository committed to (GitHub's list,
/// which counts the commits it links to the account, not other authors'), as `ranked` reads them:
/// their files come from a clone of the repository without its blobs, in `dir`.
fn touched(login: &str, user: &Value, month: &str, dir: &Path) -> String {
    let mut log = String::new();
    for c in user["lastMonth"]["commitContributionsByRepository"].as_array().into_iter().flatten() {
        let repo = c["repository"]["nameWithOwner"].as_str().unwrap_or("");
        if !public(&c["repository"]) {
            continue;
        }
        let shas = gh(&["api", "--paginate", &format!("repos/{repo}/commits?author={login}&since={month}&per_page=100"), "--jq", ".[].sha"]);
        if shas.trim().is_empty() {
            continue;
        }
        let at = dir.join(repo.replace('/', "_"));
        if !at.exists() {
            run("git", &["clone", "-q", "--bare", "--filter=blob:none", &format!("https://github.com/{repo}"), at.to_str().unwrap()]);
        }
        let mut args = vec!["-C", at.to_str().unwrap(), "log", "--no-walk=unsorted", "--ignore-missing", "--name-only", "--format=format:@"];
        args.extend(shas.split_whitespace());
        log += &run("git", &args);
    }
    log
}

/// Run a command; stop the cover with its error when it fails.
fn run(cmd: &str, args: &[&str]) -> String {
    let got = Command::new(cmd).args(args).output().unwrap_or_else(|_| panic!("cover: {cmd} is not on PATH"));
    if !got.status.success() {
        eprintln!("cover: {cmd} {}: {}", args.iter().take(6).copied().collect::<Vec<_>>().join(" "), String::from_utf8_lossy(&got.stderr));
        exit(1);
    }
    String::from_utf8_lossy(&got.stdout).into_owned()
}

fn gh(args: &[&str]) -> String {
    run("gh", args)
}

/// "1 commit", "2 commits".
fn count(n: i64, noun: &str) -> String {
    format!("{n} {noun}{}", if n == 1 { "" } else { "s" })
}

/// Whole years from `since` to `today`, both "YYYY-MM-DD...".
fn years(since: &str, today: &str) -> i64 {
    let year = |d: &str| d.get(..4).and_then(|y| y.parse::<i64>().ok()).unwrap_or(0);
    year(today) - year(since) - i64::from(today.get(5..10) < since.get(5..10))
}

/// Where the i-th pin sits: a grid of COLS columns right of the user's box.
fn place(i: usize) -> [i64; 2] {
    let (col, row) = (i as i64 % COLS, i as i64 / COLS);
    [GRID_X + col * (CELL_W + GAP), GAP + row * (CELL_H + ROW_GAP)]
}

/// The user's box top left, the pins in a grid (each with its default branch's commits) of three columns to its right, in GitHub's order.
/// No lines: on a cover every box is read on its own, and six lines from one box are noise.
fn diagram(user: &Value, today: &str, claude: i64) -> Value {
    let login = user["login"].as_str().unwrap_or("");
    let repos: Vec<&Value> = user["pinnedItems"]["nodes"].as_array().into_iter().flatten().filter(|r| shown(r)).collect();
    let mut components = vec![json!({
        "id": "user", "type": "external",
        "label": format!("{login} · {} years", years(user["createdAt"].as_str().unwrap_or(today), today)),
        "sublabel": format!("{}: {} contribs · {claude} w/ claude", &today[..4],
            user["thisYear"]["contributionCalendar"]["totalContributions"].as_i64().unwrap_or(0)),
        "tag": format!("30d: {}", user["languages"].as_array().into_iter().flatten().filter_map(Value::as_str).collect::<Vec<_>>().join(" · ")),
        "pos": [GAP, GAP], "size": [USER_W, CELL_H],
    })];
    for (i, r) in repos.iter().enumerate() {
        let name = r["nameWithOwner"].as_str().unwrap_or("");
        // A pin the owner marked `org` stands for its organisation: its name, its counts.
        let (label, commits, people) = match r.get("org") {
            Some(org) => (org["login"].as_str().unwrap_or(""), &org["commits"], &org["contributors"]),
            None => (name.rsplit('/').next().unwrap_or(""), &r["defaultBranchRef"]["target"]["history"]["totalCount"], &r["contributors"]),
        };
        components.push(json!({
            "id": format!("repo-{i}"), "type": "backend",
            "label": label,
            "sublabel": skills(r).join(" · "),
            "tag": format!("{} · {}", count(commits.as_i64().unwrap_or(0), "commit"), count(people.as_i64().unwrap_or(0), "contributor")),
            "pos": place(i), "size": [CELL_W, CELL_H],
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

/// The people who committed to a repository's default branch, as GitHub links them to accounts:
/// its accounts of type User, less the account "claude", whose commits the owner's box counts.
fn contributors(repo: &str) -> Vec<String> {
    // shortcut: one page of 100 contributors, enough for every pin today; paginate if a pin passes it.
    // An empty repository answers nothing.
    gh(&["api", &format!("repos/{repo}/contributors?per_page=100"),
        "--jq", ".[] | select(.type == \"User\" and .login != \"claude\") | .login"])
        .lines().map(String::from).collect()
}

const ORG: &str = "query($login: String!) { organization(login: $login) {
  repositories(privacy: PUBLIC, isFork: false, first: 100) { totalCount nodes { nameWithOwner stargazerCount
    defaultBranchRef { target { ... on Commit { history { totalCount } } } } } } } }";

/// An organisation's counts over its public source repositories: how many, their commits, and the
/// contributors of any of them, each once.
fn org(login: &str) -> Value {
    // shortcut: the first 100 repositories; paginate when an organisation passes it.
    let data: Value = serde_json::from_str(&gh(&["api", "graphql", "-f", &format!("query={ORG}"), "-F", &format!("login={login}")]))
        .expect("cover: gh did not answer JSON");
    let repos = &data["data"]["organization"]["repositories"];
    let nodes = repos["nodes"].as_array().cloned().unwrap_or_default();
    let commits: i64 = nodes.iter().map(|n| n["defaultBranchRef"]["target"]["history"]["totalCount"].as_i64().unwrap_or(0)).sum();
    let people: BTreeSet<String> = nodes.iter().flat_map(|n| contributors(n["nameWithOwner"].as_str().unwrap_or(""))).collect();
    let stars: i64 = nodes.iter().map(|n| n["stargazerCount"].as_i64().unwrap_or(0)).sum();
    json!({ "login": login, "repos": repos["totalCount"], "commits": commits, "contributors": people.len(), "stars": stars })
}

/// picasso's look (h0ffmann/picasso, site/static/style.css: the ouroboric-dev tokens): its dark
/// palette, one accent for the owner's box, in the blue of marola's logo (#1BADC5, the middle stop of its gradient, marola-dev/marola docs/assets/logo.svg at d0d576e), Fjalla One for names and Inter for the rest.
/// Archify keeps the geometry; the type is set larger here than Archify's own, since a cover is
/// read from afar and Fjalla One is narrow enough to fit.
const PICASSO: &str = "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Fjalla+One&family=Inter:wght@400;600&display=block\">\
    <style>\
    html,body{background:radial-gradient(60rem 20rem at 10% -40%,color-mix(in srgb,#1BADC5 22%,transparent),transparent 70%),#0B0D12!important}\
    body *{visibility:hidden!important}\
    .diagram-container svg,.diagram-container svg *{visibility:visible!important}\
    .diagram-container svg [data-legend],.diagram-container svg [data-legend] *,\
    .diagram-container svg .semantic-sigil,.diagram-container svg .semantic-sigil *{visibility:hidden!important}\
    .diagram-container svg [fill=\"url(#grid)\"]{display:none}\
    .diagram-container svg [data-detail]{opacity:1!important}\
    .diagram-container svg{position:fixed!important;left:0;top:0;width:100vw!important;height:100vh!important;background:none!important}\
    .diagram-container svg rect.c-mask{fill:#14171F!important}\
    .diagram-container svg rect[class^=c-]:not(.c-mask){fill:#14171F!important;stroke:#2A303C!important;rx:5px}\
    .diagram-container svg rect.c-external:not(.c-mask):not(.c-grid){stroke:#1BADC5!important}\
    .diagram-container svg text.t-primary{font:400 17px 'Fjalla One',sans-serif!important;fill:#EDEFF3!important}\
    .diagram-container svg text.t-muted{font:400 10.5px Inter,sans-serif!important;fill:#9AA3B2!important}\
    .diagram-container svg text.t-external{font:600 8px Inter,sans-serif!important;fill:#1BADC5!important}\
    .diagram-container svg text.t-backend{font:600 8px Inter,sans-serif!important;fill:#EDEFF3!important}\
    .diagram-container svg text.t-primary{transform:translateY(-5px)}\
    .diagram-container svg text.t-muted{transform:translateY(-3px)}\
    .diagram-container svg text.t-backend,.diagram-container svg text.t-external{transform:translateY(2px)}\
    </style>";

/// The drawing's own bounds, cut to 4:1: Archify will not draw a canvas under 240 units high,
/// and leaves room for its legend below the boxes.
const CROP: (i64, i64) = (GRID_X + COLS * (CELL_W + GAP) + GAP, (GRID_X + COLS * (CELL_W + GAP) + GAP) / 4);

/// A pill with an address, astride the top edge of the box at `at`: a cover is a picture, and its
/// reader types the address. Text, not GitHub's mark (AGENTS.md, hard rule 4).
fn pill(text: &str, at: [i64; 2], color: &str) -> String {
    pill_at(text, [at[0] + 10, at[1] - 6], color)
}

/// A pill whose top left is at `at`, 12 units high.
fn pill_at(text: &str, at: [i64; 2], color: &str) -> String {
    // The text is set to 3.6 units a character (textLength), whatever the face's own widths; a star
    // is as wide as two.
    let t = text.chars().map(|c| if c == '★' { 2 } else { 1 }).sum::<i64>() * 18 / 5;
    let w = t + 10;
    format!("<g class=\"gh-pill\"><rect x=\"{}\" y=\"{}\" width=\"{w}\" height=\"12\" rx=\"6\" fill=\"#0B0D12\" stroke=\"{color}\"/>\
        <text x=\"{}\" y=\"{}\" text-anchor=\"middle\" textLength=\"{t}\" lengthAdjust=\"spacing\" style=\"font:600 7px Inter,sans-serif;fill:{color}\">{text}</text></g>",
        at[0], at[1], at[0] + w / 2, at[1] + 8)
}

/// Brazil's flag, drawn (green field, yellow rhombus, blue disc), 15x10 units, astride the top
/// edge of the box at `at`, in its right corner, clear of a pill.
fn brazil(at: [i64; 2]) -> String {
    let (x, y) = (at[0] + CELL_W - 16, at[1] - 5);
    format!("<g class=\"flag-br\"><rect x=\"{x}\" y=\"{y}\" width=\"15\" height=\"10\" rx=\"1\" fill=\"#009C3B\"/>\
        <polygon points=\"{} {},{} {},{} {},{} {}\" fill=\"#FFDF00\"/><circle cx=\"{}\" cy=\"{}\" r=\"2.4\" fill=\"#002776\"/></g>",
        x as f64 + 7.5, y + 1, x + 14, y as f64 + 5.0, x as f64 + 7.5, y + 9, x + 1, y as f64 + 5.0, x as f64 + 7.5, y as f64 + 5.0)
}

/// Noto Emoji's padlock (cv/emoji, Apache-2.0), LOCK units square, after the name of the box at
/// `at`, whose label Archify centres: the name's width is guessed at NAME_W units a character of
/// Fjalla One at 17px, the size the frame sets.
const NOTO_LOCK: &str = include_str!("../../cv/emoji/emoji_u1f512.svg");
const LOCK: f64 = 13.0;
const NAME_W: f64 = 8.8;

fn padlock(name: &str, at: [i64; 2]) -> String {
    let x = at[0] as f64 + CELL_W as f64 / 2.0 + name.chars().count() as f64 * NAME_W / 2.0 + 3.0;
    let y = at[1] as f64 + 9.0;
    let svg = &NOTO_LOCK[NOTO_LOCK.find("<svg").unwrap_or(0)..];
    format!("<g class=\"lock\">{}</g>", svg.replacen("x=\"0px\" y=\"0px\"", &format!("x=\"{x}\" y=\"{y}\" width=\"{LOCK}\" height=\"{LOCK}\""), 1))
}

/// The pills: the owner's address in the accent, and each organisation's, with its repositories, in
/// grey; and the flags the owner gave the pins.
fn pills(user: &Value) -> String {
    let repos = user["pinnedItems"]["nodes"].as_array().into_iter().flatten().filter(|r| shown(r));
    let mut out = pill(&format!("github.com/{}", user["login"].as_str().unwrap_or("")), [GAP, GAP], "#1BADC5");
    for (i, r) in repos.enumerate() {
        let name = r["nameWithOwner"].as_str().unwrap_or("");
        if marked(CHOSEN, name, "br") {
            out += &brazil(place(i));
        }
        if marked(CHOSEN, name, "lock") {
            let label = r.get("org").and_then(|o| o["login"].as_str()).unwrap_or(name.rsplit('/').next().unwrap_or(""));
            out += &padlock(label, place(i));
        }
        // Below the box's bottom edge, clear of its last line: the DOI on the left, the stars on the right.
        let [x, y] = place(i);
        if let Some(d) = doi(WORKS, name).filter(|_| marked(CHOSEN, name, "doi")) {
            out += &pill_at(&format!("doi:{d}"), [x + 6, y + CELL_H - 3], "#9AA3B2");
        }
        let stars = r.get("org").unwrap_or(r)["stars"].as_i64().or(r["stargazerCount"].as_i64()).unwrap_or(0);
        if stars > 0 {
            let text = format!("★ {stars}");
            out += &pill_at(&text, [x + CELL_W - 6 - ((text.chars().count() as i64 + 1) * 18 / 5 + 10), y + CELL_H - 3], "#9AA3B2");
        }
        if let Some(org) = r.get("org") {
            out += &pill(&format!("github.com/{} · {}", org["login"].as_str().unwrap_or(""), count(org["repos"].as_i64().unwrap_or(0), "repo")),
                place(i), "#9AA3B2");
        }
    }
    out
}

/// Keep only the drawing, in picasso's look, cropped to CROP and fitted to the whole viewport, with
/// the pills; the layout keeps the photo's corner free.
fn frame(html: &str, pills: &str) -> String {
    let html = html.replacen("</head>", &format!("{PICASSO}</head>"), 1).replacen("</svg>", &format!("{pills}</svg>"), 1);
    match html.find("<svg viewBox=\"") {
        Some(at) => {
            let start = at + "<svg viewBox=\"".len();
            let close = start + html[start..].find('"').unwrap();
            // The grid is 2 rows high; the 4:1 crop is taller, so the grid sits in its middle.
            let top = (CROP.1 - (2 * GAP + ROW_GAP + 2 * CELL_H)) / 2;
            format!("{}0 {} {} {}{}", &html[..start], -top, CROP.0, CROP.1, &html[close..])
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
            let mut data = data;
            if data["data"]["user"].is_null() {
                eprintln!("cover: no GitHub user {login}");
                exit(1);
            }
            for r in data["data"]["user"]["pinnedItems"]["nodes"].as_array_mut().into_iter().flatten() {
                if shown(r) {
                    let name = r["nameWithOwner"].as_str().unwrap_or("").to_string();
                    r["contributors"] = json!(contributors(&name).len());
                    if r["owner"]["__typename"] == "Organization" && marked(CHOSEN, &name, "org") {
                        r["org"] = org(r["owner"]["login"].as_str().unwrap_or(""));
                    }
                }
            }
            let clones = Path::new(out).with_file_name("clones");
            let langs = ranked(&touched(login, &data["data"]["user"], &month, &clones));
            data["data"]["user"]["languages"] = json!(langs);
            let user = &data["data"]["user"];
            let d = diagram(user, &today, claude(login, &today[..4]));
            if d["components"].as_array().map_or(0, Vec::len) < 2 {
                eprintln!("cover: {login} pins no public repository");
                exit(1);
            }
            fs::write(out, serde_json::to_string_pretty(&d).unwrap() + "\n").unwrap();
            fs::write(Path::new(out).with_file_name("pills.svg"), pills(user)).unwrap();
        }
        ["frame", pills, input, out] => fs::write(out, frame(&fs::read_to_string(input).unwrap(), &fs::read_to_string(pills).unwrap())).unwrap(),
        _ => {
            eprintln!("usage: cover json <login> <out.json> | cover frame <pills.svg> <in.html> <out.html>");
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
            { "nameWithOwner": "a/none", "isPrivate": false, "contributors": 3, "defaultBranchRef": { "target": { "history": { "totalCount": 42 } } } },
            { "nameWithOwner": "a/other", "isPrivate": false },
            { "nameWithOwner": "b/fourth", "isPrivate": false },
            { "nameWithOwner": "a/hidden", "isPrivate": true },
        ] } });
        let d = diagram(&user, "2026-10-20", 7);
        let c = d["components"].as_array().unwrap();
        let labels: Vec<_> = c.iter().map(|c| c["label"].as_str().unwrap()).collect();
        assert_eq!(labels, ["a · 10 years", "open", "none", "other", "fourth"]);
        assert_eq!(c[0]["sublabel"], "2026: 0 contribs · 7 w/ claude");
        assert_eq!(c[1]["sublabel"], "rust · t1 · t2 · t3 · t4");
        assert_eq!(c[2]["tag"], "42 commits · 3 contributors");
        assert_eq!(c[3]["tag"], "0 commits · 0 contributors");
        assert_eq!(count(1, "commit"), "1 commit");
        assert_eq!(c[4]["pos"], json!([GRID_X, GAP + CELL_H + ROW_GAP]));
        assert!(d.get("connections").is_none());
    }

    #[test]
    fn languages_by_the_files_each_commit_changed() {
        // A commit counts once per language; shell, nix and documents count for none.
        let log = "@\n\na.rs\nb.rs\nflake.nix\n@\n\nsrc/x.gleam\nREADME.md\n@\n\ny.gleam\nz.rs\n@\n\nrun.sh\n@\n\nk.cpp\n";
        assert_eq!(ranked(log), ["rust", "gleam", "c++"]);
        assert_eq!(language("Makefile"), None);
    }

    #[test]
    fn an_organisations_pin_shows_the_organisation() {
        let user = json!({ "login": "a", "pinnedItems": { "nodes": [
            { "nameWithOwner": "o/r", "isPrivate": false, "contributors": 1, "stargazerCount": 2,
              "org": { "login": "o", "repos": 12, "commits": 1446, "contributors": 6, "stars": 9 } },
            { "nameWithOwner": "h0ffmann/ptbr-writer", "isPrivate": false, "stargazerCount": 0 } ] } });
        let c = diagram(&user, "2026-10-22", 0)["components"].as_array().unwrap().clone();
        assert_eq!(c[1]["label"], "o");
        assert_eq!(c[1]["tag"], "1446 commits · 6 contributors");
        let p = pills(&user);
        assert!(p.contains(">github.com/a</text>") && p.contains(">github.com/o · 12 repos</text>"), "{p}");
        assert_eq!(p.matches("flag-br").count(), 1, "ptbr-writer carries the flag (site/data/cover.tsv)");
        assert!(p.contains(">★ 9</text>") && !p.contains(">★ 0<"), "the organisation's stars, none for 0: {p}");
        assert!(marked(CHOSEN, "marola-dev/marola", "br") && marked(CHOSEN, "marola-dev/marola", "doi"));
        assert!(!marked(CHOSEN, "h0ffmann/ptbr-writer", "doi"));
        assert_eq!(doi(WORKS, "h0ffmann/ww3-gpu"), Some("10.5281/zenodo.23221351"));
        assert_eq!(doi(WORKS, "h0ffmann/ptbr-writer"), None);
        // A row with no skills keeps the topics.
        assert_eq!(chosen(CHOSEN, "h0ffmann/ww3-gpu"), None);
    }

    #[test]
    fn a_private_pin_shows_only_with_its_lock() {
        let user = json!({ "login": "a", "pinnedItems": { "nodes": [
            { "nameWithOwner": "h0ffmann/ww3-gpu", "isPrivate": true },
            { "nameWithOwner": "a/hidden", "isPrivate": true },
            { "nameWithOwner": "o/r", "isPrivate": false } ] } });
        let c = diagram(&user, "2026-10-28", 0)["components"].as_array().unwrap().clone();
        let labels: Vec<_> = c.iter().map(|c| c["label"].as_str().unwrap()).collect();
        assert_eq!(&labels[1..], ["ww3-gpu", "r"], "an organisation's repository without `org` keeps its own name");
        let p = pills(&user);
        assert_eq!(p.matches("class=\"lock\"").count(), 1, "{p}");
        assert_eq!(p.matches("<?xml").count(), 0);
        assert!(marked(CHOSEN, "marola-dev/marola", "org") && !marked(CHOSEN, "piabrota/alerts", "org"));
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
    fn the_owners_choice_comes_first() {
        let table = "# repository\tskills\tsource\nb/x\tnix, rust\tthe owner\n";
        assert_eq!(chosen(table, "b/x"), Some(vec!["nix".to_string(), "rust".to_string()]));
        assert_eq!(chosen(table, "b/y"), None);
        assert_eq!(skills(&json!({ "nameWithOwner": "h0ffmann/closed-source" })), ["open-book", "paper research"]);
    }

    #[test]
    fn frame_injects_once_and_crops_the_drawing() {
        let got = frame("<head></head><head></head><svg viewBox=\"0 0 646 208\" role=\"img\"></svg>", "<g>pills</g>");
        assert_eq!(got.matches("<style>").count(), 1);
        assert!(got.contains("<g>pills</g></svg>"), "{got}");
        let top = (CROP.1 - (2 * GAP + ROW_GAP + 2 * CELL_H)) / 2;
        assert!(got.contains(&format!("<svg viewBox=\"0 {} {} {}\" role=\"img\">", -top, CROP.0, CROP.1)));
    }
}
