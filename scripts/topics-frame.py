#!/usr/bin/env python3
"""Turn Archify's drawing of the topic cloud into a word cloud.

    python3 scripts/topics-frame.py IN.html OUT.html

Archify (vendor/archify) places and checks the boxes that scripts/repos.py sized by each topic's
count, but draws every label at one size. This adds a script to the page that sets each word's
size from its box (0.42 of its height), so the most used topic is the biggest word, takes the icon
off each box and lightens its border. It hides the viewer's controls and its index of nodes: the
page is made to be a picture (`just topics`). Archify's viewer draws the diagram again when the reader
changes the theme, so the script runs on every drawing, not once. Nothing is moved: the geometry
is Archify's, and the words are the topics it was given.
"""
import sys

SCRIPT = """<style>.no-print, .toolbar, .export-wrap { display: none !important; }</style>
<script>
(() => {
  const size = () => {
    for (const g of document.querySelectorAll('g[id^="node-t-"]:not([data-cloud])')) {
      const r = g.querySelector('rect');
      if (!r) continue;
      g.setAttribute('data-cloud', '');
      const y = +r.getAttribute('y'), h = +r.getAttribute('height');
      g.querySelector('[data-semantic-sigil]')?.remove();
      for (const b of g.querySelectorAll('rect[stroke-width]')) b.setAttribute('stroke-opacity', '0.35');
      const word = g.querySelector('text[data-node-label]');
      if (word) { word.setAttribute('font-size', (0.42 * h).toFixed(1)); word.setAttribute('y', (y + 0.56 * h).toFixed(1)); }
      const count = g.querySelector('text[data-detail="context"]');
      if (count) { count.setAttribute('font-size', '8'); count.setAttribute('y', (y + h - 4).toFixed(1)); }
    }
  };
  new MutationObserver(size).observe(document.documentElement, { childList: true, subtree: true });
  size();
})();
</script>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    html = open(argv[0], encoding="utf-8").read()
    if 'id="node-t-' not in html or "</body>" not in html:
        print("topics-frame: no topic box found in the drawing", file=sys.stderr)
        return 1
    open(argv[1], "w", encoding="utf-8").write(html.replace("</body>", SCRIPT + "</body>", 1))
    print(f"topics-frame: wrote {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
