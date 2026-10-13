// The few things the content generator needs from Node: files and two git commands.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execSync } from "node:child_process";

// The file's text, or "" when it does not exist.
export function read(path) {
  return existsSync(path) ? readFileSync(path, "utf8") : "";
}

export function write(path, text) {
  writeFileSync(path, text);
}

function git(args, fallback) {
  try {
    return execSync("git " + args, { stdio: ["ignore", "pipe", "ignore"] }).toString().trim();
  } catch (_) {
    return fallback;
  }
}

// The short hash of the commit that is built, or "unversioned" outside a Git checkout.
export function revision() {
  return git("rev-parse --short HEAD", "unversioned");
}

// How many commits changed README.md, and the date of the first: "146 2025-06-25".
// "0 " in a shallow clone or outside a checkout.
export function readme_commits() {
  const dates = git("log --follow --format=%as -- ../../README.md", "");
  if (dates === "") return "0 ";
  const lines = dates.split("\n");
  return lines.length + " " + lines[lines.length - 1];
}

// The words of an SVG card, with its styles and tags taken out and its spaces made single.
export function card_text(path) {
  if (!existsSync(path)) return "";
  return readFileSync(path, "utf8")
    .replace(/<style[\s\S]*?<\/style>/g, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}
