#!/usr/bin/env python3
"""scan-filter.py — drop already-decided media from a new Apify scan result.

The knowledge base keeps sources/media-registry.json: every video or podcast episode ever
considered, with a status (transcribed / digested / applied / candidate / discarded) and the
reason. A new market scan (playbooks/scan-market-for-module.md) must only spend attention on
items that are NOT already in the registry, so this script splits a scan result into
"new" and "already decided".

Usage:
  python3 scripts/scan-filter.py <scan-results.json> [--show-known] [--include-candidates]

  <scan-results.json>  the file saved from streamers/youtube-scraper (either the raw Apify
                       dataset array, or the wrapper {"results": [...]} used in sources/raw/).
  --show-known         also print the items that were dropped, with their registry status.
  --include-candidates treat status "candidate" as still open (default: candidates are
                       reported separately, because they were parked on purpose for a module).

Output: a markdown table of NEW items (title, channel, subscribers, views, date, duration,
query) sorted by subscribers, plus counts. Nothing is written; the registry is updated by hand
(or by the agent) once the selection is made — see the playbook, step "Track".

Registry entry shape (add one per decided item):
  {"id": "<youtube id or episode url>", "url": "...", "title": "...", "channel": "...",
   "published": "YYYY-MM-DD", "status": "transcribed|digested|applied|candidate|discarded",
   "reason": "...", "module": "sNN", "scan": "sources/YYYY-MM-DD-market-scan-....md",
   "raw": "sources/raw/.../file.md" (when transcribed), "decided": "YYYY-MM-DD"}
"""
import json, re, sys, os

def vid(url):
    m = re.search(r'(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})', url or '')
    return m.group(1) if m else (url or '').strip()

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = sys.argv[1]
    show_known = '--show-known' in sys.argv
    inc_cand = '--include-candidates' in sys.argv
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg = json.load(open(os.path.join(root, 'sources', 'media-registry.json')))
    known = {e['id']: e for e in reg['items']}
    data = json.load(open(path))
    items = data['results'] if isinstance(data, dict) and 'results' in data else data
    new, dropped, cands, seen = [], [], [], set()
    for it in items:
        v = vid(it.get('url', ''))
        if v in seen: continue
        seen.add(v)
        e = known.get(v)
        if e is None: new.append(it)
        elif e['status'] == 'candidate' and not inc_cand: cands.append((it, e))
        elif e['status'] == 'candidate': new.append(it)
        else: dropped.append((it, e))
    new.sort(key=lambda i: -(i.get('numberOfSubscribers') or 0))
    print(f"# scan-filter: {len(items)} items in scan → {len(new)} NEW, {len(cands)} parked candidates, {len(dropped)} already decided\n")
    print("## New (never considered before)\n")
    print("| Title | Channel | Subs | Views | Date | Length | Query | URL |\n|---|---|---|---|---|---|---|---|")
    for i in new:
        print(f"| {i.get('title','').replace('|','/')} | {i.get('channelName','')} | {i.get('numberOfSubscribers','')} | {i.get('viewCount','')} | {(i.get('date') or '')[:10]} | {i.get('duration','')} | {i.get('input','')} | {i.get('url','')} |")
    if cands:
        print("\n## Parked candidates that surfaced again (decide now if this module is theirs)\n")
        for i, e in cands:
            print(f"- {e['title']} — parked for {e['module']} ({e['reason']})")
    if show_known and dropped:
        print("\n## Already decided (dropped)\n")
        for i, e in dropped:
            print(f"- [{e['status']}] {e['title']} — {e['reason']} ({e['scan']})")

if __name__ == '__main__':
    main()
