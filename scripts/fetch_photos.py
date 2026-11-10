#!/usr/bin/env python3
"""Download 2–4 Wikimedia Commons photos per route and write attribution.

Images are stored in the repo (not hotlinked). Only permissive licenses
(public domain, CC0, CC BY, CC BY-SA) are accepted. NC and ND are rejected
because resizing is a derivative.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "photos"
UA = "hiking-routes-guide/1.0 (educational static site; photo attribution; Beijing)"

# (slug, search queries, filename keywords that must match at least one if set)
ROUTES = [
    ("angels-landing", ["Angels Landing Zion", "Angels Landing chains trail"], ["angel"]),
    ("zion-narrows", ["Zion Narrows Virgin River", "The Narrows Zion hike"], ["narrow"]),
    ("half-dome", ["Half Dome Yosemite cables", "Half Dome Yosemite trail"], ["half dome", "halfdome"]),
    ("mist-trail", ["Mist Trail Yosemite Vernal Fall", "Nevada Fall Mist Trail"], ["mist", "vernal", "nevada fall"]),
    ("clouds-rest", ["Clouds Rest Yosemite", "Clouds Rest trail Sierra"], ["cloud"]),
    ("panorama-trail", ["Panorama Trail Yosemite Glacier Point", "Glacier Point Yosemite panorama"], ["glacier point", "panorama", "yosemite"]),
    ("bright-angel", ["Bright Angel Trail Grand Canyon", "Bright Angel Grand Canyon switchbacks"], ["bright angel", "grand canyon"]),
    ("south-kaibab", ["South Kaibab Trail Grand Canyon", "Ooh Aah Point South Kaibab"], ["kaibab", "grand canyon"]),
    ("rim-to-rim", ["Grand Canyon Rim to Rim", "North Kaibab Trail Grand Canyon"], ["grand canyon", "kaibab"]),
    ("john-muir-trail", ["John Muir Trail Sierra", "John Muir Trail Evolution Valley"], ["muir", "sierra", "evolution"]),
    ("mount-whitney", ["Mount Whitney Trail", "Mount Whitney summit Alabama Hills view"], ["whitney"]),
    ("wonderland-trail", ["Wonderland Trail Mount Rainier", "Mount Rainier Wonderland Trail"], ["rainier", "wonderland"]),
    ("enchantments", ["Enchantments Alpine Lakes Washington", "Colchuck Lake Enchantments"], ["enchantment", "colchuck", "alpine lakes"]),
    ("kalalau", ["Kalalau Trail Na Pali", "Kalalau Beach Kauai"], ["kalalau", "na pali", "nāpali", "napali"]),
    ("franconia-ridge", ["Franconia Ridge New Hampshire", "Franconia Ridge Trail"], ["franconia"]),
    ("teton-crest", ["Teton Crest Trail", "Grand Teton Paintbrush Divide"], ["teton"]),
    ("longs-peak", ["Longs Peak Keyhole Route", "Longs Peak Rocky Mountain"], ["longs"]),
    ("timberline-trail", ["Timberline Trail Mount Hood", "Mount Hood Timberline Trail"], ["hood", "timberline"]),
    ("havasupai", ["Havasupai Havasu Falls", "Havasu Falls trail"], ["havasu"]),
    ("navajo-loop", ["Navajo Loop Bryce Canyon", "Bryce Canyon Navajo Loop switchbacks"], ["navajo", "bryce"]),
    ("precipice-trail", ["Precipice Trail Acadia", "Acadia Precipice Trail"], ["precipice", "acadia"]),
    ("monitor-ridge", ["Monitor Ridge Mount St Helens", "Mount St. Helens summit hike"], ["helens", "monitor ridge"]),
    ("tour-du-mont-blanc", ["Tour du Mont Blanc", "Tour du Mont Blanc refuge"], ["mont blanc", "mont-blanc", "chamonix", "tmb"]),
    ("walkers-haute-route", ["Walker Haute Route Chamonix Zermatt", "Haute Route hikers Alps"], ["haute", "zermatt", "chamonix"]),
    ("gr20", ["GR20 Corsica", "GR 20 Calenzana"], ["gr20", "gr 20", "corsica", "corse"]),
    ("alta-via-1", ["Alta Via 1 Dolomites", "Alta Via 1 Lago di Braies"], ["alta via", "dolomit"]),
    ("alta-via-2", ["Alta Via 2 Dolomites", "Alta Via 2 Dolomiti"], ["alta via", "dolomit"]),
    ("west-highland-way", ["West Highland Way Scotland", "West Highland Way Bridge of Orchy"], ["highland", "milngavie", "glencoe"]),
    ("laugavegur", ["Laugavegur trail Iceland", "Laugavegur Landmannalaugar"], ["laugavegur", "landmannalaugar"]),
    ("fimmvorduhals", ["Fimmvörðuháls hike", "Fimmvorduhals Skogar"], ["fimm", "skogar", "thorsmork", "þórsmörk"]),
    ("kungsleden", ["Kungsleden Abisko", "Kungsleden Sweden trail"], ["kungsleden", "abisko"]),
    ("camino-frances", ["Camino Frances Santiago", "Camino de Santiago French Way pilgrims"], ["camino", "santiago", "pilgrim"]),
    ("tour-monte-rosa", ["Tour Monte Rosa hike", "Monte Rosa hut trail"], ["monte rosa", "rosa"]),
    ("eiger-trail", ["Eiger Trail Grindelwald", "Eiger north face trail"], ["eiger"]),
    ("trolltunga", ["Trolltunga hike", "Trolltunga Norway"], ["trolltunga"]),
    ("preikestolen", ["Preikestolen hike", "Preikestolen Pulpit Rock"], ["preikestolen", "pulpit"]),
    ("llanberis-path", ["Llanberis Path Snowdon", "Yr Wyddfa Llanberis Path"], ["llanberis", "snowdon", "wyddfa"]),
    ("ben-nevis", ["Ben Nevis Mountain Track", "Ben Nevis tourist path"], ["ben nevis", "nevis"]),
    ("besseggen", ["Besseggen ridge hike", "Besseggen Gjende"], ["besseggen", "gjende"]),
    ("samaria-gorge", ["Samaria Gorge Crete hike", "Samaria Gorge trail"], ["samaria", "samariá"]),
    ("hadrians-wall", ["Hadrian's Wall Path", "Hadrian's Wall hiking"], ["hadrian"]),
    ("pennine-way", ["Pennine Way England", "Pennine Way Kinder Scout"], ["pennine"]),
    ("coast-to-coast", ["Coast to Coast Walk Wainwright", "Coast to Coast Walk Lake District"], ["coast to coast", "wainwright", "st bees"]),
    ("ruta-del-cares", ["Ruta del Cares", "Cares Gorge Picos de Europa"], ["cares"]),
    ("gr221", ["GR221 Mallorca", "Ruta de Pedra en Sec"], ["pedra", "gr 221", "gr221", "mallorca", "tramuntana"]),
    ("trilho-dos-pescadores", ["Trilho dos Pescadores Rota Vicentina", "Fishermen's Trail Alentejo"], ["pescador", "vicentina", "fishermen"]),
    ("caminito-del-rey", ["Caminito del Rey", "Caminito del Rey walkway"], ["caminito"]),
    ("highline-glacier", ["Highline Trail Glacier National Park", "Highline Trail Logan Pass"], ["highline", "logan pass", "glacier national"]),
    ("presidential-traverse", ["Presidential Traverse White Mountains", "Mount Washington Presidential Range"], ["presidential", "washington", "madison"]),
    ("delicate-arch", ["Delicate Arch Arches trail", "Delicate Arch Utah"], ["delicate arch"]),
    ("seceda", ["Seceda Dolomites ridge", "Seceda Val Gardena"], ["seceda", "secëda"]),
    ("cinque-terre", ["Sentiero Azzurro Cinque Terre", "Cinque Terre hiking trail Vernazza"], ["cinque terre", "vernazza", "monterosso", "manarola", "riomaggiore"]),
    ("tre-cime", ["Tre Cime di Lavaredo hike", "Drei Zinnen circuit trail"], ["tre cime", "drei zinnen", "lavaredo"]),
]

BAD_NAME = re.compile(
    r"map|logo|icon|diagram|locator|pictogram|svg|coat of arms|flag of|portrait|signature|bus stop|qr",
    re.I,
)


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = (
        text.replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )
    return re.sub(r"\s+", " ", text).strip()


def api(params: dict):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def license_ok(name: str) -> bool:
    n = (name or "").lower()
    if any(x in n for x in ["noncommercial", "non-commercial", "-nc", " nc", "noderiv", "no deriv", "-nd", " nd"]):
        return False
    return any(x in n for x in ["cc0", "cc-by", "cc by", "public domain", "pdm"])


def candidates_for(query: str):
    data = api(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": "6",
            "gsrlimit": "20",
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": "1600",
            "iiextmetadatafilter": "LicenseShortName|Artist|LicenseUrl|UsageTerms|ImageDescription",
        }
    )
    pages = (data.get("query") or {}).get("pages") or {}
    found = []
    for page in pages.values():
        info = (page.get("imageinfo") or [None])[0]
        if not info:
            continue
        meta = info.get("extmetadata") or {}
        lic = strip_html((meta.get("LicenseShortName") or {}).get("value", ""))
        if not license_ok(lic):
            continue
        mime = info.get("mime") or ""
        if not mime.startswith("image/") or "svg" in mime:
            continue
        title = page.get("title") or ""
        if BAD_NAME.search(title):
            continue
        width = info.get("thumbwidth") or info.get("width") or 0
        if (info.get("width") or 0) < 900:
            continue
        url = info.get("thumburl") or info.get("url")
        if not url:
            continue
        artist = strip_html((meta.get("Artist") or {}).get("value", "")) or "未知作者"
        lic_url = strip_html((meta.get("LicenseUrl") or {}).get("value", ""))
        desc = strip_html((meta.get("ImageDescription") or {}).get("value", ""))
        file_name = title.replace("File:", "")
        source = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
        found.append(
            {
                "title": file_name,
                "page": title,
                "url": url,
                "author": artist[:180],
                "license": lic,
                "licenseUrl": lic_url,
                "description": desc[:240],
                "sourceUrl": source,
                "width": width,
            }
        )
    return found


def save_image(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    im = Image.open(BytesIO(raw))
    im = im.convert("RGB")
    im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=78, optimize=True, progressive=True)


def score(item, keywords):
    blob = (item["title"] + " " + item["description"]).lower()
    s = 0
    for kw in keywords:
        if kw.lower() in blob:
            s += 5
    s += min(item["width"], 2000) / 1000
    return s


def main():
    manifest = {}
    for slug, queries, keywords in ROUTES:
        print(f"\n== {slug}", flush=True)
        pool = []
        seen = set()
        for q in queries:
            try:
                rows = candidates_for(q)
            except Exception as exc:  # noqa: BLE001
                print("  search fail", exc, flush=True)
                time.sleep(1)
                continue
            for row in rows:
                if row["page"] in seen:
                    continue
                seen.add(row["page"])
                row["score"] = score(row, keywords)
                pool.append(row)
            time.sleep(0.4)
        pool.sort(key=lambda r: r["score"], reverse=True)
        # Prefer keyword hits; fall back to anything licensed if we are short.
        picked = [r for r in pool if r["score"] >= 5][:4]
        if len(picked) < 2:
            for r in pool:
                if r not in picked:
                    picked.append(r)
                if len(picked) >= 3:
                    break
        photos = []
        for i, row in enumerate(picked[:4], start=1):
            dest = OUT / slug / f"{i:02d}.jpg"
            try:
                save_image(row["url"], dest)
            except Exception as exc:  # noqa: BLE001
                print("  download fail", row["title"], exc, flush=True)
                continue
            rel = f"photos/{slug}/{i:02d}.jpg"
            photos.append(
                {
                    "file": rel,
                    "title": row["title"],
                    "author": row["author"],
                    "license": row["license"],
                    "licenseUrl": row["licenseUrl"],
                    "sourceUrl": row["sourceUrl"],
                    "description": row["description"],
                }
            )
            print(f"  {rel} {row['license']} {row['title'][:70]}", flush=True)
            time.sleep(0.3)
        manifest[slug] = photos
        (ROOT / "data").mkdir(exist_ok=True)
        (ROOT / "data" / "photos.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print("photos done", flush=True)


if __name__ == "__main__":
    main()
