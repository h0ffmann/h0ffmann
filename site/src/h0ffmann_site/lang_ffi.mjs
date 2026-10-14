// The language of the page: one value for the whole page, read by `app.t` each time a sentence is
// drawn. It starts from the address (`?lang=pt-BR`), then from what the reader chose before, then
// from English. When the page is rendered at build time there is no browser, and it is English.
const KNOWN = ["en", "pt-BR"];
let current = "en";

try {
  const asked = new URLSearchParams(globalThis.location?.search ?? "").get("lang");
  const kept = globalThis.localStorage?.getItem("lang");
  const first = [asked, kept].find((l) => KNOWN.includes(l));
  if (first) current = first;
} catch (_) {
  // No address and no storage: the page is being rendered at build time.
}

export function get() {
  return current;
}

export function set(lang) {
  current = KNOWN.includes(lang) ? lang : "en";
  try {
    globalThis.document.documentElement.lang = current;
    globalThis.localStorage?.setItem("lang", current);
  } catch (_) {
    // A reader who blocks storage still gets the language for this visit.
  }
  return current;
}
