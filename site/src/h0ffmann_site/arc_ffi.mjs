// The browser's half of the sideways arc. app.gleam decides where the timeline is; this file reads
// the page (where the section is, how wide the timeline is) and writes what was decided. When the
// page is rendered at build time there is no document, and nothing happens.
let stage, track;

export function watch(frame) {
  const doc = globalThis.document;
  if (!doc) return;
  // After the first render, so that the section exists.
  requestAnimationFrame(() => {
    const section = doc.querySelector(".arc-scroll");
    stage = section?.querySelector(".arc-stage");
    track = section?.querySelector(".timeline");
    if (!track || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    section.dataset.flow = "row";
    let queued = false;
    const tick = () => {
      queued = false;
      const box = section.getBoundingClientRect();
      frame(box.top, box.height, innerHeight, stage.clientWidth, track.scrollWidth, track.firstElementChild.offsetWidth);
    };
    const ask = () => {
      if (!queued) {
        queued = true;
        requestAnimationFrame(tick);
      }
    };
    addEventListener("scroll", ask, { passive: true });
    addEventListener("resize", ask);
    // Fonts and logos change the timeline's width after the first frame.
    new ResizeObserver(ask).observe(track);
    tick();
  });
}

export function place(length, x, now, era) {
  stage.parentElement.style.setProperty("--len", `${length}px`);
  track.style.setProperty("--x", `${x}px`);
  [...track.children].forEach((li, i) => li.toggleAttribute("data-now", i === now));
  for (const li of stage.querySelectorAll(".eras li")) li.toggleAttribute("data-now", li.dataset.era === era);
}
