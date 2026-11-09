// The picture of the topic cloud: Chromium, through Playwright, takes the page that
// scripts/topics-frame.py made, down to the bottom of Archify's notes.
//   node scripts/topics-shot.mjs IN.html OUT.png
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";

const [input, output] = process.argv.slice(2);
if (!input || !output) {
  console.error("usage: node scripts/topics-shot.mjs IN.html OUT.png");
  process.exit(2);
}
const { chromium } = createRequire(path.join(process.cwd(), "x.js"))("playwright");
const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2, colorScheme: "dark" });
await page.goto(pathToFileURL(path.resolve(input)).href);
await page.waitForSelector('g[id^="node-t-"][data-cloud]');
await page.waitForTimeout(800);
const bottom = await page.evaluate(() => Math.max(...[...document.querySelectorAll(".cards")].map((e) => e.getBoundingClientRect().bottom)));
await page.screenshot({ path: output, clip: { x: 0, y: 0, width: 1280, height: Math.ceil(bottom + 24) } });
await browser.close();
console.log(`topics-shot: ${output}`);
