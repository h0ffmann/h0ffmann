-- Every emoji becomes \cvemoji{emoji_u1f30a}: vector Noto artwork (cv/emoji/*.svg, converted to
-- PDF by cv/build.sh) instead of a font glyph — see cv/cvemoji.py for why. Runs after
-- shields-badges.lua, so badge text (raw LaTeX by then) is covered too. The original character
-- stays as the PDF-string alternative, so bookmarks keep it.
-- Same rules as `sequences` in cv/cvemoji.py — change both together.
local VS16, ZWJ = 0xFE0F, 0x200D

local function is_flag(c) return c and c >= 0x1F1E6 and c <= 0x1F1FF end
local function is_modifier(c) return c and (c == VS16 or (c >= 0x1F3FB and c <= 0x1F3FF)) end
local function is_base(c)
  return c and ((c >= 0x2600 and c <= 0x27BF) or (c >= 0x2B00 and c <= 0x2BFF)
    or (c >= 0x1F000 and c <= 0x1F1E5) or (c >= 0x1F200 and c <= 0x1F3FA) or (c >= 0x1F400 and c <= 0x1FAFF))
end

-- end index of the emoji starting at cps[i], or nil
local function sequence_end(cps, i)
  if is_flag(cps[i]) then return is_flag(cps[i + 1]) and i + 1 or nil end
  if not is_base(cps[i]) then return nil end
  local j = i
  while true do
    while is_modifier(cps[j + 1]) do j = j + 1 end
    if cps[j + 1] == ZWJ and is_base(cps[j + 2]) then j = j + 2 else return j end
  end
end

local function macro(cps, i, j)
  local hex = {}
  for k = i, j do
    if cps[k] ~= VS16 then hex[#hex + 1] = string.format("%x", cps[k]) end
  end
  return "\\texorpdfstring{\\cvemoji{emoji_u" .. table.concat(hex, "_") .. "}}{" .. utf8.char(table.unpack(cps, i, j)) .. "}"
end

-- text split into plain strings and emoji macros: { {text = "..."} | {tex = "..."} }, or nil if no emoji
local function split(text)
  if not text:find("[\xE2\xF0]") then return nil end
  local cps = {}
  for _, c in utf8.codes(text) do cps[#cps + 1] = c end
  local parts, plain, i, found = {}, {}, 1, false
  while i <= #cps do
    local j = sequence_end(cps, i)
    if j then
      if #plain > 0 then parts[#parts + 1] = { text = utf8.char(table.unpack(plain)) }; plain = {} end
      parts[#parts + 1] = { tex = macro(cps, i, j) }
      i, found = j + 1, true
    else
      plain[#plain + 1] = cps[i]
      i = i + 1
    end
  end
  if #plain > 0 then parts[#parts + 1] = { text = utf8.char(table.unpack(plain)) } end
  return found and parts or nil
end

local function raw(text)
  local parts = split(text)
  if not parts then return nil end
  local out = {}
  for _, part in ipairs(parts) do out[#out + 1] = part.tex or part.text end
  return table.concat(out)
end

return { {
  Str = function(el)
    local parts = split(el.text)
    if not parts then return nil end
    local inlines = {}
    for _, part in ipairs(parts) do
      inlines[#inlines + 1] = part.tex and pandoc.RawInline("latex", part.tex) or pandoc.Str(part.text)
    end
    return inlines
  end,
  RawInline = function(el)
    local tex = el.format == "latex" and raw(el.text)
    return tex and pandoc.RawInline("latex", tex) or nil
  end,
  RawBlock = function(el)
    local tex = el.format == "latex" and raw(el.text)
    return tex and pandoc.RawBlock("latex", tex) or nil
  end,
} }
