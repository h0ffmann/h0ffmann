#!/usr/bin/env python3
"""
ASD-STE100 structural check:
  - max 25 words per descriptive sentence
  - max 6 sentences per paragraph
"""
import sys, re, os

MAX_WORDS = 25
MAX_SENTENCES = 6

def split_sentences(paragraph):
    # Split on sentence-ending punctuation followed by space or EOL
    parts = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    return [p for p in parts if p.strip()]

def count_words(sentence):
    return len(re.findall(r"\b[\w'-]+\b", sentence))

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip front matter
    content = re.sub(r'^---.*?---\n', '', content, count=1, flags=re.DOTALL)
    # Strip HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    paragraphs = re.split(r'\n\s*\n', content)
    errors = 0

    for i, para in enumerate(paragraphs, 1):
        para = para.strip()
        if not para or para.startswith('#'):
            continue
        sents = split_sentences(para)
        if len(sents) > MAX_SENTENCES:
            print(f"❌ ¶{i}: {len(sents)} sentences (max {MAX_SENTENCES})")
            errors += 1
        for s in sents:
            w = count_words(s)
            if w > MAX_WORDS:
                print(f"❌ ¶{i}: sentence has {w} words (max {MAX_WORDS}): {s[:60]}...")
                errors += 1

    if errors == 0:
        print(f"✅ STE structure OK ({len(paragraphs)} paragraphs checked)")
    return errors == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ste-check.py <file.md>")
        sys.exit(1)
    sys.exit(0 if check_file(sys.argv[1]) else 1)
