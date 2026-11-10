#!/usr/bin/env python3
"""Merge editorial copy, computed track stats, and photo credits into data/routes.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    editorial = json.loads((ROOT / "data" / "editorial.json").read_text())
    stats = {}
    photos = {}
    stats_path = ROOT / "data" / "track_stats.json"
    photos_path = ROOT / "data" / "photos.json"
    if stats_path.exists():
        stats = json.loads(stats_path.read_text())
    if photos_path.exists():
        photos = json.loads(photos_path.read_text())

    routes = []
    for ed in editorial["routes"]:
        route = dict(ed)
        slug = route["slug"]
        route["photos"] = photos.get(slug) or []
        st = stats.get(slug)
        official = route.get("statsMode") == "official"
        if st and not official:
            route["lengthKm"] = st["lengthKm"]
            cover = st.get("elevationCoverage") or 0
            route["ascentM"] = st["ascentM"] if cover >= 0.8 else None
            route["descentM"] = st["descentM"] if cover >= 0.8 else None
            route["minElevationM"] = st["minElevationM"] if cover >= 0.8 else None
            route["maxElevationM"] = st["maxElevationM"] if cover >= 0.8 else None
            route["gpx"] = st["gpx"]
            gaps = [g for g in st.get("gapsM") or [] if g >= 200]
            gap_txt = ""
            if gaps:
                shown = "、".join(str(int(g)) for g in gaps[:8])
                gap_txt = f" 轨迹分成多段，段与段之间有约 {shown} 米的缺口；这些缺口没有用直线连上，也不计入长度。"
            ids = "、".join(str(i) for i in st["relationIds"])
            route["lengthSource"] = (
                f"长度 {st['lengthKm']} km 由 OpenStreetMap 关系 {ids} 的全分辨率节点，"
                f"按 WGS84 大圆距离累加（地球半径 6371008.8 米），计算日 2026-11-10。"
                f"采样轨迹长 {st['sampledLengthKm']} km（约每 {st['sampleSpacingM']:.0f} 米一点）。"
                + gap_txt
            )
            if route["ascentM"] is None:
                route["ascentSource"] = "高程采样覆盖不足，累计爬升不采用估算值。"
            else:
                route["ascentSource"] = (
                    f"{st['ascentMethod']} 覆盖率 {cover:.0%}。"
                    f"3 点中值平滑后累计爬升 {st['ascentM']} 米、下降 {st['descentM']} 米；"
                    f"未平滑的正向高差合计 {st['ascentRawM']} 米。这是 DEM 估算，不是实测剖面。"
                    + gap_txt
                )
            shape = "环线或原路往返（起终点相距不足 400 米）" if st["loop"] else "单程（起终点不相接）"
            route["gpxNote"] = (
                f"GPX：gpx/{slug}.gpx。几何来自 OpenStreetMap 关系 {ids}，© OpenStreetMap contributors，ODbL 1.0。"
                f"点已按约 {st['sampleSpacingM']:.0f} 米抽稀，以便浏览和高程采样；长度仍按抽稀前的节点计算。"
                f"有 <ele> 的点来自 OpenTopoData 数据集 {st['elevationDataset']}。"
                f"本文件方向下，轨迹呈{shape}。"
                + gap_txt
            )
        elif st and official:
            route["gpx"] = st["gpx"]
            ids = "、".join(str(i) for i in st["relationIds"])
            route["gpxNote"] = (
                f"GPX：gpx/{slug}.gpx，只覆盖 OpenStreetMap 关系 {ids}，"
                f"抽稀后约 {st['lengthKm']} km，高程约 {st['minElevationM']}–{st['maxElevationM']} 米，"
                f"平滑后爬升 {st['ascentM']} 米（OpenTopoData {st['elevationDataset']}）。"
                "它不是下方“官方全程”所描述的整条路线。© OpenStreetMap contributors，ODbL。"
            )
            route.setdefault(
                "lengthSource",
                "长度栏采用官方文字记载（见路线说明），不用上面这段不完整 GPX 的长度。",
            )
        else:
            route["gpx"] = None
            route["gpxNote"] = "GPX 暂缺。没有找到能够代表整条路线的 OSM 关系或路径，本站不编造轨迹。"
            route.setdefault("lengthSource", "没有可用的 GPX。长度只在有官方文字记载时写入说明，不单列估算值。")
            route.setdefault("ascentSource", "没有可用的 GPX 高程采样。")
        routes.append(route)

    out = {
        "meta": editorial.get("meta") or {},
        "routes": routes,
    }
    dest = ROOT / "data" / "routes.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {dest} routes={len(routes)}")


if __name__ == "__main__":
    main()
