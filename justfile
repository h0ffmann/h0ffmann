# h0ffmann. Every check and every build has a recipe here, and CI runs the same recipes: the
# shape of marola-dev/marola-research's and h0ffmann/closed-source's justfile. The tools come
# from flake.nix, pinned in flake.lock.

set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# The website (www/): www/content/*.md, one per language, into www/dist, which is committed
# because CI is off. `just www --check` fails when www/dist is stale.
www *args:
    python3 www/build.py {{args}}

# The ASD-STE100 check (www/ste/Ste.agda, in Agda): the English page and llms.txt. Its proofs
# are checked when it compiles. `just ste FILE...` checks other files.
ste *files:
    nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#ste --command just _ste {{files}}

_ste *files:
    cd www/ste && LC_ALL=C.UTF-8 agda --compile --compile-dir=../../build/ste Ste.agda > /dev/null
    LC_ALL=C.UTF-8 build/ste/Ste {{ if files == "" { "www/content/en.md llms.txt" } else { files } }}

nixb := "nix --extra-experimental-features 'nix-command flakes'"

# The short CV in English (cv/summary.md, the look of the site) and the three long ones (the
# READMEs). Commit them with the change, as marola-research commits a paper with its text.
# Render the four CVs into pdf/.
cv:
    python3 -m unittest discover -s cv
    # Built from the last commit, not from the files on disk: the short CV names that commit in
    # its foot, and the PDFs of pdf/ would make any tree look changed. Commit the sources first.
    git diff --quiet HEAD -- . ':!pdf' || { echo "cv: commit the sources first; the CV is built from the last commit" >&2; exit 1; }
    {{nixb}} build --no-update-lock-file --out-link build/cv "git+file://$PWD?rev=$(git rev-parse HEAD)"
    mkdir -p pdf && install -m 644 build/cv/*.pdf pdf/
    @for f in pdf/*.pdf; do echo "cv: $f ($(pdfinfo "$f" 2>/dev/null | awk '/^Pages/ {print $2}') pages)"; done

# The committed CVs are the ones their sources make. What CI's `pdf` runs.
current:
    {{nixb}} build --no-update-lock-file --out-link build/cv
    {{nixb}} develop --no-update-lock-file --command python3 scripts/cv-current.py build/cv pdf

# Read the featured repositories again from GitHub: the counts, the commits and the commit each
# one was reviewed at. The list is site/data/featured.tsv. It needs `gh`, signed in.
# Write FEATURED_REPO.md. `just featured --check` only looks for each row.
featured *args:
    python3 scripts/featured.py {{args}}

# One text for each featured repository, sized for LinkedIn's "Projects" (DERIVATION.md).
# Write LINKEDIN_PROJECTS.md. `just linkedin --check` fails when it is stale.
linkedin *args:
    python3 scripts/linkedin-projects.py {{args}}

# The LinkedIn cover (1584x396) of the public repositories that h0ffmann pins: cover/ (Rust) reads
# them with `gh` and writes Archify's input, vendor/archify draws it and checks it, Chrome takes the
# picture. Write build/cover/h0ffmann/cover.png. Only for h0ffmann (AGENTS.md, hard rule 5).
cover:
    nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#cover --command just _cover h0ffmann

# The tests of cover/.
cover-test:
    nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#cover --command bash -c 'cd cover && cargo test -q'

_cover login:
    [ "{{login}}" = h0ffmann ] || { echo "cover: only h0ffmann (AGENTS.md, hard rule 5)" >&2; exit 2; }
    # vendor/archify is a pinned submodule, sparse to archify/: a fresh clone checks it out once.
    [ -f vendor/archify/archify/bin/archify.mjs ] || { git submodule update --init --depth 1 vendor/archify && git -C vendor/archify sparse-checkout set --no-cone /archify/; }
    rm -rf build/cover/{{login}} && mkdir -p build/cover/{{login}}
    cd cover && cargo run -q -- json {{login}} ../build/cover/{{login}}/cover.json
    ARCHIFY_UPDATE_CHECK_DISABLED=1 node vendor/archify/archify/bin/archify.mjs finalize architecture build/cover/{{login}}/cover.json build/cover/{{login}}/cover.html --out-dir build/cover/{{login}}/receipts --quality showcase --json > build/cover/{{login}}/finalize.json || { cat build/cover/{{login}}/finalize.json >&2; exit 1; }
    cd cover && cargo run -q -- frame ../build/cover/{{login}}/pills.svg ../build/cover/{{login}}/cover.html ../build/cover/{{login}}/frame.html
    "${CHROME:-google-chrome}" --headless --disable-gpu --hide-scrollbars --force-dark-mode --user-data-dir="$PWD/build/cover/{{login}}/profile" --window-size=1584,396 --virtual-time-budget=3000 --screenshot="$PWD/build/cover/{{login}}/cover.png" "file://$PWD/build/cover/{{login}}/frame.html" 2>/dev/null
    rm -rf build/cover/{{login}}/profile
    @echo "cover: build/cover/{{login}}/cover.png"

# Every public source repository of h0ffmann, marola-dev and piabrota (site/data/repos.tsv), every
# public fork (site/data/forks.tsv), and their most used GitHub topics (site/data/topics.tsv,
# site/data/fork_topics.tsv), read again from GitHub with `gh`; then the two topic clouds:
# vendor/archify places and checks the boxes, scripts/topics-frame.py sizes each word by its box,
# Chromium (Playwright) takes site/static/topics.png and site/static/fork-topics.png.
# `just topics --self-test` runs the script's own test.
topics *args:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "{{args}}" = --self-test ]; then python3 scripts/repos.py --self-test; exit; fi
    [ -f vendor/archify/archify/bin/archify.mjs ] || { git submodule update --init --depth 1 vendor/archify && git -C vendor/archify sparse-checkout set --no-cone /archify/; }
    rm -rf build/topics build/forks && mkdir -p build/topics build/forks
    python3 scripts/repos.py --archify build/topics/topics.json
    python3 scripts/repos.py --forks --forks-archify build/forks/topics.json
    for d in topics:topics forks:fork-topics; do
      (cd "build/${d%%:*}"
       ARCHIFY_UPDATE_CHECK_DISABLED=1 node ../../vendor/archify/archify/bin/archify.mjs finalize architecture topics.json topics.html --out-dir receipts --quality showcase --json > finalize.json || { cat finalize.json >&2; exit 1; }
       python3 ../../scripts/topics-frame.py topics.html cloud.html
       node ../../scripts/topics-shot.mjs cloud.html "../../site/static/${d##*:}.png")
    done

# Every logo of the timeline still answers at its owner's address. A logo is never a file here.
logos:
    for u in $(grep -v '^#' site/data/timeline.tsv | cut -f6 | grep -E '^https://' | sort -u); do code="$(curl -s -o /dev/null -L --max-time 30 -A 'Mozilla/5.0' -w '%{http_code}' "$u")"; [ "$code" = 200 ] || { echo "logos: $code $u" >&2; exit 1; }; done
    @echo "logos: every logo answers"

md := "nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#md --command"

# Three analysers over the Markdown files: markdownlint-cli2, Vale, lychee.
# `just md-quality --online` also fetches every web link; `--self-test` gives each one a bad file.
md-quality *args:
    {{md}} scripts/md-quality.sh {{args}}

# The slip box keeps its rules (NOTES.md).
notes:
    scripts/notes-check.sh

# Every row of the site's tables has its cells and its source.
sources:
    scripts/sources-check.sh

# Write CITATION.cff from .zenodo.json. `just citation --check` fails when it is stale.
citation *args:
    {{md}} python3 scripts/citation.py {{args}}

# Licence and copyright for every file (REUSE.toml).
reuse:
    {{md}} reuse lint

# What CI's `.md / quality` runs. Run it before a pull request.
check:
    just md-quality --self-test
    just md-quality
    just notes
    just sources
    just citation --check
    just reuse
    python3 -m unittest discover -s cv
    just featured --check
    just linkedin --check

