# 山径手册

Junwei Zhang（北京）整理的静态网站：美国和欧洲的经典徒步路线。用浏览器打开 `index.html`，或放到 GitHub Pages（`main` 分支根目录）。

页面上的脚本和样式都在仓库里，不引用 Google Fonts、unpkg、jsDelivr。在中国访问时，不依赖那些经常被墙的 CDN。

## 数据从哪来

- **路线几何**：OpenStreetMap 的 `route=hiking` 关系，经 Overpass API 取出。许可是 **ODbL**。© OpenStreetMap contributors。见每条 GPX 文件头，以及页面上的说明。
- **长度**：用关系里的全部节点，按 WGS84 大圆距离累加（地球半径 6,371,008.8 米）。关系成员如果顺序是乱的，会按端点重新接起来；接不上的缺口（大约 200 米以上）**不会用直线补上**，也不算进长度。
- **爬升和海拔**：把抽稀后的点送到 [OpenTopoData](https://www.opentopodata.org/) 采样。美国本土用 `ned10m`，夏威夷用 `srtm30m`，欧洲优先 `eudem25m`，覆盖不到再换数据集。高程做 3 点中值平滑后，把上升量加总。这是 DEM 估算，不是测绘队的剖面。
- **费用和许可**：只写查阅当天能在官方页面上对上的数字，并注明日期和链接。页面没写单价的，就写“没有核对到”，不编一个数。
- **照片**：维基共享资源上的公有领域、CC0、CC BY、CC BY-SA。按比例缩小到最长边 1600 像素以内，存进 `photos/`。署名和许可写在图片下面。NC、ND 的照片没有用，因为缩小也算演绎。

有的路线找不到一整条可靠的 OSM 关系（例如冰川国家公园的高线步道、总统山脉纵贯、精致拱门、塞切达、五渔村蓝色步道、三峰环线）。这些条目标成 **GPX 暂缺**，没有伪造轨迹。半圆顶的 GPX 只覆盖 OSM 里同名的山顶那一段，页面上的里程用的是美国国家公园管理局写的全程。

## 怎样在 GitHub Pages 上打开

仓库所有者到 GitHub：Settings → Pages → Build and deployment → Deploy from a branch → 选 `main`、`/ (root)`，保存。

根目录有 `.nojekyll`，避免 Jekyll 丢掉下划线开头的文件或按自己的规则处理站点。

如果 Pages API 返回 403，就只能在网页里手动打开上面的开关。打开之后地址一般是 `https://<用户名>.github.io/hiking-routes/`。

## 怎样再加一条路线

1. 在 `scripts/make_editorial.py`（美国）或 `scripts/make_editorial_eu.py`（欧洲）里加一条。必填：原名、中文名、国家、地区、门口城镇、简介、天数、难度、适宜月份、是否要许可、费用（含查阅日期和官方链接）、交通、住宿、至少一个链接。不知道的数字留空，并在说明里写原因。
2. 如果 OpenStreetMap 有路线关系，把关系号写进 `scripts/build_tracks.py` 的 `ROUTES`，然后运行：

   ```bash
   python3 scripts/build_tracks.py 你的-slug
   ```

   几何缓存在 `cache/`（不提交）。高程来自 OpenTopoData，请控制请求频率。
3. 在 `scripts/fetch_photos.py` 里加维基共享资源的搜索词，运行脚本。确认照片真是这条路线，再看作者和许可。
4. 重新生成文案和站点数据：

   ```bash
   python3 scripts/make_editorial.py
   python3 scripts/merge_routes.py
   python3 scripts/validate.py
   ```

`validate.py` 会检查必填字段、GPX 文件是否存在并带有 OSM 署名、每条路线 2–4 张本地照片且有作者和许可，以及页面没有外部 CDN。

## 目录

- `index.html`、`css/`、`js/`：站点
- `data/routes.json`：站点读取的数据
- `data/editorial.json`：文字稿
- `data/track_stats.json`：由轨迹算出的数字
- `gpx/`：可下载的轨迹
- `photos/`：图片
