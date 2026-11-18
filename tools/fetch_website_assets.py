"""Re-download every website asset listed in website-assets.json from globalrhub.org.

Use it after a photo or logo changes on the website, or to restore a fresh clone.
    python3 tools/fetch_website_assets.py            # only files that are missing
    python3 tools/fetch_website_assets.py --force    # re-download everything
Derived files (halftones, crops, the campus still) are rebuilt with tools/make_halftones.py etc.
"""
import json, os, sys, urllib.request

force = "--force" in sys.argv
m = json.load(open(os.path.join(os.path.dirname(__file__), "..", "website-assets.json")))
root = os.path.join(os.path.dirname(__file__), "..")
ok = skipped = 0
for a in m["assets"]:
    dst = os.path.join(root, a["file"])
    if os.path.exists(dst) and not force:
        skipped += 1
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    req = urllib.request.Request(a["url"], headers={"User-Agent": "asset-fetch"})
    with urllib.request.urlopen(req, timeout=30) as r, open(dst, "wb") as f:
        f.write(r.read())
    ok += 1
    print("fetched", a["file"])
print(f"{ok} downloaded, {skipped} already present")
