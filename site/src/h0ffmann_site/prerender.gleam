//// `gleam run -m h0ffmann_site/prerender > dist/index.html`: the first render, which the client
//// then takes over in place, so the page reads without JavaScript.

import gleam/io
import h0ffmann_site/app
import h0ffmann_site/page
import lustre/element

pub fn main() -> Nil {
  app.initial()
  |> app.view
  |> page.document
  |> element.to_document_string
  |> io.println
}
