import gleeunit
import profile_content as generate

pub fn main() -> Nil {
  gleeunit.main()
}

pub fn rows_skip_comments_and_empty_lines_test() {
  assert generate.rows("# a\tb\nx\ty\n\n# c\nz\t\n") == [["x", "y"], ["z", ""]]
}

pub fn plain_takes_the_marks_out_test() {
  assert generate.plain(
      "with **8 years**, for **[marola-dev](https://x)** and `nagori`",
    )
    == "with 8 years, for marola-dev and nagori"
}

pub fn paragraph_is_the_first_one_under_the_heading_test() {
  let readme =
    "# h\n\n## 👋 me\n\nsr. engineer with **8 years**.\n<!-- cv:skip -->\n<p>x</p>\n\n## 🏅 certs\n\n**aws certified 4x** (a, b)\n\n## next\n"
  assert generate.paragraph(readme, "## 👋 me") == "sr. engineer with 8 years."
  assert generate.paragraph(readme, "## 🏅 certs") == "aws certified 4x (a, b)"
  assert generate.paragraph(readme, "## missing") == ""
}

pub fn headings_are_the_third_level_ones_test() {
  assert generate.headings(
      "# a\n## b\n### people who read\ntext\n### money first\n",
    )
    == ["people who read", "money first"]
}

pub fn numbers_are_read_from_a_card_test() {
  let card =
    "mhoffmann Joined GitHub 10 years ago Followed by 85 users Contributed to 54 repositories Activity 4140 Commits 8 Pull requests reviewed"
  assert generate.number_before(card, "Commits") == 4140
  assert generate.number_before(card, "repositories") == 54
  assert generate.number_before(card, "Stars") == 0
}

pub fn languages_are_read_from_a_card_test() {
  let card =
    "12 Languages Most used languages estimation from 14.2mb of code in 4069 edited files across 764 commits Nix 20.3 kB 0.71% Scala 1.27 MB 44.2% Jupyter Notebook 500 kB 17.38%"
  assert generate.languages(card)
    == [#("Scala", "44.2%"), #("Jupyter Notebook", "17.38%"), #("Nix", "0.71%")]
  assert generate.languages("no card") == []
}
