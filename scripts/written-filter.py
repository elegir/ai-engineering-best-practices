#!/usr/bin/env python3
"""written-filter.py — is this written source (doc, paper, article, course) already in the registry?

Usage:
  python3 scripts/written-filter.py <url> [<url> ...]
  python3 scripts/written-filter.py --file urls.txt        (one URL per line; '#' comments allowed)

Prints one line per URL: NEW, or the registry status + module + reason. Nothing is written;
register decisions by hand (type "written", status catalogued | cited | discarded) as the
playbook says. Ids are the URL without scheme, "www." and trailing slash.
"""
import json, os, re, sys

def nid(u): return re.sub(r'^https?://(www\.)?', '', u.strip()).rstrip('/')

def main():
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(1)
    if args[0] == '--file':
        urls = [l.strip() for l in open(args[1]) if l.strip() and not l.startswith('#')]
    else:
        urls = args
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg = json.load(open(os.path.join(root, 'sources', 'media-registry.json')))
    known = {e['id']: e for e in reg['items']}
    new = 0
    for u in urls:
        e = known.get(nid(u))
        if e: print(f"KNOWN  [{e['status']}, {e['module']}] {u} — {e['reason'][:90]}")
        else: print(f"NEW    {u}"); new += 1
    print(f"\n{new} new, {len(urls)-new} already in the registry")

if __name__ == '__main__': main()
