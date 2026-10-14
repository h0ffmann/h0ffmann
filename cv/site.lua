-- site.lua: the look of the site, for the short CV (cv/summary.md, cv/site.tex, DESIGN.md).
-- 1. A link to a file of this repository becomes a link to github.com: a PDF has no folder
--    beside it, so a relative link in it opens nothing.
-- 2. The fenced blocks of cv/summary.md become the environments of cv/site.tex.
-- 3. The tip at the end gains the commit that the PDF was built from (CV_COMMIT, from flake.nix).
local repo = "https://github.com/h0ffmann/h0ffmann"
local lights = { water = true, ideas = true, ouroboric = true, closed = true }

local function raw(s) return pandoc.RawInline("latex", s) end
local function rawb(s) return pandoc.RawBlock("latex", s) end

-- "../me/a.md#x" seen from cv/ is "me/a.md#x" from the root.
local function absolute(target)
  if target:match("^%a[%w+.-]*:") or target:match("^#") then return target end
  local parts = { "cv" }
  local path, frag = target:match("^([^#]*)(#?.*)$")
  for part in path:gmatch("[^/]+") do
    if part == ".." then table.remove(parts) elseif part ~= "." then table.insert(parts, part) end
  end
  return repo .. "/blob/main/" .. table.concat(parts, "/") .. frag
end

local function light_of(el)
  for _, c in ipairs(el.classes) do if lights[c] then return c end end
end

local function wrap(inlines, before, after)
  local out = pandoc.List({ raw(before) })
  out:extend(inlines)
  out:insert(raw(after))
  return out
end

local link_macro = "\\cvlink"

function Link(el)
  el.target = absolute(el.target)
  local macro = el.classes:includes("data") and "\\cvdoi" or link_macro
  el.classes = {}
  el.content = wrap(el.content, macro .. "{", "}")
  return el
end

function Span(el)
  if el.classes:includes("data") then return wrap(el.content, "{\\cvdata ", "}") end
  local light = light_of(el)
  if light then return wrap(el.content, "{\\color{" .. light .. "}", "}") end
end

function Header(el)
  if el.level == 1 then return pandoc.Plain(wrap(el.content, "\\cvname{", "}")) end
  if el.level == 2 then return pandoc.Plain(wrap(el.content, "\\cvsection{", "}")) end
end

local function env(el, name, arg)
  local blocks = pandoc.List({ rawb("\\begin{" .. name .. "}" .. (arg or "")) })
  blocks:extend(el.content)
  blocks:insert(rawb("\\end{" .. name .. "}"))
  return blocks
end

-- The arc: each item is "[when]{.data} what" and becomes one row, the date in its own column.
local function arc(el)
  local rows = pandoc.List()
  for _, block in ipairs(el.content) do
    if block.t == "BulletList" then
      for _, item in ipairs(block.content) do
        local inlines = pandoc.List(item[1].content)
        local when = table.remove(inlines, 1)
        while inlines[1] and inlines[1].t == "Space" do table.remove(inlines, 1) end
        local row = pandoc.List({ raw("\\cvrow{") })
        row:insert(when)
        row:insert(raw("}{"))
        row:extend(inlines)
        row:insert(raw("}"))
        rows:insert(pandoc.Plain(row))
      end
    end
  end
  return rows
end

local function tip(el)
  local commit = os.getenv("CV_COMMIT") or ""
  if commit:match("^%x+$") and #commit >= 7 then
    local last = el.content[#el.content]
    last.content:extend({ pandoc.Space(), pandoc.Str("built"), pandoc.Space(), pandoc.Str("from"),
      pandoc.Space(), pandoc.Str("commit"), pandoc.Space(),
      raw("\\href{" .. repo .. "/commit/" .. commit .. "}{\\cvdoi{" .. commit:sub(1, 7) .. "}}"),
      pandoc.Str(".") })
  end
  return env(el, "cvtip")
end

function Div(el)
  if el.classes:includes("epithet") then return env(el, "cvepithet") end
  if el.classes:includes("lede") then return env(el, "cvlede") end
  if el.classes:includes("contact") then return env(el, "cvcontact") end
  if el.classes:includes("pair") then
    -- two halves, side by side: the first ends its column
    local blocks, seen = pandoc.List({ rawb("\\begin{cvpair}") }), 0
    for _, block in ipairs(el.content) do
      if seen == 1 then blocks:insert(rawb("\\columnbreak")) end
      seen = seen + 1
      blocks:insert(block)
    end
    blocks:insert(rawb("\\end{cvpair}"))
    return blocks
  end
  if el.classes:includes("works") then return env(el, "cvworks") end
  if el.classes:includes("work") then return env(el, "cvwork", "{" .. (light_of(el) or "muted") .. "}") end
  if el.classes:includes("tip") then return tip(el) end
end

-- Inside the contact block a link is a pill, not an underlined word. Divs are visited after
-- their links and spans (bottom up), so the pills and the rows of the arc, which read their
-- own spans, are made in a first pass of their own.
local pills = {
  Div = function(el)
    if el.classes:includes("arc") then return arc(el) end
    if el.classes:includes("contact") then
      return el:walk({
        Link = function(l) l.classes:insert("pill"); return l end,
        SoftBreak = function() return pandoc.Space() end,
      })
    end
  end,
}
-- The tip is the foot of the page (cv/site.tex), and a foot must be known before its page is
-- sent out: the two columns at the end can send the page before a block after them is read.
-- So the tip is written last in cv/summary.md and moved to the start here.
function pills.Pandoc(doc)
  for i, block in ipairs(doc.blocks) do
    if block.t == "Div" and block.classes:includes("tip") then
      table.insert(doc.blocks, 1, table.remove(doc.blocks, i))
      return doc
    end
  end
end

local function pill_links(el)
  if el.classes:includes("pill") then
    el.target = absolute(el.target)
    el.classes = {}
    el.content = wrap(el.content, "\\cvpill{", "}")
    return el, false
  end
end

return {
  pills,
  { Link = function(el) local a, b = pill_links(el); if a then return a end return Link(el) end,
    Span = Span, Header = Header },
  { Div = Div },
}
