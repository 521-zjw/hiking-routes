#!/usr/bin/env python3
"""Validate data/routes.json, GPX files, photo files, and the no-CDN rule."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "slug", "name", "nameZh", "continent", "country", "region", "gateway",
    "summary", "daysMin", "daysMax", "difficulty", "difficultyZh", "difficultyNote",
    "bestMonths", "bestSeasonNote", "permitRequired", "fees", "transport",
    "accommodation", "links", "gpxNote", "lengthSource", "ascentSource",
]
BANNED = (
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "unpkg.com",
    "jsdelivr.net",
    "cdnjs.cloudflare.com",
    "cdn.jsdelivr.net",
)


def main() -> int:
    errors = []
    data_path = ROOT / "data" / "routes.json"
    if not data_path.exists():
        print("missing data/routes.json")
        return 1
    data = json.loads(data_path.read_text())
    routes = data.get("routes") or []
    if len(routes) < 40:
        errors.append(f"need at least 40 routes, found {len(routes)}")
    us = [r for r in routes if r.get("continent") == "us"]
    eu = [r for r in routes if r.get("continent") == "eu"]
    if len(us) < 18 or len(eu) < 18:
        errors.append(f"continent split too uneven: US {len(us)} Europe {len(eu)}")
    slugs = set()
    gpx_n = photo_routes = 0
    for route in routes:
        slug = route.get("slug")
        if not slug or slug in slugs:
            errors.append(f"bad or duplicate slug {slug}")
            continue
        slugs.add(slug)
        for key in REQUIRED:
            if key not in route or route[key] in ("", None, [], {}):
                # ascentSource may be a sentence; empty not allowed. lists empty not allowed.
                errors.append(f"{slug}: missing {key}")
        if route.get("continent") not in ("us", "eu"):
            errors.append(f"{slug}: continent")
        if not isinstance(route.get("bestMonths"), list) or not route["bestMonths"]:
            errors.append(f"{slug}: bestMonths")
        if not isinstance(route.get("permitRequired"), bool):
            errors.append(f"{slug}: permitRequired bool")
        for fee in route.get("fees") or []:
            for k in ("item", "amount", "asOf", "sourceUrl"):
                if not fee.get(k):
                    errors.append(f"{slug}: fee missing {k}")
            if not str(fee.get("sourceUrl", "")).startswith("http"):
                errors.append(f"{slug}: fee sourceUrl")
        for link in route.get("links") or []:
            if not str(link.get("url", "")).startswith("http"):
                errors.append(f"{slug}: link url")
        if len(route.get("links") or []) < 1:
            errors.append(f"{slug}: no links")
        photos = route.get("photos") or []
        if len(photos) < 2 or len(photos) > 4:
            errors.append(f"{slug}: need 2–4 photos, found {len(photos)}")
        else:
            photo_routes += 1
        for photo in photos:
            for k in ("file", "author", "license", "sourceUrl"):
                if not photo.get(k):
                    errors.append(f"{slug}: photo missing {k}")
            path = ROOT / photo.get("file", "")
            if not path.exists():
                errors.append(f"{slug}: photo file missing {photo.get('file')}")
            if not str(photo.get("sourceUrl", "")).startswith("http"):
                errors.append(f"{slug}: photo source")
        gpx = route.get("gpx")
        note = route.get("gpxNote") or ""
        if gpx:
            gpx_n += 1
            path = ROOT / gpx
            if not path.exists():
                errors.append(f"{slug}: gpx missing {gpx}")
            else:
                text = path.read_text(errors="replace")
                if "<gpx" not in text or "<trkpt" not in text:
                    errors.append(f"{slug}: gpx not a track")
                if "OpenStreetMap" not in text:
                    errors.append(f"{slug}: gpx missing OSM attribution")
        else:
            if "GPX 暂缺" not in note:
                errors.append(f"{slug}: missing GPX must say GPX 暂缺")
    if not (ROOT / ".nojekyll").exists():
        errors.append("missing .nojekyll")
    for rel in ("index.html", "css/style.css", "js/app.js"):
        text = (ROOT / rel).read_text(errors="replace")
        for banned in BANNED:
            if banned in text:
                errors.append(f"{rel} references {banned}")
        if "http://" in text or "https://" in text:
            # allow only inside comments? The site files should not hotlink assets.
            # app.js has no remote URLs. css/html neither. Flag any https in the shell.
            if rel != "js/app.js":
                errors.append(f"{rel} contains an absolute URL")
    print(f"routes={len(routes)} US={len(us)} Europe={len(eu)} with_gpx={gpx_n} with_2to4_photos={photo_routes}")
    if errors:
        print(f"{len(errors)} errors")
        for err in errors[:80]:
            print(" -", err)
        return 1
    print("validation ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
