#!/usr/bin/env python3
"""Extract markdown links and check HTTP status (non-fatal on 403/timeout)."""
import sys, re, urllib.request, urllib.error

def check_links(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'\]\((https?://[^)]+)\)', content)
    if not links:
        print("ℹ️  No external links found")
        return True
    ok = True
    for url in set(links):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'h0ffmann-harness/1.0'})
            with urllib.request.urlopen(req, timeout=8) as r:
                print(f"✅ {r.status}  {url}")
        except urllib.error.HTTPError as e:
            print(f"⚠️  {e.code}  {url}")
            if e.code >= 500: ok = False
        except Exception as e:
            print(f"⚠️  ERR  {url} ({e})")
    return ok

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: links-check.py <file.md>")
        sys.exit(1)
    sys.exit(0 if check_links(sys.argv[1]) else 1)
