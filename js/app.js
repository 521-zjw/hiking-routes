/* 山径手册 — 本地脚本，无外部依赖。 */
(function () {
  const MONTHS = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"];
  const DIFF = { easy: "轻松", moderate: "中等", hard: "困难", strenuous: "艰辛" };
  const DIFF_RANK = { easy: 1, moderate: 2, hard: 3, strenuous: 4 };

  const els = {
    list: document.getElementById("list"),
    detail: document.getElementById("detail"),
    count: document.getElementById("count"),
    q: document.getElementById("q"),
    continent: document.getElementById("f-continent"),
    country: document.getElementById("f-country"),
    length: document.getElementById("f-length"),
    ascent: document.getElementById("f-ascent"),
    days: document.getElementById("f-days"),
    difficulty: document.getElementById("f-difficulty"),
    month: document.getElementById("f-month"),
    permit: document.getElementById("f-permit"),
    sort: document.getElementById("f-sort"),
  };

  let routes = [];
  MONTHS.forEach((name, i) => {
    const opt = document.createElement("option");
    opt.value = String(i + 1);
    opt.textContent = name;
    els.month.appendChild(opt);
  });

  function fmt(n, unit) {
    if (n === null || n === undefined || Number.isNaN(n)) return "暂无";
    return String(n) + (unit || "");
  }

  function countriesOf(route) {
    return route.countries && route.countries.length ? route.countries : [route.country];
  }

  function matches(route) {
    const q = els.q.value.trim().toLowerCase();
    if (q) {
      const blob = [route.name, route.nameZh, route.region, route.park, route.gateway, route.summary, route.country]
        .join(" ").toLowerCase();
      if (!blob.includes(q)) return false;
    }
    if (els.continent.value && route.continent !== els.continent.value) return false;
    if (els.country.value && !countriesOf(route).includes(els.country.value)) return false;
    const len = route.lengthKm;
    if (els.length.value === "s" && !(len < 20)) return false;
    if (els.length.value === "m" && !(len >= 20 && len < 80)) return false;
    if (els.length.value === "l" && !(len >= 80 && len < 200)) return false;
    if (els.length.value === "xl" && !(len >= 200)) return false;
    const asc = route.ascentM;
    if (els.ascent.value === "na" && asc !== null && asc !== undefined) return false;
    if (els.ascent.value === "s" && !(asc < 800)) return false;
    if (els.ascent.value === "m" && !(asc >= 800 && asc < 2000)) return false;
    if (els.ascent.value === "l" && !(asc >= 2000)) return false;
    const d = route.daysMax || route.daysMin;
    if (els.days.value === "1" && !(route.daysMax <= 1)) return false;
    if (els.days.value === "2" && !(route.daysMin <= 4 && route.daysMax >= 2)) return false;
    if (els.days.value === "5" && !(route.daysMin <= 9 && route.daysMax >= 5)) return false;
    if (els.days.value === "10" && !(d >= 10)) return false;
    if (els.difficulty.value && route.difficulty !== els.difficulty.value) return false;
    if (els.month.value && !(route.bestMonths || []).includes(Number(els.month.value))) return false;
    if (els.permit.value === "yes" && !route.permitRequired) return false;
    if (els.permit.value === "no" && route.permitRequired) return false;
    return true;
  }

  function sortRoutes(list) {
    const key = els.sort.value;
    const copy = list.slice();
    copy.sort((a, b) => {
      if (key === "length") return (a.lengthKm ?? 1e12) - (b.lengthKm ?? 1e12);
      if (key === "ascent") return (a.ascentM ?? 1e12) - (b.ascentM ?? 1e12);
      if (key === "days") return (a.daysMin ?? 99) - (b.daysMin ?? 99);
      if (key === "difficulty") return (DIFF_RANK[a.difficulty] || 9) - (DIFF_RANK[b.difficulty] || 9);
      if (key === "elev") return (a.maxElevationM ?? -1) - (b.maxElevationM ?? -1);
      return (a.nameZh || a.name).localeCompare(b.nameZh || b.name, "zh");
    });
    return copy;
  }

  function card(route) {
    const a = document.createElement("a");
    a.className = "card";
    a.href = "#/" + route.slug;
    const photo = (route.photos || [])[0];
    if (photo) {
      const img = document.createElement("img");
      img.className = "card-photo";
      img.src = photo.file;
      img.alt = photo.title || route.nameZh;
      a.appendChild(img);
    } else {
      const ph = document.createElement("div");
      ph.className = "placeholder";
      ph.textContent = "暂无照片";
      a.appendChild(ph);
    }
    const body = document.createElement("div");
    body.className = "card-body";
    body.innerHTML =
      `<p class="kicker">${escapeHtml(countriesOf(route).join(" · "))} · ${escapeHtml(route.region || "")}</p>` +
      `<h2>${escapeHtml(route.nameZh)}</h2>` +
      `<p class="orig">${escapeHtml(route.name)}</p>`;
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.appendChild(chip(route.lengthDisplay || fmt(route.lengthKm, " km")));
    meta.appendChild(chip(route.ascentDisplay || (route.ascentM == null ? "爬升暂无" : "↑ " + route.ascentM + " m")));
    const days = route.daysMin === route.daysMax ? route.daysMin + " 天" : route.daysMin + "–" + route.daysMax + " 天";
    meta.appendChild(chip(days));
    meta.appendChild(chip(route.difficultyZh || DIFF[route.difficulty] || ""));
    if (route.permitRequired) meta.appendChild(chip("需许可", true));
    if (!route.gpx) meta.appendChild(chip("GPX 暂缺", true));
    body.appendChild(meta);
    a.appendChild(body);
    return a;
  }

  function chip(text, warn) {
    const s = document.createElement("span");
    s.className = "chip" + (warn ? " warn" : "");
    s.textContent = text;
    return s;
  }

  function renderList() {
    const shown = sortRoutes(routes.filter(matches));
    els.list.hidden = false;
    els.detail.hidden = true;
    els.list.replaceChildren();
    if (!shown.length) {
      const p = document.createElement("p");
      p.className = "empty";
      p.textContent = "没有符合条件的路线。放宽筛选，或换个关键词。";
      els.list.appendChild(p);
    } else {
      shown.forEach((r) => els.list.appendChild(card(r)));
    }
    els.count.textContent = shown.length + " / " + routes.length + " 条";
  }

  function escapeHtml(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function renderDetail(route) {
    els.list.hidden = true;
    els.detail.hidden = false;
    window.scrollTo(0, 0);
    const days = route.daysMin === route.daysMax ? route.daysMin + " 天" : route.daysMin + "–" + route.daysMax + " 天";
    const months = (route.bestMonths || []).map((m) => MONTHS[m - 1]).join("、") || "资料不足";
    const fees = (route.fees || []).map((f) => `
      <tr>
        <td>${escapeHtml(f.item)}</td>
        <td>${escapeHtml(f.amount)}</td>
        <td>${escapeHtml(f.asOf || "")}</td>
        <td><a href="${escapeHtml(f.sourceUrl)}" rel="noopener">${escapeHtml(f.sourceName || "来源")}</a>${f.note ? "<div class='note'>" + escapeHtml(f.note) + "</div>" : ""}</td>
      </tr>`).join("");
    const links = (route.links || []).map((l) =>
      `<li><a href="${escapeHtml(l.url)}" rel="noopener">${escapeHtml(l.label)}</a></li>`).join("");
    const photos = (route.photos || []).map((p) => `
      <figure>
        <img src="${escapeHtml(p.file)}" alt="${escapeHtml(p.title || route.name)}">
        <figcaption>
          ${escapeHtml(p.title || "")}<br>
          作者：${escapeHtml(p.author || "未知")} ·
          许可：${p.licenseUrl ? `<a href="${escapeHtml(p.licenseUrl)}" rel="noopener">${escapeHtml(p.license)}</a>` : escapeHtml(p.license || "")}
          · <a href="${escapeHtml(p.sourceUrl)}" rel="noopener">维基共享资源原文件</a>
        </figcaption>
      </figure>`).join("");
    const gpxBtn = route.gpx
      ? `<a class="gpx-btn" href="${escapeHtml(route.gpx)}" download>下载 GPX</a>`
      : `<span class="gpx-btn" aria-disabled="true">GPX 暂缺</span>`;

    els.detail.innerHTML = `
      <div class="detail-top">
        <button class="back" type="button" id="back">返回列表</button>
      </div>
      <p class="kicker">${escapeHtml(countriesOf(route).join(" · "))} · ${escapeHtml(route.region || "")}</p>
      <h2>${escapeHtml(route.nameZh)}</h2>
      <p class="sub">${escapeHtml(route.name)}${route.park ? " · " + escapeHtml(route.park) : ""}</p>
      <p class="summary">${escapeHtml(route.summary || "")}</p>
      <div class="statgrid">
        <div class="stat"><b>${escapeHtml(route.lengthDisplay || fmt(route.lengthKm, " km"))}</b><span>长度</span></div>
        <div class="stat"><b>${escapeHtml(route.ascentDisplay || fmt(route.ascentM, " m"))}</b><span>累计爬升</span></div>
        <div class="stat"><b>${fmt(route.maxElevationM, " m")}</b><span>最高海拔</span></div>
        <div class="stat"><b>${fmt(route.minElevationM, " m")}</b><span>最低海拔</span></div>
        <div class="stat"><b>${escapeHtml(days)}</b><span>参考天数</span></div>
        <div class="stat"><b>${escapeHtml(route.difficultyZh || "")}</b><span>难度</span></div>
      </div>
      <div class="prose">
        <p class="note">${escapeHtml(route.lengthSource || "")}</p>
        <p class="note">${escapeHtml(route.ascentSource || "")}</p>
        ${route.hoursNote ? `<p>${escapeHtml(route.hoursNote)}</p>` : ""}
        ${route.officialNote ? `<p>${escapeHtml(route.officialNote)}</p>` : ""}
        <h3>季节</h3>
        <p>较适宜的月份：${escapeHtml(months)}。${escapeHtml(route.bestSeasonNote || "")}</p>
        <h3>难度说明</h3>
        <p>${escapeHtml(route.difficultyNote || "")}</p>
        <h3>费用与许可</h3>
        <p>${route.permitRequired ? "这条路线在通常走法下需要许可、抽签或预约。" : "通常不必为走路本身单独申请许可；门票、交通或山屋仍可能另收费。"}</p>
        <div class="fees-wrap"><table class="fees">
          <thead><tr><th>项目</th><th>金额</th><th>查阅日期</th><th>来源</th></tr></thead>
          <tbody>${fees || "<tr><td colspan='4'>暂无已核对的费用条目。</td></tr>"}</tbody>
        </table></div>
        <h3>交通</h3>
        <p>${escapeHtml(route.transport || "")}</p>
        <h3>住宿</h3>
        <p>${escapeHtml(route.accommodation || "")}</p>
        <h3>轨迹与高程</h3>
        <p>${escapeHtml(route.gpxNote || (route.gpx ? "" : "GPX 暂缺"))}</p>
        ${gpxBtn}
        <div class="layout-2" style="margin-top:0.8rem">
          <div class="panel">
            <h3>路线示意</h3>
            <div id="map"></div>
            <p class="note">平面示意，不是导航地图，不加载在线瓦片。© OpenStreetMap contributors，ODbL。</p>
          </div>
          <div class="panel">
            <h3>高程剖面</h3>
            <div id="profile"></div>
            <p class="note" id="profile-note"></p>
          </div>
        </div>
        <h3>照片</h3>
        <div class="photos">${photos || "<p>暂无已入库的可自由使用照片。</p>"}</div>
        <h3>官方与参考链接</h3>
        <ul class="link-list">${links}</ul>
      </div>`;
    document.getElementById("back").addEventListener("click", () => { location.hash = ""; });
    if (route.gpx) loadTrack(route.gpx);
    else {
      document.getElementById("map").textContent = "GPX 暂缺，无法绘制轨迹。";
      document.getElementById("profile").textContent = "GPX 暂缺，无法绘制高程。";
    }
  }

  function loadTrack(url) {
    fetch(url).then((r) => r.text()).then((xml) => {
      const doc = new DOMParser().parseFromString(xml, "application/xml");
      const segs = Array.from(doc.getElementsByTagName("trkseg")).map((seg) =>
        Array.from(seg.getElementsByTagName("trkpt")).map((pt) => ({
          lat: Number(pt.getAttribute("lat")),
          lon: Number(pt.getAttribute("lon")),
          ele: pt.getElementsByTagName("ele")[0] ? Number(pt.getElementsByTagName("ele")[0].textContent) : null,
        }))
      ).filter((s) => s.length > 1);
      drawMap(segs);
      drawProfile(segs);
    }).catch(() => {
      document.getElementById("map").textContent = "轨迹文件没有载入。";
      document.getElementById("profile").textContent = "轨迹文件没有载入。";
    });
  }

  function drawMap(segs) {
    const host = document.getElementById("map");
    const pts = segs.flat();
    if (!pts.length) { host.textContent = "轨迹为空。"; return; }
    const lats = pts.map((p) => p.lat);
    const lons = pts.map((p) => p.lon);
    const minLat = Math.min(...lats), maxLat = Math.max(...lats);
    const minLon = Math.min(...lons), maxLon = Math.max(...lons);
    const pad = 28;
    const W = 640, H = 420;
    const dx = Math.max(1e-6, maxLon - minLon);
    const dy = Math.max(1e-6, maxLat - minLat);
    const scale = Math.min((W - pad * 2) / dx, (H - pad * 2) / dy);
    const xOf = (lon) => pad + (lon - minLon) * scale + ((W - pad * 2) - dx * scale) / 2;
    const yOf = (lat) => H - pad - (lat - minLat) * scale - ((H - pad * 2) - dy * scale) / 2;
    const paths = segs.map((seg) => {
      const d = seg.map((p, i) => `${i ? "L" : "M"}${xOf(p.lon).toFixed(1)} ${yOf(p.lat).toFixed(1)}`).join(" ");
      return `<path d="${d}" fill="none" stroke="#1d3c34" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>`;
    }).join("");
    const a = segs[0][0];
    const b = segs[segs.length - 1][segs[segs.length - 1].length - 1];
    host.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="路线平面示意">
      <rect width="${W}" height="${H}" fill="#f7f3ea"/>
      ${paths}
      <circle cx="${xOf(a.lon)}" cy="${yOf(a.lat)}" r="5" fill="#2f6a4f"/>
      <rect x="${xOf(b.lon) - 4}" y="${yOf(b.lat) - 4}" width="8" height="8" fill="#a33b24"/>
      <text x="12" y="22" font-size="13" fill="#4a433a">绿点起点 · 红点终点 · 上为北</text>
    </svg>`;
  }

  function drawProfile(segs) {
    const host = document.getElementById("profile");
    const note = document.getElementById("profile-note");
    const pts = [];
    let dist = 0;
    segs.forEach((seg, si) => {
      seg.forEach((p, i) => {
        if (i > 0) dist += haversine(seg[i - 1], p);
        else if (si > 0) dist += haversine(segs[si - 1][segs[si - 1].length - 1], p);
        if (p.ele != null && !Number.isNaN(p.ele)) pts.push({ d: dist / 1000, ele: p.ele });
      });
    });
    if (pts.length < 2) {
      host.textContent = "这条 GPX 没有可用的高程采样。";
      note.textContent = "";
      return;
    }
    const W = 640, H = 420, padL = 48, padR = 12, padT = 16, padB = 32;
    const minE = Math.min(...pts.map((p) => p.ele));
    const maxE = Math.max(...pts.map((p) => p.ele));
    const maxD = pts[pts.length - 1].d;
    const spanE = Math.max(10, maxE - minE);
    const xOf = (d) => padL + (d / Math.max(maxD, 0.01)) * (W - padL - padR);
    const yOf = (e) => padT + (1 - (e - minE) / spanE) * (H - padT - padB);
    const line = pts.map((p, i) => `${i ? "L" : "M"}${xOf(p.d).toFixed(1)} ${yOf(p.ele).toFixed(1)}`).join(" ");
    const area = `${line} L${xOf(maxD).toFixed(1)} ${yOf(minE).toFixed(1)} L${xOf(0).toFixed(1)} ${yOf(minE).toFixed(1)} Z`;
    host.innerHTML = `<svg viewBox="0 0 ${W} ${H}" id="profile-svg" role="img" aria-label="高程剖面">
      <rect width="${W}" height="${H}" fill="#f7f3ea"/>
      <path d="${area}" fill="rgba(47,106,79,0.18)"/>
      <path d="${line}" fill="none" stroke="#a33b24" stroke-width="2"/>
      <text x="${padL}" y="${H - 8}" font-size="12" fill="#4a433a">0 km</text>
      <text x="${W - padR}" y="${H - 8}" font-size="12" fill="#4a433a" text-anchor="end">${maxD.toFixed(1)} km</text>
      <text x="8" y="${yOf(maxE) + 4}" font-size="12" fill="#4a433a">${Math.round(maxE)}</text>
      <text x="8" y="${yOf(minE)}" font-size="12" fill="#4a433a">${Math.round(minE)}</text>
      <line id="cursor" x1="0" x2="0" y1="${padT}" y2="${H - padB}" stroke="#1d3c34" stroke-dasharray="3 3" visibility="hidden"/>
    </svg>`;
    note.textContent = `剖面使用 GPX 中的高程点（约 ${Math.round(minE)}–${Math.round(maxE)} m）。横轴是采样点之间的地面距离，轨迹若有间断，距离仍按点序累加，不代表缺口被补成路。`;
    const svg = document.getElementById("profile-svg");
    const cursor = document.getElementById("cursor");
    function move(ev) {
      const rect = svg.getBoundingClientRect();
      const px = (ev.clientX - rect.left) / rect.width * W;
      let best = pts[0], bestDx = 1e9;
      pts.forEach((p) => {
        const dx = Math.abs(xOf(p.d) - px);
        if (dx < bestDx) { best = p; bestDx = dx; }
      });
      cursor.setAttribute("x1", xOf(best.d));
      cursor.setAttribute("x2", xOf(best.d));
      cursor.setAttribute("visibility", "visible");
      note.textContent = `${best.d.toFixed(1)} km 处约 ${Math.round(best.ele)} m（DEM 采样，不是实测点）。`;
    }
    svg.addEventListener("pointermove", move);
  }

  function haversine(a, b) {
    const R = 6371008.8;
    const p1 = a.lat * Math.PI / 180, p2 = b.lat * Math.PI / 180;
    const dlat = (b.lat - a.lat) * Math.PI / 180;
    const dlon = (b.lon - a.lon) * Math.PI / 180;
    const h = Math.sin(dlat / 2) ** 2 + Math.cos(p1) * Math.cos(p2) * Math.sin(dlon / 2) ** 2;
    return 2 * R * Math.atan2(Math.sqrt(h), Math.sqrt(Math.max(0, 1 - h)));
  }

  function routeFromHash() {
    const slug = decodeURIComponent((location.hash || "").replace(/^#\/?/, ""));
    return routes.find((r) => r.slug === slug);
  }

  function onHash() {
    const route = routeFromHash();
    if (route) renderDetail(route);
    else renderList();
  }

  ["input", "change"].forEach((ev) => {
    [els.q, els.continent, els.country, els.length, els.ascent, els.days, els.difficulty, els.month, els.permit, els.sort]
      .forEach((el) => el.addEventListener(ev, () => { if (!routeFromHash()) renderList(); }));
  });
  window.addEventListener("hashchange", onHash);

  fetch("data/routes.json")
    .then((r) => r.json())
    .then((data) => {
      routes = data.routes || [];
      const countries = new Set();
      routes.forEach((r) => countriesOf(r).forEach((c) => countries.add(c)));
      Array.from(countries).sort((a, b) => a.localeCompare(b, "zh")).forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        els.country.appendChild(opt);
      });
      onHash();
    })
    .catch(() => {
      els.list.innerHTML = "<p class='empty'>没有读到 data/routes.json。</p>";
    });
})();
