-- links.lua: a link to a file of this repository becomes a link to github.com. A PDF has no
-- folder beside it, so a relative link in it ("me/ways-of-working.md") opens nothing.
-- The long CVs are built from the READMEs at the root, so a relative path is from the root.
local base = "https://github.com/h0ffmann/h0ffmann/blob/main/"
function Link(el)
  if not (el.target:match("^%a[%w+.-]*:") or el.target:match("^#")) then
    el.target = base .. el.target:gsub("^%./", "")
  end
  return el
end
