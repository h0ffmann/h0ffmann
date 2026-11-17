#!/usr/bin/env python3
"""Build www/dist from www/content/*.md: one page per language, no dependencies.

The Markdown is a small subset: front matter, `# heading`, `---` and paragraphs with
[links](url); a link that starts with ./ is relative to the site root. The repository's llms.txt
is copied beside the pages, and so is every file of www/static. Everything before the first `---` is the centred header. `--check` fails when the committed
www/dist is not what the content makes (CI is off, so the output is committed).

The published posts of posts/ go on the site too, in English: one page each at posts/<slug>/,
listed on every language page. A post with `status: draft` in its front matter stays off the
site (`just post-list` lists them all with their status).
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT, DIST = ROOT / "content", ROOT / "dist"
POSTS = ROOT.parent / "posts"
ORDER = ["en", "pt-BR", "ja", "es"]

STYLE = """html { background: #000; color: #fff; }
body { max-width: 650px; margin: 0 auto; padding: 12px; font-family: serif; position: relative; }
h1 { margin: 0; }
p { margin: 0.25em 0; }
header, footer { text-align: center; }
header { padding: 0 76px; min-height: 64px; }
a { color: #fff; }
hr { border: 0; border-top: 1px solid #fff; }
.avatar { position: absolute; top: 12px; left: 12px; width: 64px; height: 64px; border-radius: 50%; border: 2px solid #fff; box-sizing: border-box; }"""


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        sys.exit(f"www: {path.name} has no front matter")
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
    return meta, m.group(2).strip()


def inline(s, up=""):
    out, last = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", s):
        out.append(html.escape(s[last:m.start()]))
        href = up + m.group(2)[2:] if m.group(2).startswith("./") else m.group(2)
        out.append(f'<a href="{html.escape(href)}">{html.escape(m.group(1))}</a>')
        last = m.end()
    out.append(html.escape(s[last:]))
    return "".join(out)


def blocks(md, up):
    out = []
    # A standalone HTML comment line is scaffolding, not prose (the posts' STE skeleton).
    md = re.sub(r"(?m)^[ \t]*<!--.*-->[ \t]*\n?", "", md)
    for b in re.split(r"\n\s*\n", md):
        b = b.strip()
        if b == "---":
            out.append("<hr>")
        elif re.match(r"#{1,6} ", b):
            # The site has one heading style: every level shows as its h1.
            out.append(f"<h1>{inline(b[b.index(' ') + 1:], up)}</h1>")
        else:
            out.append("<p>" + "<br>\n".join(inline(l, up) for l in b.splitlines()) + "</p>")
    return out


def page(meta, md, pages, posts):
    up = "" if meta["dir"] == "." else "../"
    body = blocks(md, up)
    cut = body.index("<hr>") if "<hr>" in body else len(body)
    listed = posts_line(posts, up)
    switch = " - ".join(
        f"<b>{p['locale']}</b>" if p is meta
        else f'<a href="{up}{"" if p["dir"] == "." else p["dir"] + "/"}" hreflang="{p["lang"]}" lang="{p["lang"]}">{p["locale"]}</a>'
        for p in pages)
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{p["lang"]}" href="{up}{"" if p["dir"] == "." else p["dir"] + "/"}">'
        for p in pages)
    return f"""<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>{html.escape(meta['title'])}</title>
  <meta name="description" content="{html.escape(meta['description'])}">
{alternates}
  <link rel="alternate" type="text/plain" title="llms.txt" href="{up}llms.txt">
  <style>
{STYLE}
  </style>
</head>
<body>
  <header>
    <img class="avatar" src="{up}avatar.png" width="64" height="64" alt="">
    {chr(10).join(body[:cut])}
  </header>
  {chr(10).join(body[cut:])}
  {listed}
  <br>
  <hr>
  <footer>{switch} · <a href="{up}llms.txt">llms.txt</a></footer>
</body>
</html>
"""


def load_posts():
    # posts/<date>-<slug>.md; newest first. `status: draft` stays off the site.
    out = []
    for path in sorted(POSTS.glob("*.md"), reverse=True):
        meta, md = parse(path)
        if meta.get("status") == "draft":
            continue
        stem = path.stem
        slug = stem[11:] if re.match(r"\d{4}-\d{2}-\d{2}-", stem) else stem
        out.append({
            "slug": slug,
            "date": meta.get("date", ""),
            "title": meta["title"].strip('"'),
            "md": md,
        })
    return out


def posts_line(posts, up):
    if not posts:
        return ""
    items = " - ".join(
        f'<a href="{up}posts/{p["slug"]}/">{html.escape(p["title"])}</a>' for p in posts)
    return f"<p>posts: {items}</p>"


def post_page(post):
    # A post is in English whatever the reader's locale; `../..` climbs out of posts/<slug>/.
    up = "../.."
    body = blocks(post["md"], up)
    description = html.escape(next(
        (re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", b.strip())
         for b in re.split(r"\n\s*\n", post["md"])
         if b.strip() and not b.strip().startswith("<!--")
         and b.strip() != "---" and not re.match(r"#{1,6} ", b.strip())), ""))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>{html.escape(post['title'])}</title>
  <meta name="description" content="{description}">
  <link rel="alternate" type="text/plain" title="llms.txt" href="{up}/llms.txt">
  <style>
{STYLE}
  </style>
</head>
<body>
  <header>
    <img class="avatar" src="{up}/avatar.png" width="64" height="64" alt="">
    <h1>{html.escape(post['title'])}</h1>
    <p>{html.escape(post['date'])}</p>
  </header>
  {chr(10).join(body)}
  <br>
  <hr>
  <footer><a href="{up}/">hffmnn</a> · <a href="{up}/llms.txt">llms.txt</a></footer>
</body>
</html>
"""


def build():
    posts = load_posts()
    pages, mds = [], {}
    for name in ORDER:
        meta, md = parse(CONTENT / f"{name}.md")
        pages.append(meta)
        mds[id(meta)] = md
    files = {
        (Path(p["dir"]) / "index.html").as_posix(): page(p, mds[id(p)], pages, posts)
        for p in pages
    }
    for post in posts:
        files[f"posts/{post['slug']}/index.html"] = post_page(post)
    # The index for language models is the repository's own, served beside the pages.
    files["llms.txt"] = (ROOT.parent / "llms.txt").read_text(encoding="utf-8")
    return files


STATIC = ROOT / "static"  # copied into dist as they are (the avatar)


def main():
    files = build()
    if "--check" in sys.argv:
        stale = [f for f, s in files.items()
                 if not (DIST / f).exists() or (DIST / f).read_text(encoding="utf-8") != s]
        stale += [f.name for f in sorted(STATIC.iterdir())
                  if not (DIST / f.name).exists() or (DIST / f.name).read_bytes() != f.read_bytes()]
        if stale:
            sys.exit("www: stale, run `just www`: " + ", ".join(stale))
        print("www: dist is current")
        return
    for f, s in files.items():
        (DIST / f).parent.mkdir(parents=True, exist_ok=True)
        (DIST / f).write_text(s, encoding="utf-8")
        print(f"www: dist/{f}")
    for f in sorted(STATIC.iterdir()):
        (DIST / f.name).write_bytes(f.read_bytes())
        print(f"www: dist/{f.name}")


if __name__ == "__main__":
    main()
