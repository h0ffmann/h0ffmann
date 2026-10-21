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
    nameWithOwner description url isPrivate stargazerCount
    licenseInfo { spdxId } primaryLanguage { name }
    repositoryTopics(first: 10) { nodes { topic { name } } } } } } } }";

const NODE_W: i64 = 360;
const NODE_H: i64 = 64;
const ROW: i64 = 92;
const USER_X: i64 = 40 + NODE_W + 100;
const USER_W: i64 = 360;
const LANGUAGES: usize = 3;
const SKILLS: usize = 5;
const TAG: usize = 66;
const DESC: usize = 64;

/// Every public pin, as GitHub lists it: a pin with no licence, or "NOASSERTION", is still drawn.
fn public(repo: &Value) -> bool {
    !repo["isPrivate"].as_bool().unwrap_or(true)
}

/// The skills of a pin: its language, then its GitHub topics in GitHub's order, five at most,
/// and fewer when the line would pass TAG characters, the width of a box.
fn skills(repo: &Value) -> Vec<String> {
    let topics = repo["repositoryTopics"]["nodes"].as_array().into_iter().flatten();
    repo["primaryLanguage"]["name"].as_str().into_iter().map(str::to_lowercase)
        .chain(topics.filter_map(|t| t["topic"]["name"].as_str().map(String::from)))
        .take(SKILLS)
        .fold(vec![], |mut kept: Vec<String>, s| {
            if kept.iter().map(|k| k.chars().count() + 3).sum::<usize>() + s.chars().count() <= TAG {
                kept.push(s);
            }
            kept
        })
}

/// shortcut: a description longer than DESC characters is cut with "…"; GitHub keeps it whole.
fn short(text: &str) -> String {
    let text = text.trim();
    if text.chars().count() <= DESC { text.to_string() } else { text.chars().take(DESC - 1).collect::<String>() + "…" }
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

/// The user in the middle, the pins in two columns of up to three: the first half on the left.
fn diagram(user: &Value, today: &str, claude: i64) -> Value {
    let login = user["login"].as_str().unwrap_or("");
    let repos: Vec<&Value> = user["pinnedItems"]["nodes"].as_array().into_iter().flatten().filter(|r| public(r)).collect();
    let left = repos.len().div_ceil(2);
    let rows = left.max(1) as i64;
    let mut components = vec![json!({
        "id": "user", "type": "external", "label": login,
        "sublabel": format!("{} years · {} contributions · {claude} commits with claude in {}",
            years(user["createdAt"].as_str().unwrap_or(today), today),
            user["thisYear"]["contributionCalendar"]["totalContributions"].as_i64().unwrap_or(0), &today[..4]),
        "tag": format!("last 30 days: {}", languages(user).join(" · ")),
        "pos": [USER_X, 40 + (rows * ROW - ROW + NODE_H) / 2 - 40], "size": [USER_W, 80],
    })];
    let mut connections = vec![];
    for (i, r) in repos.iter().enumerate() {
        let (side, x, row) = if i < left { ("left", 40, i) } else { ("right", USER_X + USER_W + 100, i - left) };
        let id = format!("repo-{i}");
        components.push(json!({
            "id": id, "type": "backend",
            "label": r["nameWithOwner"].as_str().unwrap_or(""),
            "sublabel": short(r["description"].as_str().unwrap_or("")),
            "pos": [x, 40 + row as i64 * ROW], "size": [NODE_W, NODE_H],
        }));
        let tag = skills(r).join(" · ");
        if !tag.is_empty() {
            components.last_mut().unwrap()["tag"] = json!(tag);
        }
        let to = if side == "left" { "right" } else { "left" };
        connections.push(json!({ "id": format!("pins-{i}"), "from": "user", "to": id, "fromSide": side, "toSide": to }));
    }
    json!({
        "schema_version": 1, "diagram_type": "architecture",
        "meta": { "title": format!("{login}: pinned repositories, read from GitHub on {today}"),
                  "output": "cover.html", "quality_profile": "showcase" },
        "components": components, "connections": connections,
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

/// Hide everything but the drawing (and its legend), show every detail (the tags) and fit it to the viewport, leaving the left quarter empty:
/// LinkedIn puts the profile photo over the bottom left of the cover.
fn frame(html: &str) -> String {
    let css = "<style>body *{visibility:hidden!important}\
        .diagram-container svg,.diagram-container svg *{visibility:visible!important}\
        .diagram-container svg [data-legend],.diagram-container svg [data-legend] *{visibility:hidden!important}\
        .diagram-container svg [data-detail]{opacity:1!important}\
        .diagram-container svg{position:fixed!important;left:25vw;top:4vh;width:72vw!important;height:92vh!important}</style>";
    html.replacen("</head>", &format!("{css}</head>"), 1)
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
            if d["connections"].as_array().map_or(true, |c| c.is_empty()) {
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
    fn draws_every_public_pin_with_five_skills_at_most() {
        let user = json!({ "login": "a", "pinnedItems": { "nodes": [
            { "nameWithOwner": "a/open", "isPrivate": false, "primaryLanguage": { "name": "Rust" }, "repositoryTopics": { "nodes": [
                { "topic": { "name": "t1" } }, { "topic": { "name": "t2" } }, { "topic": { "name": "t3" } },
                { "topic": { "name": "t4" } }, { "topic": { "name": "t5" } } ] } },
            { "nameWithOwner": "a/none", "isPrivate": false, "licenseInfo": null },
            { "nameWithOwner": "a/other", "isPrivate": false, "licenseInfo": { "spdxId": "NOASSERTION" } },
            { "nameWithOwner": "a/hidden", "isPrivate": true, "licenseInfo": { "spdxId": "MIT" } },
        ] } });
        let d = diagram(&user, "2026-10-20", 0);
        let c = d["components"].as_array().unwrap();
        let labels: Vec<_> = c.iter().map(|c| c["label"].as_str().unwrap()).collect();
        assert_eq!(labels, ["a", "a/open", "a/none", "a/other"]);
        assert_eq!(c[1]["tag"], "rust · t1 · t2 · t3 · t4");
        assert!(c[3].get("tag").is_none());
        assert_eq!(c[3]["pos"][0].as_i64().unwrap() > c[1]["pos"][0].as_i64().unwrap(), true);
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
        let long = |n: &str| json!({ "topic": { "name": format!("{n}-{}", "x".repeat(20)) } });
        let repo = json!({ "primaryLanguage": { "name": "Gleam" }, "repositoryTopics": { "nodes": [long("a"), long("b"), long("c"), long("d")] } });
        let got = skills(&repo).join(" · ");
        assert!(got.chars().count() <= TAG, "{got}");
        assert_eq!(skills(&repo).len(), 3);
    }

    #[test]
    fn a_long_description_is_cut() {
        assert_eq!(short("ocean intelligence layer"), "ocean intelligence layer");
        let cut = short(&"x".repeat(90));
        assert_eq!(cut.chars().count(), DESC);
        assert!(cut.ends_with('…'));
    }

    #[test]
    fn frame_injects_once_before_head_end() {
        assert_eq!(frame("<head></head><head></head>").matches("<style>").count(), 1);
    }
}
