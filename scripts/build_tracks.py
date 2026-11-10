#!/usr/bin/env python3
"""Build GPX tracks from OpenStreetMap route relations and sample elevations.

Geometry: © OpenStreetMap contributors, ODbL 1.0.
Elevations: OpenTopoData public API (dataset recorded per route).

Usage:
  python3 scripts/build_tracks.py            # all routes
  python3 scripts/build_tracks.py slug ...   # subset
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache"
GPX_DIR = ROOT / "gpx"
STATS_DIR = CACHE / "stats"
OSM_CACHE = CACHE / "osm"

UA = "hiking-routes-guide/1.0 (educational static site; OSM ODbL; Beijing)"
OVERPASS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
]
EARTH_R = 6371008.8
SKIP_ROLES = {
    "alternative",
    "excursion",
    "side_path",
    "approach",
    "abandoned",
    "proposed",
    "shortcut",
    "construction",
}

# Conventional direction is chosen with start_hint when the drawn
# direction would otherwise follow OSM digitisation order.
ROUTES = [
    {"slug": "angels-landing", "continent": "us", "relations": [7387173], "start_hint": [37.259, -112.951]},
    {"slug": "zion-narrows", "continent": "us", "relations": [13331651], "start_hint": [37.384, -112.848]},
    {"slug": "half-dome", "continent": "us", "relations": [16315186], "start_hint": [37.732, -119.560], "prefer": "ascent"},
    {"slug": "mist-trail", "continent": "us", "relations": [6451906], "start_hint": [37.732, -119.558]},
    {"slug": "clouds-rest", "continent": "us", "relations": [16759394], "start_hint": [37.826, -119.468]},
    {"slug": "panorama-trail", "continent": "us", "relations": [6451907], "start_hint": [37.746, -119.533]},
    {"slug": "bright-angel", "continent": "us", "relations": [2836803], "start_hint": [36.057, -112.143]},
    {"slug": "south-kaibab", "continent": "us", "relations": [2836796], "start_hint": [36.053, -112.084]},
    {"slug": "rim-to-rim", "continent": "us", "relations": [2836789, 2836803], "start_hint": [36.217, -112.057]},
    {"slug": "john-muir-trail", "continent": "us", "relations": [1244828], "start_hint": [37.732, -119.558]},
    {"slug": "mount-whitney", "continent": "us", "relations": [3289187], "start_hint": [36.587, -118.240]},
    {"slug": "wonderland-trail", "continent": "us", "relations": [4111743], "start_hint": [46.786, -121.735]},
    {"slug": "enchantments", "continent": "us", "relations": [4829792], "start_hint": [47.544, -120.821]},
    {"slug": "kalalau", "continent": "us", "relations": [9146299], "start_hint": [22.219, -159.583]},
    {"slug": "franconia-ridge", "continent": "us", "relations": [7729143], "start_hint": [44.142, -71.681]},
    {"slug": "teton-crest", "continent": "us", "relations": [3895101], "start_hint": [43.657, -110.830]},
    {"slug": "longs-peak", "continent": "us", "relations": [6747615], "start_hint": [40.272, -105.557]},
    {"slug": "timberline-trail", "continent": "us", "relations": [7641482], "start_hint": [45.331, -121.711]},
    {"slug": "havasupai", "continent": "us", "relations": [8264386], "start_hint": [36.159, -112.712]},
    {"slug": "navajo-loop", "continent": "us", "relations": [7758461], "start_hint": [37.622, -112.167]},
    {"slug": "precipice-trail", "continent": "us", "relations": [9816832], "start_hint": [44.349, -68.188]},
    {"slug": "monitor-ridge", "continent": "us", "relations": [7006673], "start_hint": [46.146, -122.183]},
    {"slug": "tour-du-mont-blanc", "continent": "eu", "relations": [9678362], "start_hint": [45.791, 6.799]},
    {"slug": "walkers-haute-route", "continent": "eu", "relations": [3020521], "start_hint": [45.923, 6.869]},
    {"slug": "gr20", "continent": "eu", "relations": [12484370], "start_hint": [42.508, 8.855]},
    {"slug": "alta-via-1", "continent": "eu", "relations": [177743], "start_hint": [46.697, 12.085]},
    {"slug": "alta-via-2", "continent": "eu", "relations": [404914], "start_hint": [46.716, 11.656]},
    {"slug": "west-highland-way", "continent": "eu", "relations": [16287], "start_hint": [55.941, -4.314]},
    {"slug": "laugavegur", "continent": "eu", "relations": [1225037], "start_hint": [63.989, -19.061]},
    {"slug": "fimmvorduhals", "continent": "eu", "relations": [396940], "start_hint": [63.529, -19.513]},
    {"slug": "kungsleden", "continent": "eu", "relations": [1657661], "start_hint": [68.349, 18.831]},
    {"slug": "camino-frances", "continent": "eu", "relations": [2163573], "start_hint": [43.163, -1.238]},
    {"slug": "tour-monte-rosa", "continent": "eu", "relations": [10353523], "start_hint": [46.024, 7.749]},
    {"slug": "eiger-trail", "continent": "eu", "relations": [19465820], "start_hint": [46.574, 7.974]},
    {"slug": "trolltunga", "continent": "eu", "relations": [4270209], "start_hint": [60.123, 6.740]},
    {"slug": "preikestolen", "continent": "eu", "relations": [4270259], "start_hint": [58.987, 6.137]},
    {"slug": "llanberis-path", "continent": "eu", "relations": [4004181], "start_hint": [53.116, -4.128]},
    {"slug": "ben-nevis", "continent": "eu", "relations": [4004229], "start_hint": [56.812, -5.073]},
    {"slug": "besseggen", "continent": "eu", "relations": [1417687], "start_hint": [61.495, 8.682]},
    {"slug": "samaria-gorge", "continent": "eu", "relations": [9634834], "start_hint": [35.309, 23.962]},
    {"slug": "hadrians-wall", "continent": "eu", "relations": [38791], "start_hint": [54.988, -2.601]},
    {"slug": "pennine-way", "continent": "eu", "relations": [4080347], "start_hint": [53.351, -1.850]},
    {"slug": "coast-to-coast", "continent": "eu", "relations": [12145], "start_hint": [54.491, -3.591]},
    {"slug": "ruta-del-cares", "continent": "eu", "relations": [2687934], "start_hint": [43.257, -4.834]},
    {"slug": "gr221", "continent": "eu", "relations": [383060], "start_hint": [39.796, 2.796]},
    {"slug": "trilho-dos-pescadores", "continent": "eu", "relations": [20810829], "start_hint": [37.928, -8.807]},
    {"slug": "caminito-del-rey", "continent": "eu", "relations": [4678863], "start_hint": [36.916, -4.776]},
]


def hav(a, b) -> float:
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_R * math.atan2(math.sqrt(h), math.sqrt(max(0.0, 1 - h)))


def http_json(url, data=None, timeout=180, headers=None, retries=4):
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read()[:300]
            last = f"HTTP {exc.code} {body!r}"
            if exc.code in (400, 404):
                raise RuntimeError(last)
            wait = 3 + i * 4
            print(f"  retry {i+1} {url[:70]} {last} sleep {wait}s", flush=True)
            time.sleep(wait)
        except Exception as exc:  # noqa: BLE001
            last = exc
            wait = 3 + i * 4
            print(f"  retry {i+1} {url[:70]} {exc} sleep {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"failed {url}: {last}")


def overpass(query: str, cache_name: str):
    path = OSM_CACHE / f"{cache_name}.json"
    if path.exists() and path.stat().st_size > 50:
        return json.loads(path.read_text())
    OSM_CACHE.mkdir(parents=True, exist_ok=True)
    payload = query.encode("utf-8")
    last = None
    for i, ep in enumerate(OVERPASS * 2):
        try:
            req = urllib.request.Request(ep, data=payload, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=240) as resp:
                raw = resp.read()
            data = json.loads(raw.decode("utf-8"))
            if "elements" not in data:
                raise RuntimeError(data.get("remark") or "no elements")
            path.write_text(json.dumps(data))
            time.sleep(1.2)
            return data
        except Exception as exc:  # noqa: BLE001
            last = exc
            print(f"  overpass fail {ep} {exc}", flush=True)
            time.sleep(4 + i * 3)
    raise RuntimeError(f"overpass failed for {cache_name}: {last}")


def osm_relation(rid: int):
    path = OSM_CACHE / f"api_rel_{rid}.json"
    if path.exists():
        return json.loads(path.read_text())
    data = http_json(f"https://api.openstreetmap.org/api/0.6/relation/{rid}.json", timeout=60)
    path.write_text(json.dumps(data))
    time.sleep(0.4)
    return data


def fetch_relation_geom(rid: int):
    """Return the relation element with way member geometries when possible."""
    try:
        data = overpass(
            f"[out:json][timeout:180];relation({rid});out geom;",
            f"relgeom_{rid}",
        )
        el = data["elements"][0]
        members = el.get("members") or []
        way_members = [m for m in members if m.get("type") == "way"]
        missing = [m for m in way_members if not m.get("geometry")]
        if way_members and not missing:
            return el
        if not way_members:
            return el
    except Exception as exc:  # noqa: BLE001
        print(f"  full geom failed {rid}: {exc}", flush=True)
        el = None
    # Fallback: member order from OSM API, geometries in batches.
    api = osm_relation(rid)["elements"][0]
    way_ids = [m["ref"] for m in api["members"] if m["type"] == "way"]
    geom_by_id = {}
    for i in range(0, len(way_ids), 40):
        chunk = way_ids[i : i + 40]
        ids = ",".join(str(x) for x in chunk)
        data = overpass(
            f"[out:json][timeout:120];way(id:{ids});out geom;",
            f"ways_{rid}_{i}",
        )
        for way in data["elements"]:
            geom_by_id[way["id"]] = way.get("geometry") or []
    members = []
    for m in api["members"]:
        item = {"type": m["type"], "ref": m["ref"], "role": m.get("role") or ""}
        if m["type"] == "way":
            item["geometry"] = geom_by_id.get(m["ref"]) or []
        members.append(item)
    return {"id": rid, "tags": api.get("tags") or {}, "members": members}


def orient_pts(prev, pts, role: str):
    if len(pts) < 2:
        return pts
    role = (role or "").lower()
    forward = pts
    backward = list(reversed(pts))
    if prev is None:
        return backward if role == "backward" else forward
    gap_f = hav(prev, forward[0])
    gap_b = hav(prev, backward[0])
    if role == "forward" and gap_f <= gap_b + 30:
        return forward
    if role == "backward" and gap_b <= gap_f + 30:
        return backward
    return backward if gap_b < gap_f else forward


def append_pts(segments, pts, join_m=80):
    if len(pts) < 2:
        return
    if not segments:
        segments.append(pts)
        return
    prev = segments[-1][-1]
    gap = hav(prev, pts[0])
    if gap <= join_m:
        if gap < 8 and hav(prev, pts[0]) < 8:
            pts = pts[1:]
        segments[-1].extend(pts)
    else:
        segments.append(pts)


def reverse_segments(segments):
    out = []
    for seg in reversed(segments):
        out.append(list(reversed(seg)))
    return out


def end_point(segments):
    return segments[-1][-1] if segments else None


def start_point(segments):
    return segments[0][0] if segments else None


def sequential_chain(polylines, hint=None, max_gap=200):
    """Follow OSM member order, flipping each way so it meets the previous end."""
    lines = [list(p) for p in polylines if len(p) >= 2]
    if not lines:
        return []
    first = lines[0]
    if hint is not None and hav(hint, first[-1]) + 5 < hav(hint, first[0]):
        first = list(reversed(first))
    segments = [first]
    for line in lines[1:]:
        end = segments[-1][-1]
        if hav(end, line[-1]) + 5 < hav(end, line[0]):
            line = list(reversed(line))
        gap = hav(end, line[0])
        if gap <= max_gap:
            if gap < 12:
                line = line[1:]
            if line:
                segments[-1].extend(line)
        else:
            segments.append(line)
    return segments


def chain_gap_sum(segments) -> float:
    total = 0.0
    for left, right in zip(segments, segments[1:]):
        total += hav(left[-1], right[0])
    return total


def best_chain(polylines, hint=None):
    """Member order is authoritative when it connects. Greedy repair is only for unsorted relations."""
    lines = [list(p) for p in polylines if len(p) >= 2]
    if not lines:
        return []
    candidates = [
        sequential_chain(lines, hint),
        sequential_chain(list(reversed(lines)), hint),
        greedy_chain(lines, hint),
    ]
    def score(segs):
        return (chain_gap_sum(segs), len(segs), -length_m(segs))
    return min(candidates, key=score)


def greedy_chain(polylines, hint=None, max_gap=200):
    """Order unordered OSM ways by joining the nearest free endpoint.

    Member order in route relations is often reversed or unsorted. A gap
    larger than max_gap is left as a break instead of a straight invented line.
    """
    unused = [list(p) for p in polylines if len(p) >= 2]
    if not unused:
        return []
    if hint is not None:
        def endpoint_distance(line):
            return min(hav(hint, line[0]), hav(hint, line[-1]))
        start_i = min(range(len(unused)), key=lambda i: endpoint_distance(unused[i]))
    else:
        start_i = 0
    current = unused.pop(start_i)
    if hint is not None and hav(hint, current[-1]) + 5 < hav(hint, current[0]):
        current = list(reversed(current))
    segments = [current]
    while unused:
        end = segments[-1][-1]
        best_i, best_gap, best_rev = 0, 1e18, False
        for i, line in enumerate(unused):
            g0 = hav(end, line[0])
            g1 = hav(end, line[-1])
            if g0 < best_gap:
                best_i, best_gap, best_rev = i, g0, False
            if g1 < best_gap:
                best_i, best_gap, best_rev = i, g1, True
        line = unused.pop(best_i)
        if best_rev:
            line = list(reversed(line))
        if best_gap <= max_gap:
            if best_gap < 12:
                line = line[1:]
            if len(line) >= 1:
                segments[-1].extend(line)
        else:
            segments.append(line)
    return segments


def relation_segments(rid: int, seen: set, depth: int = 0, hint=None):
    if rid in seen:
        print(f"  skip cycle {rid}", flush=True)
        return []
    seen.add(rid)
    el = fetch_relation_geom(rid)
    chunks = []
    way_buf = []

    def flush_ways():
        nonlocal way_buf
        if way_buf:
            chunks.append(("ways", way_buf))
            way_buf = []

    for mem in el.get("members") or []:
        role = (mem.get("role") or "").strip().lower()
        if role in SKIP_ROLES or "alternative" in role:
            continue
        if mem.get("type") == "way":
            geom = mem.get("geometry") or []
            pts = [(p["lat"], p["lon"]) for p in geom if "lat" in p and "lon" in p]
            if len(pts) >= 2:
                way_buf.append(pts)
        elif mem.get("type") == "relation":
            flush_ways()
            chunks.append(("rel", mem["ref"]))
    flush_ways()

    segments = []
    local_hint = hint
    for kind, payload in chunks:
        if kind == "ways":
            chained = best_chain(payload, hint=local_hint or end_point(segments))
            block = chained
        else:
            block = relation_segments(payload, seen, depth + 1, hint=end_point(segments) or local_hint)
        if not block:
            continue
        prev = end_point(segments)
        if prev is not None:
            if hav(prev, end_point(block)) + 30 < hav(prev, start_point(block)):
                block = reverse_segments(block)
            gap = hav(prev, start_point(block))
            if gap <= 200:
                segments[-1].extend(block[0][1:] if gap < 12 else block[0])
                segments.extend(block[1:])
            else:
                segments.extend(block)
        else:
            segments.extend(block)
        local_hint = end_point(segments)
    cleaned = []
    for seg in segments:
        out = []
        for p in seg:
            if not out or hav(out[-1], p) > 1.5:
                out.append(p)
        if len(out) >= 2:
            cleaned.append(out)
    return repair_segments(cleaned)


def repair_segments(segments):
    """Join pieces that actually touch, and drop tiny disconnected fragments.

    A route relation sometimes repeats a short stub at the far end of the member
    list, or stores two halves that share an endpoint. Those are not missing trail.
    """
    segs = [list(s) for s in segments if len(s) >= 2]
    changed = True
    while changed and len(segs) > 1:
        changed = False
        best = None
        best_d = 250
        for i in range(len(segs)):
            for j in range(i + 1, len(segs)):
                a, b = segs[i], segs[j]
                options = [
                    (hav(a[-1], b[0]), "a-b", False),
                    (hav(a[-1], b[-1]), "a-rb", True),
                    (hav(b[-1], a[0]), "b-a", False),
                    (hav(b[0], a[0]), "rb-a", True),
                ]
                for dist, kind, _rev in options:
                    if dist < best_d:
                        best_d = dist
                        best = (i, j, kind, dist)
        if not best:
            break
        i, j, kind, dist = best
        a, b = segs[i], segs[j]
        la, lb = length_m([a]), length_m([b])
        short, long = (lb, la) if lb < la else (la, lb)
        if short < 500 and long > 2000 and dist < 250:
            # duplicate stub at a junction: keep the long piece
            drop = j if lb < la else i
            segs.pop(drop)
            changed = True
            continue
        if kind == "a-b":
            merged = a + (b[1:] if dist < 12 else b)
        elif kind == "a-rb":
            rb = list(reversed(b))
            merged = a + (rb[1:] if dist < 12 else rb)
        elif kind == "b-a":
            merged = b + (a[1:] if dist < 12 else a)
        else:
            # The two starts are the close ends: reverse A so it finishes there, then follow B.
            ra = list(reversed(a))
            merged = ra + (b[1:] if dist < 12 else b)
        keep_i, drop_i = (i, j) if i < j else (j, i)
        # replace the lower index with merged, delete the other
        first, second = min(i, j), max(i, j)
        segs[first] = merged
        segs.pop(second)
        changed = True
    if len(segs) > 1:
        lengths = [length_m([s]) for s in segs]
        longest = max(lengths)
        kept = []
        for seg, ln in zip(segs, lengths):
            if ln < 500 and longest > 2000:
                print(f"  drop disconnected fragment {ln:.0f} m", flush=True)
                continue
            kept.append(seg)
        segs = kept or segs
    return segs


def length_m(segments) -> float:
    total = 0.0
    for seg in segments:
        for a, b in zip(seg, seg[1:]):
            total += hav(a, b)
    return total


def gaps(segments):
    found = []
    for a, b in zip(segments, segments[1:]):
        found.append(round(hav(a[-1], b[0]), 1))
    return found


def resample(segments, spacing: float):
    """Resample each segment at about `spacing` metres. Returns list of segments."""
    out = []
    for seg in segments:
        if len(seg) < 2:
            continue
        cum = [0.0]
        for a, b in zip(seg, seg[1:]):
            cum.append(cum[-1] + hav(a, b))
        total = cum[-1]
        if total < 1:
            continue
        targets = [0.0]
        d = spacing
        while d < total:
            targets.append(d)
            d += spacing
        if total - targets[-1] > spacing * 0.3:
            targets.append(total)
        else:
            targets[-1] = total
        pts = []
        j = 0
        for target in targets:
            while j < len(cum) - 2 and cum[j + 1] < target:
                j += 1
            span = cum[j + 1] - cum[j]
            t = 0 if span <= 0 else (target - cum[j]) / span
            t = min(1, max(0, t))
            lat = seg[j][0] + (seg[j + 1][0] - seg[j][0]) * t
            lon = seg[j][1] + (seg[j + 1][1] - seg[j][1]) * t
            if not pts or hav(pts[-1], (lat, lon)) > 0.5:
                pts.append((lat, lon))
        if len(pts) >= 2:
            out.append(pts)
    return out


def choose_spacing(length: float) -> float:
    if length < 12000:
        return 40
    if length < 40000:
        return 80
    if length < 120000:
        return 140
    if length < 300000:
        return 220
    return 350


def datasets_for(continent: str, lat: float, lon: float):
    if continent == "us":
        if lon < -150 or lat < 30:
            return ["srtm30m", "aster30m", "mapzen"]
        return ["ned10m", "srtm30m", "aster30m"]
    if lat > 60 or lat < 35:
        return ["eudem25m", "aster30m", "mapzen"]
    return ["eudem25m", "srtm30m", "aster30m"]


def opentopo(dataset: str, points):
    loc = "|".join(f"{p[0]:.6f},{p[1]:.6f}" for p in points)
    body = json.dumps({"locations": loc}).encode()
    url = f"https://api.opentopodata.org/v1/{dataset}"
    data = http_json(
        url,
        data=body,
        timeout=90,
        headers={"Content-Type": "application/json", "User-Agent": UA},
        retries=4,
    )
    if data.get("status") != "OK":
        raise RuntimeError(str(data)[:200])
    return [r.get("elevation") for r in data.get("results") or []]


def sample_elevations(points, datasets):
    """Return (elevations, dataset_used). None where all datasets are void."""
    n = len(points)
    elev = [None] * n
    used = None
    unresolved = list(range(n))
    for dataset in datasets:
        if not unresolved:
            break
        still = []
        for i in range(0, len(unresolved), 90):
            idxs = unresolved[i : i + 90]
            pts = [points[k] for k in idxs]
            try:
                vals = opentopo(dataset, pts)
            except Exception as exc:  # noqa: BLE001
                print(f"  elevation error {dataset}: {exc}", flush=True)
                still.extend(idxs)
                time.sleep(2)
                continue
            if len(vals) != len(idxs):
                still.extend(idxs)
                continue
            got = 0
            for idx, val in zip(idxs, vals):
                if isinstance(val, (int, float)):
                    elev[idx] = float(val)
                    got += 1
                else:
                    still.append(idx)
            if got and used is None:
                used = dataset
            time.sleep(1.15)
        unresolved = still
        if unresolved:
            print(f"  {dataset} left {len(unresolved)} voids", flush=True)
    return elev, used or datasets[0]


def smooth_median(vals, window=3):
    out = list(vals)
    half = window // 2
    for i in range(len(vals)):
        chunk = [vals[j] for j in range(max(0, i - half), min(len(vals), i + half + 1)) if vals[j] is not None]
        if chunk and vals[i] is not None:
            chunk.sort()
            out[i] = chunk[len(chunk) // 2]
    return out


def ascent_descent(elev):
    """Compute ascent on contiguous runs. Returns ascent, descent, min, max, coverage."""
    known = [v for v in elev if isinstance(v, (int, float))]
    if not known:
        return None, None, None, None, 0.0
    asc = 0.0
    desc = 0.0
    prev = None
    for v in elev:
        if v is None:
            prev = None
            continue
        if prev is not None:
            d = v - prev
            if d > 0:
                asc += d
            elif d < 0:
                desc -= d
        prev = v
    return asc, desc, min(known), max(known), len(known) / len(elev)


def apply_start_hint(segments, hint):
    if not hint or not segments:
        return segments
    ds = hav(hint, start_point(segments))
    de = hav(hint, end_point(segments))
    if de + 200 < ds:
        return reverse_segments(segments)
    return segments


def write_gpx(path: Path, slug: str, segments, elev_by_index, meta_desc: str):
    def esc(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="hiking-routes-guide"',
        ' xmlns="http://www.topografix.com/GPX/1/1">',
        "  <metadata>",
        f"    <name>{esc(slug)}</name>",
        f"    <desc>{esc(meta_desc)}</desc>",
        '    <author><name>OpenStreetMap contributors</name></author>',
        '    <copyright author="OpenStreetMap contributors">ODbL-1.0</copyright>',
        '    <link href="https://www.openstreetmap.org/copyright"><text>© OpenStreetMap contributors, ODbL</text></link>',
        "  </metadata>",
        "  <trk>",
        f"    <name>{esc(slug)}</name>",
        "    <desc>© OpenStreetMap contributors, ODbL. Elevations where present are DEM samples, not a survey.</desc>",
    ]
    idx = 0
    for seg in segments:
        lines.append("    <trkseg>")
        for lat, lon in seg:
            ele = elev_by_index[idx] if idx < len(elev_by_index) else None
            idx += 1
            if isinstance(ele, float):
                lines.append(f'      <trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
            else:
                lines.append(f'      <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
        lines.append("    </trkseg>")
    lines += ["  </trk>", "</gpx>", ""]
    path.write_text("\n".join(lines))


def build_route(route):
    slug = route["slug"]
    print(f"\n=== {slug} relations {route['relations']}", flush=True)
    seen = set()
    segments = []
    hint = route.get("start_hint")
    for rid in route["relations"]:
        child = relation_segments(rid, seen, hint=hint if not segments else end_point(segments))
        if not child:
            print(f"  empty relation {rid}", flush=True)
            continue
        prev = end_point(segments)
        if prev is not None:
            if hav(prev, end_point(child)) + 40 < hav(prev, start_point(child)):
                child = reverse_segments(child)
            gap = hav(prev, start_point(child))
            if gap <= 200:
                segments[-1].extend(child[0])
                segments.extend(child[1:])
            else:
                segments.extend(child)
        else:
            segments.extend(child)
    if not segments:
        raise RuntimeError(f"no geometry for {slug}")
    segments = apply_start_hint(segments, route.get("start_hint"))
    full_len = length_m(segments)
    gap_list = gaps(segments)
    spacing = choose_spacing(full_len)
    sampled = resample(segments, spacing)
    flat = [p for seg in sampled for p in seg]
    print(
        f"  full {full_len/1000:.2f} km, segs {len(segments)}, gaps {gap_list[:6]}, "
        f"sampled {len(flat)} pts @ {spacing:.0f} m",
        flush=True,
    )
    lat = flat[0][0]
    lon = flat[0][1]
    datasets = datasets_for(route["continent"], lat, lon)
    ele_cache = CACHE / "ele" / f"{slug}.json"
    signature = [round(full_len), len(flat), round(flat[0][0], 4), round(flat[0][1], 4), round(flat[-1][0], 4), round(flat[-1][1], 4)]
    if ele_cache.exists():
        cached = json.loads(ele_cache.read_text())
        if cached.get("signature") == signature and cached.get("datasets") == datasets:
            elev = cached["elev"]
            dataset = cached["dataset"]
            print(f"  elevation cache {dataset}", flush=True)
        else:
            elev, dataset = sample_elevations(flat, datasets)
            ele_cache.parent.mkdir(parents=True, exist_ok=True)
            ele_cache.write_text(json.dumps({"signature": signature, "datasets": datasets, "dataset": dataset, "elev": elev}))
    else:
        elev, dataset = sample_elevations(flat, datasets)
        ele_cache.parent.mkdir(parents=True, exist_ok=True)
        ele_cache.write_text(json.dumps({"signature": signature, "datasets": datasets, "dataset": dataset, "elev": elev}))
    smoothed = smooth_median(elev, 3)
    asc, desc, emin, emax, cover = ascent_descent(smoothed)
    asc_raw, desc_raw, _, _, _ = ascent_descent(elev)
    if (
        route.get("prefer") == "ascent"
        and asc is not None
        and desc is not None
        and desc > asc + 30
    ):
        segments = reverse_segments(segments)
        sampled = reverse_segments(sampled)
        smoothed = list(reversed(smoothed))
        elev = list(reversed(elev))
        asc, desc = desc, asc
        asc_raw, desc_raw = desc_raw, asc_raw
        print("  reversed so the stored track climbs", flush=True)
    desc_text = (
        f"Geometry from OpenStreetMap relation(s) {', '.join(str(i) for i in route['relations'])}. "
        f"© OpenStreetMap contributors, ODbL 1.0. "
        f"Track resampled at about {spacing:.0f} m from the full relation geometry "
        f"(full-resolution length {full_len/1000:.2f} km; gaps between segments are not filled). "
        f"Elevations, where present, are samples from OpenTopoData dataset {dataset} "
        f"at those resampled points — not a ground survey. Points without <ele> are DEM voids."
    )
    GPX_DIR.mkdir(parents=True, exist_ok=True)
    write_gpx(GPX_DIR / f"{slug}.gpx", slug, sampled, smoothed, desc_text)
    stats = {
        "slug": slug,
        "relationIds": route["relations"],
        "lengthKm": round(full_len / 1000, 2),
        "sampledLengthKm": round(length_m(sampled) / 1000, 2),
        "ascentM": None if asc is None else round(asc),
        "descentM": None if desc is None else round(desc),
        "ascentRawM": None if asc_raw is None else round(asc_raw),
        "descentRawM": None if desc_raw is None else round(desc_raw),
        "minElevationM": None if emin is None else round(emin),
        "maxElevationM": None if emax is None else round(emax),
        "elevationDataset": dataset,
        "elevationDatasetsTried": datasets,
        "elevationCoverage": round(cover, 3),
        "sampleSpacingM": spacing,
        "sampleCount": len(flat),
        "segmentCount": len(sampled),
        "gapsM": gap_list,
        "start": [round(start_point(segments)[0], 5), round(start_point(segments)[1], 5)],
        "end": [round(end_point(segments)[0], 5), round(end_point(segments)[1], 5)],
        "loop": hav(start_point(segments), end_point(segments)) < 400,
        "gpx": f"gpx/{slug}.gpx",
        "lengthMethod": "Full-resolution OSM geometry, WGS84 haversine, Earth radius 6371008.8 m. Breaks between segments are not bridged and are not counted.",
        "ascentMethod": (
            f"OpenTopoData {dataset} at ~{spacing:.0f} m spacing along the track. "
            "Elevations are smoothed with a 3-point median. Ascent is the sum of positive differences on contiguous samples. "
            "Voids break the sum and are not interpolated."
        ),
    }
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    (STATS_DIR / f"{slug}.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(
        f"  -> {stats['lengthKm']} km  +{stats['ascentM']} m / -{stats['descentM']} m  "
        f"ele {stats['minElevationM']}–{stats['maxElevationM']} {dataset} cover {cover:.0%} loop {stats['loop']}",
        flush=True,
    )
    return stats


def main():
    for p in (CACHE, GPX_DIR, STATS_DIR, OSM_CACHE, CACHE / "ele"):
        p.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:]
    routes = [r for r in ROUTES if not wanted or r["slug"] in wanted]
    all_stats = {}
    merged_path = ROOT / "data" / "track_stats.json"
    if merged_path.exists():
        try:
            all_stats = json.loads(merged_path.read_text())
        except json.JSONDecodeError:
            all_stats = {}
    for route in routes:
        try:
            stats = build_route(route)
            all_stats[route["slug"]] = stats
            merged_path.parent.mkdir(parents=True, exist_ok=True)
            merged_path.write_text(json.dumps(all_stats, ensure_ascii=False, indent=2))
        except Exception as exc:  # noqa: BLE001
            print(f"FAILED {route['slug']}: {exc}", flush=True)
    print("\nDONE", len(all_stats), flush=True)


if __name__ == "__main__":
    main()
