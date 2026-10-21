//! The LinkedIn cover: a GitHub user's pinned FOSS repositories as an Archify architecture diagram.
//!
//!     cover json <login> <out.json>     read the pinned repositories with `gh`, write Archify's input
//!     cover frame <in.html> <out.html>  keep only the drawing, sized for a 1584x396 capture
use serde_json::{json, Value};
use std::process::{exit, Command};
use std::{env, fs};

const QUERY: &str = "query($login: String!) { user(login: $login) { login name
  pinnedItems(first: 6, types: REPOSITORY) { nodes { ... on Repository {
    nameWithOwner description url isPrivate stargazerCount
    licenseInfo { spdxId } primaryLanguage { name } } } } } }";

const NODE_W: i64 = 190;
const GAP: i64 = 30;

/// FOSS here means public with a licence GitHub could name: no licence, or "NOASSERTION", is not open.
fn foss(repo: &Value) -> bool {
    let spdx = repo["licenseInfo"]["spdxId"].as_str().unwrap_or("NOASSERTION");
    !repo["isPrivate"].as_bool().unwrap_or(true) && spdx != "NOASSERTION"
}

fn diagram(user: &Value, today: &str) -> Value {
    let login = user["login"].as_str().unwrap_or("");
    let repos: Vec<&Value> = user["pinnedItems"]["nodes"].as_array().into_iter().flatten().filter(|r| foss(r)).collect();
    let row = repos.len().max(1) as i64 * (NODE_W + GAP) - GAP;
    let mut components = vec![json!({
        "id": "user", "type": "external", "label": login,
        "sublabel": user["name"].as_str().unwrap_or("github"),
        "pos": [40 + (row - 220) / 2, 40], "size": [220, 64],
    })];
    let mut connections = vec![];
    for (i, r) in repos.iter().enumerate() {
        let id = format!("repo-{i}");
        let lang = r["primaryLanguage"]["name"].as_str().unwrap_or("code");
        components.push(json!({
            "id": id, "type": "backend",
            "label": r["nameWithOwner"].as_str().unwrap_or("").rsplit('/').next(),
            "sublabel": format!("{lang} · {}", r["licenseInfo"]["spdxId"].as_str().unwrap_or("")),
            "tag": format!("★ {}", r["stargazerCount"].as_i64().unwrap_or(0)),
            "pos": [40 + i as i64 * (NODE_W + GAP), 220], "size": [NODE_W, 64],
        }));
        connections.push(json!({ "id": format!("pins-{i}"), "from": "user", "to": id }));
    }
    json!({
        "schema_version": 1, "diagram_type": "architecture",
        "meta": { "title": format!("{login}: pinned FOSS repositories, read from GitHub on {today}"),
                  "output": "cover.html", "quality_profile": "showcase" },
        "components": components, "connections": connections,
    })
}

/// Hide everything but the drawing (and its legend) and fit it to the viewport, leaving the left quarter empty:
/// LinkedIn puts the profile photo over the bottom left of the cover.
fn frame(html: &str) -> String {
    let css = "<style>body *{visibility:hidden!important}\
        .diagram-container svg,.diagram-container svg *{visibility:visible!important}\
        .diagram-container svg [data-legend],.diagram-container svg [data-legend] *{visibility:hidden!important}\
        .diagram-container svg{position:fixed!important;left:25vw;top:4vh;width:72vw!important;height:92vh!important}</style>";
    html.replacen("</head>", &format!("{css}</head>"), 1)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.iter().map(String::as_str).collect::<Vec<_>>()[1..] {
        ["json", login, out] => {
            let got = Command::new("gh").args(["api", "graphql", "-f", &format!("query={QUERY}"), "-F", &format!("login={login}")])
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
            let today = String::from_utf8(Command::new("date").arg("+%F").output().unwrap().stdout).unwrap();
            let d = diagram(user, today.trim());
            if d["connections"].as_array().map_or(true, |c| c.is_empty()) {
                eprintln!("cover: {login} pins no public repository with a licence");
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
    fn keeps_only_public_licensed_repositories() {
        let user = json!({ "login": "a", "pinnedItems": { "nodes": [
            { "nameWithOwner": "a/open", "isPrivate": false, "licenseInfo": { "spdxId": "MIT" } },
            { "nameWithOwner": "a/none", "isPrivate": false, "licenseInfo": null },
            { "nameWithOwner": "a/other", "isPrivate": false, "licenseInfo": { "spdxId": "NOASSERTION" } },
            { "nameWithOwner": "a/hidden", "isPrivate": true, "licenseInfo": { "spdxId": "MIT" } },
        ] } });
        let d = diagram(&user, "2026-10-20");
        let labels: Vec<_> = d["components"].as_array().unwrap().iter().map(|c| c["label"].as_str().unwrap()).collect();
        assert_eq!(labels, ["a", "open"]);
        assert_eq!(d["connections"].as_array().unwrap().len(), 1);
    }

    #[test]
    fn frame_injects_once_before_head_end() {
        assert_eq!(frame("<head></head><head></head>").matches("<style>").count(), 1);
    }
}
