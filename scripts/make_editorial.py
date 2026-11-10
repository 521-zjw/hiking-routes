#!/usr/bin/env python3
"""Human-written route copy. Numbers that come from the GPX are filled later by merge_routes.py."""

from __future__ import annotations

import json
from pathlib import Path

ASOF = "2026-11-10"
ROOT = Path(__file__).resolve().parents[1]


def fee(item, amount, url, name, note=""):
    row = {
        "item": item,
        "amount": amount,
        "asOf": ASOF,
        "sourceUrl": url,
        "sourceName": name,
    }
    if note:
        row["note"] = note
    return row


ZION_FEE = "https://www.nps.gov/zion/planyourvisit/fees.htm"
YOSE_FEE = "https://www.nps.gov/yose/planyourvisit/fees.htm"
GRCA_FEE = "https://www.nps.gov/grca/planyourvisit/fees.htm"
GLAC_FEE = "https://www.nps.gov/glac/planyourvisit/fees.htm"
MORA_FEE = "https://www.nps.gov/mora/planyourvisit/fees.htm"
ROMO_FEE = "https://www.nps.gov/romo/planyourvisit/fees.htm"
ARCH_FEE = "https://www.nps.gov/arch/planyourvisit/fees.htm"
GRTE_FEE = "https://www.nps.gov/grte/planyourvisit/fees.htm"
BRCA_FEE = "https://www.nps.gov/brca/planyourvisit/fees.htm"
ACAD_FEE = "https://www.nps.gov/acad/planyourvisit/fees.htm"

NONRES = "非美国居民年满 16 岁，除门票外另付 100 美元/人；持有效 America the Beautiful 年票可以免这项附加费。居民年票 80 美元，非居民年票 250 美元。免费入园日只对美国公民和居民，而且不含许可费。"


def park_fee(url, name, vehicle, moto, person, extra_nonres=True, note=""):
    text = f"私家车 {vehicle}；摩托车 {moto}；步行或自行车 {person}。"
    if extra_nonres:
        text += NONRES
    return fee("公园门票", text, url, name, note)


ROUTES = []


def add(**kwargs):
    ROUTES.append(kwargs)


add(
    slug="angels-landing",
    name="Angels Landing",
    nameZh="天使降落",
    continent="us",
    country="美国",
    countries=["美国"],
    region="犹他州",
    park="锡安国家公园",
    gateway="斯普林代尔",
    summary="从峡谷班车 The Grotto 站沿西缘步道爬到 Scout Lookout，最后半英里是开凿在岩脊上的链索路，两侧落差很大。NPS 把链索段写成 strenuous。轨迹是谷底到山顶的单程，返回大体沿原路，距离大约加倍，但爬升不会再来一遍。",
    daysMin=1, daysMax=1,
    hoursNote="NPS 把链索段本身标成 1–2 小时，不含西缘步道的上下。多数人往返要留出半天。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="NPS 用语是 strenuous：窄脊、台阶和间断链索，有的地方只容一人通过，落差可达约 1,000 英尺。",
    difficultySource="https://www.nps.gov/thingstodo/hike-angels-landing.htm",
    bestMonths=[3, 4, 5, 9, 10, 11],
    bestSeasonNote="春秋较合适。夏季峡谷很热，雨后或结冰时链索会危险或关闭。冬季日照短，有时需要冰爪。",
    permitRequired=True,
    fees=[
        park_fee(ZION_FEE, "NPS Zion Fees", "35 美元（1–7 天）", "30 美元（7 天）", "20 美元/人（15 岁及以下免费）"),
        fee("天使降落链索段许可", "抽签申请费 6 美元（一次申请最多 6 人，不退）；抽中后每人再收 3 美元。", "https://www.recreation.gov/permits/4675325", "Recreation.gov Angels Landing", "从 Scout Lookout 到山顶每天、全天都要许可。只走到 Scout Lookout 不要许可。季节抽签和前一天抽签都在 Recreation.gov，公园售票处不卖。"),
    ],
    transport="最近的商业机场多是圣乔治（SGU）或拉斯维加斯（LAS），再租车到斯普林代尔。班车季私人车通常不能开进锡安峡谷，从游客中心乘园内班车到 The Grotto（6 号站）。班车是否收费、运行月份以 NPS 当季公告为准。",
    accommodation="斯普林代尔有旅馆。园内 Watchman 和 South 营地要预订。链索路是一日往返，不在岩脊上露营。",
    links=[
        {"label": "NPS：天使降落许可", "url": "https://www.nps.gov/zion/planyourvisit/angels-landing-hiking-permits.htm"},
        {"label": "NPS：天使降落徒步说明", "url": "https://www.nps.gov/thingstodo/hike-angels-landing.htm"},
        {"label": "Recreation.gov 抽签", "url": "https://www.recreation.gov/permits/4675325"},
        {"label": "NPS：门票", "url": ZION_FEE},
    ],
)

add(
    slug="zion-narrows",
    name="The Narrows (top-down)",
    nameZh="锡安窄道（自上而下）",
    continent="us",
    country="美国",
    countries=["美国"],
    region="犹他州",
    park="锡安国家公园",
    gateway="斯普林代尔",
    summary="沿维尔京河从 Chamberlain's Ranch 走到 Temple of Sinawava 的穿越，大部分时间在河里。NPS 称之为 16 英里的 through-hike，需要荒野许可。从下游 Temple of Sinawava 往上游走到 Big Spring 则是另一条走法，NPS 写明不需要许可，往返最远约 10 英里。本页轨迹对应的是自上而下那条 OSM 路线。",
    daysMin=1, daysMax=2,
    hoursNote="下游溯河可走一小时，也可走到 Big Spring 用一整天。自上而下的 16 英里穿越通常是一天强行或一晚。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="NPS：流量低于 70 CFS 时为 moderately difficult，齐膝的湿滑河床，并常有及腰的水潭。涨水时会关闭。",
    difficultySource="https://www.nps.gov/zion/planyourvisit/thenarrows.htm",
    bestMonths=[6, 7, 8, 9, 10],
    bestSeasonNote="要等春汛退去、流量降下来。夏季有雷暴带来的骤发洪水风险，出门前看 NPS 的流量和天气。",
    permitRequired=True,
    fees=[
        park_fee(ZION_FEE, "NPS Zion Fees", "35 美元（1–7 天）", "30 美元（7 天）", "20 美元/人"),
        fee("自上而下荒野许可", "需要许可。页面说明可在线或向荒野护林员申请，但这次抓取的说明页没有写出单价。", "https://www.nps.gov/zion/planyourvisit/thenarrows.htm", "NPS The Narrows", "从下游往上走到 Big Spring 不需要这条许可。单价以申请系统当时页面为准，本站不补一个数。"),
    ],
    transport="班车季乘园内班车到 Temple of Sinawava（9 号站）是下游入口。自上而下要自己安排到 Chamberlain's Ranch 的车，NPS 写明交通需自行解决，通常是斯普林代尔的包车，价格不在 NPS 页面上。",
    accommodation="穿越可在指定营地过夜（许可上会写）。一日溯河则住斯普林代尔或园内营地。不要在窄缝里随意扎营。",
    links=[
        {"label": "NPS：窄道", "url": "https://www.nps.gov/zion/planyourvisit/thenarrows.htm"},
        {"label": "NPS：门票", "url": ZION_FEE},
    ],
)

add(
    slug="half-dome",
    name="Half Dome",
    nameZh="半圆顶",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="优胜美地国家公园",
    gateway="优胜美地谷",
    summary="一日路线从 Happy Isles 经 Vernal Fall、Nevada Fall 和小优胜美地谷，最后用钢缆爬上半圆顶。NPS 写往返 14–16 英里、累计爬升约 4,800 英尺，多数人要 10–12 小时。钢缆竖着的季节（通常是阵亡将士纪念日前的周五到十月第二个星期一之后一天）每天都要许可。",
    daysMin=1, daysMax=1,
    hoursNote="NPS：多数人往返 10–12 小时，建议日出前出发，并自己定一个折返时间。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="NPS 写明不适合没有准备的人。最后约 400 英尺靠两条钢缆，没有攀岩装备；岩石湿的时候是致命坠落的主要原因。",
    difficultySource="https://www.nps.gov/yose/planyourvisit/halfdome.htm",
    bestMonths=[6, 7, 8, 9],
    bestSeasonNote="钢缆不在的月份走不到顶。下午雷暴常见，NPS 建议早登顶。",
    permitRequired=True,
    statsMode="official",
    lengthDisplay="往返 14–16 英里",
    ascentDisplay="约 4,800 英尺",
    maxElevationM=2682,
    lengthSource="NPS：往返 14 到 16 英里。这里不把它收成一个单值。1 英里 = 1.609 公里，大约是 23–26 公里。",
    ascentSource="NPS：total of 4,800 feet。按 1 英尺 = 0.3048 米，约 1,463 米。这是从山谷出发的全程，不是 GPX 片段。",
    officialNote="OSM 里名为 Half Dome Trail 的关系只有山顶附近约 3 公里、海拔大约 2,131–2,689 米的一段，不是 NPS 说的全程。页面上的 GPX 只供看这一段，不能拿去从 Happy Isles 导航。山顶海拔 NPS 写 about 8,800 feet（约 2,682 米）。",
    fees=[
        park_fee(YOSE_FEE, "NPS Yosemite Fees", "35 美元（连续 7 天）", "30 美元（7 天）", "20 美元/人（15 岁及以下免费）"),
        fee("半圆顶日间许可", "申请费 10 美元/份（不退，按申请不按人）；抽中后 10 美元/人。", "https://www.nps.gov/yose/planyourvisit/hdpermits.htm", "NPS Half Dome permits", "季前抽签在 3 月 1 日到 31 日（美东时间），每天 225 个名额。赛季中还有提前两天的每日抽签。在小优胜美地谷过夜的人要把半圆顶写进荒野许可，而不是用这条日间抽签。"),
    ],
    transport="可飞弗雷斯诺等地，再转 YARTS 巴士进谷，票价以 yarts.com 为准。谷内穿梭巴士到 Happy Isles（16 号站）附近。NPS 写 Happy Isles 距步道停车场约半英里。",
    accommodation="一日往返住山谷营地或旅馆，都要提前订。若在小优胜美地谷露营，走荒野许可而不是日间半圆顶许可。",
    links=[
        {"label": "NPS：半圆顶", "url": "https://www.nps.gov/yose/planyourvisit/halfdome.htm"},
        {"label": "NPS：许可与费用", "url": "https://www.nps.gov/yose/planyourvisit/hdpermits.htm"},
        {"label": "NPS：门票", "url": YOSE_FEE},
    ],
)

add(
    slug="mist-trail",
    name="Mist Trail",
    nameZh="迷雾步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="优胜美地国家公园",
    gateway="优胜美地谷",
    summary="从 Happy Isles 沿梅塞德河上到 Vernal Fall，再往上可到 Nevada Fall。石阶陡、水雾大。它也是半圆顶和约翰·缪尔步道的下段。本页 GPX 是 OSM 的 Mist Trail 关系本身。",
    daysMin=1, daysMax=1,
    hoursNote="到 Vernal Fall 往返常见是半天；继续到 Nevada Fall 要留出一整天里的大半天。具体小时数 NPS 半圆顶页没有单独给迷雾步道。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="石阶湿滑、坡度大。NPS 在半圆顶页提醒 Vernal Fall 步桥以上没有处理过的饮用水。",
    difficultySource="https://www.nps.gov/yose/planyourvisit/halfdome.htm",
    bestMonths=[5, 6, 7, 8, 9, 10],
    bestSeasonNote="春末夏初水量大、水雾最盛，台阶也更滑。冬季可能结冰。",
    permitRequired=False,
    fees=[park_fee(YOSE_FEE, "NPS Yosemite Fees", "35 美元（7 天）", "30 美元", "20 美元/人")],
    transport="与半圆顶相同：YARTS 进谷，再乘谷内班车到 Happy Isles 一带。",
    accommodation="山谷营地和旅馆。这条路线本身是当日往返。",
    links=[
        {"label": "NPS：半圆顶页（含迷雾步道相关提醒）", "url": "https://www.nps.gov/yose/planyourvisit/halfdome.htm"},
        {"label": "NPS：门票", "url": YOSE_FEE},
    ],
)

add(
    slug="clouds-rest",
    name="Clouds Rest",
    nameZh="云憩峰",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="优胜美地国家公园",
    gateway="图奥勒米草地 / 优胜美地谷",
    summary="云憩峰顶是一条窄脊，能看见半圆顶和高山地。OSM 这条同名关系算出来是起终点相距很近的来回，最高点约 3,015 米，和峰顶海拔同一量级。从山谷走会更长，那不是这个文件所覆盖的全部。",
    daysMin=1, daysMax=2,
    hoursNote="从日出高地或泰纳亚湖方向当日往返很常见；从山谷接上约翰·缪尔步道则是另一条更长的路线。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="峰脊暴露。海拔将近 3,000 米，下午有雷暴。难度描述综合步道特征和海拔，不是 NPS 的正式分级原文。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="泰奥加路通常要到初夏才开，关闭日期每年不同，先看 NPS 路况。",
    permitRequired=False,
    fees=[
        park_fee(YOSE_FEE, "NPS Yosemite Fees", "35 美元（7 天）", "30 美元", "20 美元/人"),
        fee("过夜", "当日往返不要半圆顶那种许可。若在荒野露营，需要优胜美地荒野许可，费用以 NPS / Recreation.gov 当时页面为准。", "https://www.nps.gov/yose/planyourvisit/wildpermits.htm", "NPS wilderness permits"),
    ],
    transport="峰顶常用的入口在泰奥加路沿线（日出步道口或泰纳亚湖），路不通时就走不到。谷内班车不到这些高海拔入口。",
    accommodation="图奥勒米草地营地（开放季）或山谷。荒野营地要许可。",
    links=[
        {"label": "NPS：门票", "url": YOSE_FEE},
        {"label": "NPS：荒野许可", "url": "https://www.nps.gov/yose/planyourvisit/wildpermits.htm"},
        {"label": "维基百科：Clouds Rest", "url": "https://en.wikipedia.org/wiki/Clouds_Rest"},
    ],
)

add(
    slug="panorama-trail",
    name="Panorama Trail",
    nameZh="全景步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="优胜美地国家公园",
    gateway="冰川点 / 优胜美地谷",
    summary="经典走法是从冰川点下到山谷，沿途能看到内华达瀑布和维纳尔瀑布。OSM 的 Panorama Trail 关系比“冰川点一直下到谷底”的口头说法短，页面数字以轨迹为准，并在来源里写明。",
    daysMin=1, daysMax=1,
    hoursNote="从冰川点走到山谷一般是一天。回程若没有人接，还要另外安排上山的交通。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="下坡长，膝盖负担大。不是技术攀爬。",
    bestMonths=[6, 7, 8, 9, 10],
    bestSeasonNote="冰川点路冬季关闭。开放日看 NPS。",
    permitRequired=False,
    fees=[park_fee(YOSE_FEE, "NPS Yosemite Fees", "35 美元（7 天）", "30 美元", "20 美元/人")],
    transport="旺季有从山谷到冰川点的园内巴士，时刻以 NPS 为准。自己开车要占冰川点停车场。走到谷底后用谷内班车。",
    accommodation="山谷住宿。步道本身不安排过夜。",
    links=[
        {"label": "NPS：门票", "url": YOSE_FEE},
        {"label": "维基百科：Panorama Trail", "url": "https://en.wikipedia.org/wiki/Panorama_Trail"},
    ],
)

add(
    slug="bright-angel",
    name="Bright Angel Trail",
    nameZh="亮天使步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="亚利桑那州",
    park="大峡谷国家公园",
    gateway="大峡谷村（南缘）",
    summary="南缘最常用的下谷步道，有休息屋和季节性的水。GPX 是从南缘下到科罗拉多河一带的单程。当日往返要原路爬上来，距离大约加倍，回程爬升大约等于去程的下降。",
    daysMin=1, daysMax=2,
    hoursNote="只下到一个半休息点再返回是常见的一日走法。下到河边再当天返回会非常长，NPS 不鼓励没有准备的人这样做。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="难在返回时的爬升、高温和脱水，不是技术路段。夏季内峡谷可超过 40°C。",
    bestMonths=[4, 5, 9, 10],
    bestSeasonNote="夏季白天地表极热，很多人改在清晨或只走到有水的休息点。冬季南缘高处会有冰雪。",
    permitRequired=False,
    fees=[
        park_fee(GRCA_FEE, "NPS Grand Canyon Fees", "35 美元（7 天）", "30 美元", "20 美元/人", note="2026 年南缘和北缘入口都不需要预约入园。"),
        fee("过夜", "内峡谷过夜要背国许可：抽签或申请 10 美元/份（不退），谷底营地 15 美元/人/晚，缘上营地 4 美元/人/晚。", "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm", "NPS backcountry permits", "当日往返不要背国许可。幻影牧场的床位是另一套预订，不在这张许可里。"),
    ],
    transport="飞凤凰城或到弗拉格斯塔夫，再驾车约两小时量级到南缘（车程随路况变化）。园内有往返步道口的巴士，时刻看 NPS。南缘和北缘之间没有把你送回去的园内公交。",
    accommodation="南缘旅馆和 Mather 营地要预订。谷底幻影牧场和营地都要提前，而且经常满。",
    links=[
        {"label": "NPS：门票", "url": GRCA_FEE},
        {"label": "NPS：背国许可", "url": "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm"},
        {"label": "维基百科：Bright Angel Trail", "url": "https://en.wikipedia.org/wiki/Bright_Angel_Trail"},
    ],
)

add(
    slug="south-kaibab",
    name="South Kaibab Trail",
    nameZh="南凯巴布步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="亚利桑那州",
    park="大峡谷国家公园",
    gateway="大峡谷村（南缘）",
    summary="南缘另一条下谷步道，视野开、没有亮天使那样的水。GPX 从南缘步道口下到河边，几乎一路下降。很多一日徒步只走到 Ooh Aah Point 或 Cedar Ridge 就返回。",
    daysMin=1, daysMax=2,
    hoursNote="走到 Cedar Ridge 往返是半天到大半天。下到河边是长日或过夜的开始。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="无遮阴、步道上没有可靠饮水。返回全是爬升。",
    bestMonths=[4, 5, 9, 10],
    bestSeasonNote="与亮天使相同：避开盛夏中午的谷底高温。",
    permitRequired=False,
    fees=[
        park_fee(GRCA_FEE, "NPS Grand Canyon Fees", "35 美元（7 天）", "30 美元", "20 美元/人"),
        fee("过夜", "与亮天使相同的背国许可：10 美元/份，谷底 15 美元/人/晚。", "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm", "NPS backcountry permits", "当日往返不需要。"),
    ],
    transport="步道口在南缘，旺季从游客中心有接驳巴士，私人车停在指定停车场。详情以 NPS 交通页为准。",
    accommodation="同南缘。不要计划在没有许可的地方过夜。",
    links=[
        {"label": "NPS：门票", "url": GRCA_FEE},
        {"label": "NPS：背国许可", "url": "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm"},
    ],
)

add(
    slug="rim-to-rim",
    name="Grand Canyon Rim-to-Rim",
    nameZh="大峡谷双缘穿越",
    continent="us",
    country="美国",
    countries=["美国"],
    region="亚利桑那州",
    park="大峡谷国家公园",
    gateway="北缘 / 南缘",
    summary="这里取北凯巴布步道接亮天使步道，从北缘下到河边再上南缘。北缘更高，所以这一方向先大降后爬。一日完成很紧，更常见是在谷底过一夜。GPX 由两条 OSM 关系拼接，河边若有缺口会在轨迹说明里写明，没有用直线补路。",
    daysMin=1, daysMax=3,
    hoursNote="强健的人可以一天走完。更常见是 2–3 天，在亮天使营地或幻影牧场过夜。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="距离长、净爬升大、谷底炎热、饮水点有限。NPS 对没有经验的一日双缘穿越持保留态度。",
    bestMonths=[5, 6, 9, 10],
    bestSeasonNote="北缘公路和步道口大约五月中到十月中才开放，具体日期每年由 NPS 公布。南缘全年可进，但谷底夏季极热。",
    permitRequired=False,
    fees=[
        park_fee(GRCA_FEE, "NPS Grand Canyon Fees", "35 美元（7 天）", "30 美元", "20 美元/人", note="一日穿越不需要背国许可，但门票要付。北缘和南缘都要能出示门票。"),
        fee("过夜背国许可", "10 美元/份（不退）+ 谷底 15 美元/人/晚。", "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm", "NPS backcountry permits", "12 人以上的有组织一日穿越可能另要特别使用许可，见 NPS SUP 说明。"),
    ],
    transport="南北缘之间没有园内公交。商业 Trans-Canyon Shuttle 等接驳的班次和票价不在 NPS 门票页上，行前向运营商核对。最近的机场仍是弗拉格斯塔夫或凤凰城，再到南缘；北缘还要多绕路。",
    accommodation="谷底只有许可营地或幻影牧场。两端缘上有营地和旅馆。北缘开放季短。",
    links=[
        {"label": "NPS：门票", "url": GRCA_FEE},
        {"label": "NPS：背国许可", "url": "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm"},
    ],
)

add(
    slug="john-muir-trail",
    name="John Muir Trail",
    nameZh="约翰·缪尔步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="优胜美地、国王峡谷、红杉国家公园及国有林",
    gateway="优胜美地谷 / 惠特尼门",
    summary="从优胜美地谷 Happy Isles 到惠特尼峰顶的高山地长线，和太平洋屋脊步道有大段重合。OSM 关系自带的 distance 标签是 343.9 公里。本站长度用轨迹重算，和这个标签以及你走的出口（惠特尼门或继续向南）可能差一截。",
    daysMin=14, daysMax=25,
    hoursNote="常见是三周上下。每天里程差得很大，没有一个官方“标准天数”。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="高海拔、连续翻山口、要自带食物。南端进入惠特尼区还要另办惠特尼许可。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="七月山口还可能有雪。九月以后补给点和巴士减少，并开始有早雪。",
    permitRequired=True,
    fees=[
        park_fee(YOSE_FEE, "NPS Yosemite Fees", "35 美元（7 天）", "30 美元", "20 美元/人", note="从优胜美地出发要付优胜美地门票，并办荒野许可。许可费以 NPS 荒野页面当时标价为准，本次没有把一个没有核对到的数字写进来。"),
        fee("惠特尼区", "若从步道南端进出惠特尼区，还要 Inyo 国家森林的惠特尼许可：预订费 6 美元/份，区内 15 美元/人。", "https://www.recreation.gov/permits/445860", "Recreation.gov Mt. Whitney", "见惠特尼峰那一条。"),
    ],
    transport="北端同优胜美地谷。南端在 Lone Pine 之上的 Whitney Portal，季节性有 Eastern Sierra Transit，班次很有限。重新补给点包括红草地、缪尔步道牧场和独立城方向的路口，都要提前寄食物桶。",
    accommodation="几乎全程是荒野营地，要写进许可行程。山屋很少。两端才有营地和汽车旅馆。",
    links=[
        {"label": "NPS：优胜美地荒野许可", "url": "https://www.nps.gov/yose/planyourvisit/wildpermits.htm"},
        {"label": "维基百科：John Muir Trail", "url": "https://en.wikipedia.org/wiki/John_Muir_Trail"},
        {"label": "Recreation.gov：惠特尼", "url": "https://www.recreation.gov/permits/445860"},
    ],
)

add(
    slug="mount-whitney",
    name="Mount Whitney Trail",
    nameZh="惠特尼峰步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="加利福尼亚州",
    park="Inyo 国家森林 / 红杉国家公园",
    gateway="隆派恩（Lone Pine）",
    summary="美国本土最高峰的步道，从 Whitney Portal 到山顶。林务局：全年进入惠特尼区都要许可；5 月 1 日到 11 月 1 日有配额，日间每天 100 人、过夜 60 人。GPX 是门户到高处的单程，返回要沿原路。",
    daysMin=1, daysMax=2,
    hoursNote="一日登顶是很长的一天。更从容的走法是在 Trail Camp 过一夜。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="海拔从门户约 2,500 米一下到 4,400 米以上，有高反。配额季之外的冬季是登山路线，不是普通徒步。",
    difficultySource="https://www.fs.usda.gov/r05/inyo/wilderness/mount-whitney",
    bestMonths=[7, 8, 9],
    bestSeasonNote="林务局写步道通常 7 月到 9 月下旬没有积雪。配额季是 5 月 1 日到 11 月 1 日。",
    permitRequired=True,
    fees=[
        fee("惠特尼许可", "预订费 6 美元/份（不退）+ 15 美元/人。不退、不改期。", "https://www.recreation.gov/permits/445860", "Recreation.gov Mt. Whitney", "抽签申请大约 2 月 1 日到 3 月 1 日，3 月 15 日出结果，4 月 21 日太平洋时间晚 9 点前必须付清 15 美元/人。4 月 22 日起剩余名额先到先得。11 月 2 日到 4 月 30 日没有配额，但仍要许可。日期以林务局页面为准。"),
    ],
    transport="飞里诺、拉斯维加斯或洛杉矶，租车到 Lone Pine，再开到 Whitney Portal。公共班车只有季节性的 Eastern Sierra Transit，不能当成每天都有。",
    accommodation="Lone Pine 有汽车旅馆。门户有营地。Trail Camp 在配额许可的过夜行程里。",
    links=[
        {"label": "林务局：惠特尼", "url": "https://www.fs.usda.gov/r05/inyo/wilderness/mount-whitney"},
        {"label": "Recreation.gov", "url": "https://www.recreation.gov/permits/445860"},
    ],
)

add(
    slug="wonderland-trail",
    name="Wonderland Trail",
    nameZh="仙境步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="华盛顿州",
    park="雷尼尔山国家公园",
    gateway="阿什福德 / 长岭",
    summary="绕雷尼尔山一圈的荒野步道，反复落入河谷再爬上高地。OSM 关系是环线。公园入口 2026 年不实行限时预约。过夜必须有荒野许可，营地要按行程订。",
    daysMin=7, daysMax=12,
    hoursNote="完整一圈常见是 8–12 天。具体天数取决于抽到的营地间距。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="累计爬升很大，天天大上大下，天气在山上说变就变。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="七月高处还有雪。九月中以后许多营地服务结束。",
    permitRequired=True,
    fees=[
        park_fee(MORA_FEE, "NPS Mount Rainier Fees", "30 美元（连续 7 天）", "25 美元（7 天）", "15 美元（7 天）", extra_nonres=False, note="这次抓取的门票页写明 2026 年不实行限时入园预约。页内没有把其他公园那种 100 美元非居民附加费写出来，所以这里不假定雷尼尔也收。"),
        fee("荒野许可", "仙境步道过夜需要荒野许可和指定营地。2026-11-10 能打开的门票页没有列出许可单价。", "https://www.nps.gov/mora/planyourvisit/fees.htm", "NPS Mount Rainier fees", "许可本身请从公园网站的 wilderness 栏目进入 Recreation.gov 核对。这里不补一个没有看到的价格。"),
    ],
    transport="飞西雅图，租车经阿什福德从 Nisqually 入口进公园。环线可以在长岭、白河或 Mowich 等处起走，换人接应要自己安排第二辆车。",
    accommodation="沿途是许可里的荒野营地。园内和门口有汽车营地、旅馆，都要另订。",
    links=[
        {"label": "NPS：门票", "url": MORA_FEE},
        {"label": "维基百科：Wonderland Trail", "url": "https://en.wikipedia.org/wiki/Wonderland_Trail"},
    ],
)

add(
    slug="enchantments",
    name="The Enchantments Traverse",
    nameZh="魔法湖群穿越",
    continent="us",
    country="美国",
    countries=["美国"],
    region="华盛顿州",
    park="高山湖群荒野（Okanogan-Wenatchee 国家森林）",
    gateway="莱文沃思",
    summary="从 Stuart Lake 一侧翻过 Aasgard，穿过核心湖区，再从 Snow Creek 一侧下来（或反过来）。林务局：5 月 15 日到 10 月 31 日进入许可区的人都要许可。日间是免费自助许可；过夜要抽签。",
    daysMin=1, daysMax=4,
    hoursNote="核心区当日穿越是非常长的一天。过夜常见 3–4 天。林务局建议没有经验的人不要把核心区当成轻松的过夜。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="Aasgard 一侧又陡又碎。林务局写步道原始、多岩石，旅行困难。",
    difficultySource="https://www.recreation.gov/camping/poi/233273",
    bestMonths=[7, 8, 9],
    bestSeasonNote="五月、六月、九月、十月被林务局称为肩季，会遇到雪。核心区通常要到七月下旬才比较像夏天。",
    permitRequired=True,
    fees=[
        fee("过夜许可", "预先抽签申请费 6 美元（不退）；中签后 5 美元/人/天。", "https://www.recreation.gov/camping/poi/233273", "Recreation.gov Enchantments", "2026 年预先抽签申请是 2 月 15 日到 3 月 1 日，3 月 17 日通知，3 月 31 日前确认并付款。5–10 月另有必须人在地理围栏内才能申请的每日抽签。"),
        fee("日间", "日间许可免费，在步道口自取。Stuart Lake 日间停车场需要 Northwest Forest Pass。", "https://www.fs.usda.gov/r06/okanogan-wenatchee/recreation/enchantments", "USFS Enchantments", "日票价格以林务局 / Recreation.gov 当时页面为准，这里不写一个没有打开价目表核对过的数字。"),
    ],
    transport="飞西雅图，租车约两小时量级到莱文沃思，再到 Stuart Lake 或 Snow Creek 步道口。穿越需要两端接应，旺季停车场很早满。",
    accommodation="许可区过夜只能在抽中的区域按规定扎营。莱文沃思有旅馆。不要没有许可就在核心区过夜。",
    links=[
        {"label": "林务局：Enchantments", "url": "https://www.fs.usda.gov/r06/okanogan-wenatchee/recreation/enchantments"},
        {"label": "Recreation.gov 预先抽签", "url": "https://www.recreation.gov/camping/poi/233273"},
    ],
)

add(
    slug="kalalau",
    name="Kalalau Trail",
    nameZh="卡拉劳步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="夏威夷州考爱岛",
    park="纳帕利海岸州立荒野公园",
    gateway="哈纳莱伊 / 基拉韦厄",
    summary="沿纳帕利海岸的悬崖小径，终点是卡拉劳海滩。州立公园页面写往返 22 英里、难度 Difficult、海拔增益 800 英尺。本站 DEM 算出的累计爬升通常会高于这 800 英尺，因为小径反复上下；两个数都保留，分别注明来源。",
    daysMin=1, daysMax=3,
    hoursNote="只到 Hanakapiʻai 是一日。到卡拉劳海滩常见是 2 天，州立公园允许在纳帕利最多住 5 晚，且 Hanakoa 不能连住两晚。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="州立公园难度栏写的是 Difficult。小径湿、窄，有落石和涨水的溪谷。",
    difficultySource="https://dlnr.hawaii.gov/dsp/hiking/kauai/kalalau-trail/",
    bestMonths=[5, 6, 7, 8, 9],
    bestSeasonNote="冬季北岸浪大和降雨更多，小溪会暴涨。夏季相对稳，但仍要看当天警报。",
    permitRequired=True,
    fees=[
        fee("露营", "纳帕利海岸：夏威夷居民 25 美元/人/晚，非居民 35 美元/人/晚。", "https://dlnr.hawaii.gov/dsp/hiking/kauai/kalalau-trail/", "Hawaii DLNR Kalalau Trail", "同一页写明：现在进入卡拉劳步道必须有日间预约，或有效露营许可，并且要有停车预约。日间预约的单价若与露营不同，以预约页面为准。"),
    ],
    transport="飞檀香山再转机到考爱岛利胡埃，租车到北岸 Keʻe 步道口。北岸在大雨时会封路或封桥，先看县交通公告。",
    accommodation="卡拉劳海滩和 Hanakoa 按许可露营。超过 Hanakapiʻai 的过夜都算在上述露营费里。哈纳莱伊有少量旅馆，旺季很满。",
    links=[
        {"label": "夏威夷州立公园：卡拉劳", "url": "https://dlnr.hawaii.gov/dsp/hiking/kauai/kalalau-trail/"},
    ],
)

add(
    slug="franconia-ridge",
    name="Franconia Ridge Trail",
    nameZh="弗朗科尼亚山脊",
    continent="us",
    country="美国",
    countries=["美国"],
    region="新罕布什尔州",
    park="白山国家森林",
    gateway="林肯 / 弗兰科尼亚山口",
    summary="阿巴拉契亚小径经过的一段高山裸脊，能看见拉斐特山。OSM 这条关系主要是山脊本身，不等于“落水溪 + 山脊 + 马道”那个更长的环线。环线要另算。",
    daysMin=1, daysMax=1,
    hoursNote="只走山脊通常要接上其他步道才能回到停车场，所以实际时间长于山脊本身。完整环线常见是一整天。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="裸脊风大、雷暴时没有地方躲。白山天气以恶劣出名。",
    bestMonths=[6, 7, 8, 9],
    bestSeasonNote="六月还可能有残雪。秋季晴天最受欢迎，周末停车场黎明前满。冬季是另一种装备。",
    permitRequired=False,
    fees=[
        fee("停车", "白山国家森林许多步道口需要停车通行证。日票和年票价格以 forest service / White Mountain National Forest 当时页面为准。", "https://www.fs.usda.gov/r09/whitemountain", "White Mountain National Forest", "山脊本身没有像半圆顶那样的徒步抽签。"),
    ],
    transport="飞波士顿，租车约两个半小时量级到弗兰科尼亚山口或落水溪步道口。没有实用的每日公交到步道口。",
    accommodation="林肯和北伍德斯托克有旅馆和汽车旅馆。山脊上没有山屋；拉斐特营地在树线以下，AMC 营地要另订。",
    links=[
        {"label": "白山国家森林", "url": "https://www.fs.usda.gov/r09/whitemountain"},
        {"label": "维基百科：Franconia Ridge", "url": "https://en.wikipedia.org/wiki/Franconia_Ridge"},
    ],
)

add(
    slug="teton-crest",
    name="Teton Crest Trail",
    nameZh="提顿山脊步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="怀俄明州",
    park="大提顿国家公园及周边国有林",
    gateway="德鲁伊 / 杰克逊",
    summary="沿提顿山主脊走的高线，常见方向从阿拉斯加盆地或菲利普斯山口进入，从峡谷口（如 Paintbrush 或 Granite）下到珍妮湖。公园内过夜要背国许可。",
    daysMin=3, daysMax=5,
    hoursNote="完整山脊常见 3–5 天。只走其中一段（例如 Paintbrush 到 Cascade）可以更短。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="多个山口超过 3,000 米，下午雷暴，八月以后水源变少。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="七月上旬山口仍可能有雪。九月中步道口开始有早雪。",
    permitRequired=True,
    fees=[
        park_fee(GRTE_FEE, "NPS Grand Teton Fees", "35 美元（7 天）", "30 美元", "20 美元/人"),
        fee("背国许可", "在国家公园内过夜需要许可。本次没有从门票页抄到步道许可单价。", "https://www.nps.gov/grte/planyourvisit/back.htm", "NPS Grand Teton backcountry", "阿拉斯加盆地的起点在国有林一侧，营地规则和公园不同。走之前把两边的许可都问清。"),
    ],
    transport="飞杰克逊霍尔（JAC），租车到相应步道口。山脊两端不在同一条路上，几乎都要安排接送或两辆车。",
    accommodation="高处是许可营地。珍妮湖和杰克逊有旅馆。有的路段可以住 Jenny Lake 的营地，那也要订。",
    links=[
        {"label": "NPS：大提顿门票", "url": GRTE_FEE},
        {"label": "维基百科：Teton Crest Trail", "url": "https://en.wikipedia.org/wiki/Teton_Crest_Trail"},
    ],
)

add(
    slug="longs-peak",
    name="Longs Peak Keyhole Route",
    nameZh="朗斯峰钥匙孔路线",
    continent="us",
    country="美国",
    countries=["美国"],
    region="科罗拉多州",
    park="落基山国家公园",
    gateway="埃斯蒂斯帕克",
    summary="科罗拉多最著名的 14er 之一。钥匙孔以上是暴露的三类路，不是公园里的普通步道。GPX 从朗斯峰步道口附近上到约 4,345 米，和峰顶 14,259 英尺（约 4,346 米）一致。返回沿原路。",
    daysMin=1, daysMax=1,
    hoursNote="当日往返通常要 12 小时上下，午夜到凌晨出发才能躲开下午雷暴。这是习惯时长，不是 NPS 的官方计时。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="钥匙孔之后有窄脊和悬崖，遇雨、冰或雷电要立刻下撤。没有半圆顶那种钢缆。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="无雪窗口经常只有七月下旬到九月上旬。其他月份按技术攀登准备。",
    permitRequired=False,
    fees=[
        park_fee(ROMO_FEE, "NPS Rocky Mountain Fees", "1 天 30 美元，7 天 35 美元", "1 天 25 美元，7 天 30 美元", "1 天 15 美元，7 天 20 美元", note="五月下旬到十月中旬，部分区域和时段需要限时入园预约，朗斯峰走廊是否被包括以 NPS 当年地图为准。"),
    ],
    transport="飞丹佛，租车到埃斯蒂斯帕克，再开到 Longs Peak 步道口。停车场在旺季半夜就满。没有公交到步道口。",
    accommodation="埃斯蒂斯帕克有旅馆。步道口附近的营地要另订。这是当日往返，钥匙孔以上不能露营。",
    links=[
        {"label": "NPS：落基山门票", "url": ROMO_FEE},
        {"label": "维基百科：Longs Peak", "url": "https://en.wikipedia.org/wiki/Longs_Peak"},
    ],
)

add(
    slug="timberline-trail",
    name="Timberline Trail",
    nameZh="林线步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="俄勒冈州",
    park="胡德山国家森林",
    gateway="胡德山林线旅馆",
    summary="绕胡德山一圈，大约在林线附近，要涉过冰川融水溪。OSM 关系是环线。周末从林线旅馆起走的人最多。",
    daysMin=3, daysMax=5,
    hoursNote="完整一圈常见 3–5 天。强行也有人用一个周末加一天。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="溪流在下午融雪后水位高，有的渡口要改时间或绕路。不是技术冰川路线，但天气和涉水是主要风险。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="八月是最常走的月份。七月渡口更危险。十月开始有雪。",
    permitRequired=True,
    fees=[
        fee("荒野许可", "胡德山荒野过夜通常要在步道口自助登记。本次没有核对到一个单独的许可价格，不填写金额。", "https://www.fs.usda.gov/r06/mthood", "Mt. Hood National Forest", "林线旅馆一带停车可能要美国国有林的通行证，价格以当地步道口告示和 Recreation.gov 为准。"),
    ],
    transport="飞波特兰，租车约 1.5 小时量级到林线旅馆。没有日常公交到步道口。环线可以在 Cloud Cap、Timberline 或 Ramona Falls 等处进出。",
    accommodation="沿途荒野营地。林线旅馆是历史旅馆，价格高，要另订。政府营地位于较低的公路旁。",
    links=[
        {"label": "胡德山国家森林", "url": "https://www.fs.usda.gov/r06/mthood"},
        {"label": "维基百科：Timberline Trail", "url": "https://en.wikipedia.org/wiki/Timberline_Trail"},
    ],
)

add(
    slug="havasupai",
    name="Havasupai Trail",
    nameZh="哈瓦苏瀑布步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="亚利桑那州",
    park="哈瓦苏派保留地",
    gateway="海瓦苏派希尔顶（Hualapai Hilltop）",
    summary="从 Hilltop 下到苏派村，再走到哈瓦苏瀑布和穆尼瀑布。土地在哈瓦苏派部落，不在大峡谷国家公园的步道系统里。必须有部落的预约。2026-11-10 打开的官网首页没有在静态页面里写出票价，所以这里不填金额。",
    daysMin=2, daysMax=3,
    hoursNote="下到村里常见要数小时，再走到瀑布。多数行程是 2–3 晚。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="来回都是同样的高差，夏天极热，背包要带够水。部落对直升机进出有单独规定。",
    bestMonths=[4, 5, 9, 10],
    bestSeasonNote="夏季峡谷炎热。雨季有洪水。部落会因洪水或设施关闭保留地，行前看官网公告。",
    permitRequired=True,
    fees=[
        fee("部落预约", "必须通过部落官方预订系统。2026-11-10 的首页没有给出可引用的单价。", "https://www.havasupaireservations.com/", "Havasupai Reservations", "不要从二手博客抄价格。大峡谷国家公园门票不能代替部落许可。"),
    ],
    transport="飞拉斯维加斯或凤凰城，租车到 Hualapai Hilltop。最后一段是土路。没有公共交通到 Hilltop。",
    accommodation="村里营地、旅馆或部落指定的住宿都含在预约里，不能自己找地方扎营。",
    links=[
        {"label": "哈瓦苏派官方预订", "url": "https://www.havasupaireservations.com/"},
    ],
)

add(
    slug="navajo-loop",
    name="Navajo Loop Trail",
    nameZh="纳瓦霍环线",
    continent="us",
    country="美国",
    countries=["美国"],
    region="犹他州",
    park="布莱斯峡谷国家公园",
    gateway="布莱斯峡谷",
    summary="从日落点下到峡谷底部的短环线，两壁是石柱。常和女王花园步道接成更长的环。冬天台阶会结冰，公园经常关闭。",
    daysMin=1, daysMax=1,
    hoursNote="环线本身通常 1–3 小时。接上女王花园则是半天。",
    difficulty="moderate", difficultyZh="中等",
    difficultyNote="台阶多，海拔约 2,400 米以上会喘。不是暴露的山脊。",
    bestMonths=[5, 6, 9, 10],
    bestSeasonNote="冬季关闭很常见。夏季中午暴晒，但步道短。",
    permitRequired=False,
    fees=[park_fee(BRCA_FEE, "NPS Bryce Canyon Fees", "35 美元", "30 美元（7 天）", "20 美元/人")],
    transport="飞拉斯维加斯或盐湖城，租车经 12 号公路到公园。园内有接驳，是否停靠日落点以 NPS 当季时刻为准。",
    accommodation="园内营地和布莱斯峡谷城的旅馆。步道是当日往返。",
    links=[
        {"label": "NPS：布莱斯门票", "url": BRCA_FEE},
        {"label": "维基数据：Navajo Loop Trail", "url": "https://www.wikidata.org/wiki/Q104976865"},
    ],
)

add(
    slug="precipice-trail",
    name="Precipice Trail",
    nameZh="峭壁步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="缅因州",
    park="阿卡迪亚国家公园",
    gateway="巴尔港",
    summary="阿卡迪亚最陡的短线之一，靠铁梯和扶手贴着山崖走。春天到夏末常因游隼筑巢关闭。不是推车或怕高的路线。",
    daysMin=1, daysMax=1,
    hoursNote="开放时通常 2–4 小时往返。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="垂直铁梯和暴露岩架。公园在步道口明确劝退怕高的人。",
    bestMonths=[9, 10],
    bestSeasonNote="游隼季（常为春到仲夏）关闭。秋季开放的日子最多，但仍要当天看 NPS 告示。",
    permitRequired=False,
    fees=[
        park_fee(ACAD_FEE, "NPS Acadia Fees", "35 美元（7 天）", "30 美元", "20 美元/人", note="卡迪拉克山山顶公路另要 6 美元车辆预约。峭壁步道不在那条山顶公路上，不要把两项弄混。"),
    ],
    transport="飞班戈或波特兰，租车到巴尔港，再进环园路。岛上 Explorer 巴士覆盖一部分景点，是否停峭壁步道口以当季路线图为准。",
    accommodation="巴尔港旅馆，或园内 Blackwoods 等营地。当日往返。",
    links=[
        {"label": "NPS：阿卡迪亚门票", "url": ACAD_FEE},
    ],
)

add(
    slug="monitor-ridge",
    name="Monitor Ridge",
    nameZh="监视者山脊",
    continent="us",
    country="美国",
    countries=["美国"],
    region="华盛顿州",
    park="圣海伦斯火山国家纪念地",
    gateway="城堡岩 / 火山口",
    summary="从火山南侧的登山口沿石坡爬到 1980 年爆发后的火山口边缘。后半段是没有小径的火山渣和巨石。需要攀登许可，名额按天发放。",
    daysMin=1, daysMax=1,
    hoursNote="往返常见要一整天。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="松散火山渣，上行和下行都很磨脚。天气在火山口边缘变得很快。",
    bestMonths=[6, 7, 8, 9],
    bestSeasonNote="许可季通常是晚春到秋季，冬季路线不同。以纪念地当年公告为准。",
    permitRequired=True,
    fees=[
        fee("攀登许可", "纪念地按天限制登顶人数，许可在 Recreation.gov。本次没有打开到一份写明 2026 年单价的官方价目，所以不填金额。", "https://www.recreation.gov/", "Recreation.gov", "搜索 Mount St. Helens climbing permit。另外纪念地入口或停车是否另收费，以 USDA / NFS 页面为准。"),
    ],
    transport="飞波特兰或西雅图，租车到南侧 Climber's Bivouac。土路最后一段，没有公交。",
    accommodation="附近国有林营地和城堡岩的旅馆。登顶是当日往返，火山口边缘不能露营。",
    links=[
        {"label": "Recreation.gov 首页（再搜索圣海伦斯攀登许可）", "url": "https://www.recreation.gov/"},
        {"label": "维基百科：Mount St. Helens", "url": "https://en.wikipedia.org/wiki/Mount_St._Helens"},
    ],
)

add(
    slug="highline-glacier",
    name="Highline Trail",
    nameZh="高线步道（冰川国家公园）",
    continent="us",
    country="美国",
    countries=["美国"],
    region="蒙大拿州",
    park="冰川国家公园",
    gateway="西冰川 / 罗根山口",
    summary="从罗根山口沿花园墙走到花岗岩公园小木屋，是公园里最常被提到的一日徒步。英文维基百科写这段是 7.6 英里（12.2 公里），之后还可以再往 Fifty Mountain 方向走。没有找到一条干净、完整的 OSM 路线关系，所以 GPX 暂缺。",
    daysMin=1, daysMax=2,
    hoursNote="到花岗岩公园小木屋再返回罗根山口，或坐巴士从 The Loop 接回，是常见的一天。",
    difficulty="hard", difficultyZh="困难",
    difficultyNote="靠近山口的一段是贴着陡坡的窄路。有雪时公园会关闭。不是技术攀登，但暴露。",
    bestMonths=[7, 8, 9],
    bestSeasonNote="去太阳公路和罗根山口通常 6 月底到 10 月开放，积雪会让高线步道比公路更晚开放。",
    permitRequired=False,
    lengthDisplay="7.6 英里（至花岗岩公园小木屋）",
    lengthSource="英文维基百科 Highline Trail (Glacier National Park)：Logan Pass 到 Granite Park Chalet 7.6 英里（12.2 公里）。这是百科转述，不是 NPS 测绘报告。GPX 暂缺，所以不用轨迹长度。",
    ascentSource="没有 GPX，不做 DEM 爬升。维基百科该条目没有给出本站愿意单独引用的累计爬升。",
    fees=[
        park_fee(GLAC_FEE, "NPS Glacier Fees", "35 美元（11 月 1 日到 4 月 30 日为 25 美元）", "30 美元（冬季 20 美元）", "20 美元（冬季 15 美元）", note="同一页写 2026 年公园任何区域都不需要车辆预约。"),
        fee("花岗岩公园小木屋", "床位由承租人经营，价格不在 NPS 门票页上。", "https://www.nps.gov/glac/planyourvisit/fees.htm", "NPS Glacier Fees", "只走路、不住小木屋，就没有这项费用。"),
    ],
    transport="飞卡利斯佩尔或大瀑布城，租车到西侧入口，再沿去太阳公路到罗根山口。园内免费班车（开放季）可以用来做单程徒步，时刻以 NPS 为准。",
    accommodation="阿普加和公园门外有营地、旅馆。花岗岩公园小木屋要另订。步道旁过夜属于荒野许可。",
    links=[
        {"label": "NPS：门票与 2026 年不预约", "url": GLAC_FEE},
        {"label": "维基百科：Highline Trail", "url": "https://en.wikipedia.org/wiki/Highline_Trail_(Glacier_National_Park)"},
    ],
)

add(
    slug="presidential-traverse",
    name="Presidential Traverse",
    nameZh="总统山脉纵贯",
    continent="us",
    country="美国",
    countries=["美国"],
    region="新罕布什尔州",
    park="白山国家森林",
    gateway="阿巴拉契亚山口 / 伦道夫",
    summary="把华盛顿山、亚当斯山、杰斐逊山等总统峰连成一天或两天的山脊穿越，大部分在树线以上。没有一条被维基数据和 OSM 检索稳定对应到“全程”的关系，GPX 暂缺，避免把几段步道拼成一条看起来完整、实际上可能错的线。",
    daysMin=1, daysMax=2,
    hoursNote="一日南北纵贯是白山著名的长日。分成两天、住在湖畔小屋的人很多。",
    difficulty="strenuous", difficultyZh="艰辛",
    difficultyNote="长距离裸脊、风速常达到飓风级别，华盛顿山的天气记录以极端出名。走错天气是主要事故原因。",
    bestMonths=[6, 7, 8, 9],
    bestSeasonNote="即使八月也可能接近冰点。冬季是高山技术路线。周末山屋要提前数月订。",
    permitRequired=False,
    lengthSource="没有采用轨迹长度。公开介绍里的里程差得比较大（大约 20 英里量级），本站在没有官方测绘页的情况下不挑一个数。",
    ascentSource="没有 GPX。累计爬升常被写成超过 8,000 英尺，但来源不一，这里不引用未经核对的单值。",
    fees=[
        fee("停车与山屋", "日间穿越本身通常没有徒步抽签。华盛顿山汽车路和齿轨火车是另一张票。AMC 山屋按床位收费。", "https://www.outdoors.org/", "Appalachian Mountain Club", "2026-11-10 没有把 AMC 价目表抓成可引用的单价，床位价格请直接打开 outdoors.org。白山步道口停车通行证见国有林。"),
    ],
    transport="飞波士顿，租车到阿巴拉契亚山口（北端附近）或克劳福德山口 / 平克姆山口。南北两端要两辆车或包接送。华盛顿山有季节性的齿轨火车，那不是步道的替代。",
    accommodation="湖畔小屋（Lakes of the Clouds）等 AMC 山屋，以及平克姆山口、伦道夫的旅馆。树线以上没有可靠的临时露营点。",
    links=[
        {"label": "AMC", "url": "https://www.outdoors.org/"},
        {"label": "维基百科：Presidential Traverse", "url": "https://en.wikipedia.org/wiki/Presidential_Traverse"},
        {"label": "白山国家森林", "url": "https://www.fs.usda.gov/r09/whitemountain"},
    ],
)

add(
    slug="delicate-arch",
    name="Delicate Arch Trail",
    nameZh="精致拱门步道",
    continent="us",
    country="美国",
    countries=["美国"],
    region="犹他州",
    park="拱门国家公园",
    gateway="摩押",
    summary="公园标志性拱门的步道，后半段是光滑的砂岩坡，没有护栏。OSM 里这条步道被拆成许多短 way，没有一条可靠的路线关系把它们按顺序收齐，GPX 暂缺。",
    daysMin=1, daysMax=1,
    hoursNote="常见是 2–3 小时往返。这是游记里的习惯时长，不是本次抓到的 NPS 原文。",
    difficulty="moderate", difficultyZh="中等",
    difficultyNote="暴露的岩坡，下雨或结冰时很滑。没有链索。夏天没有遮阴。",
    bestMonths=[4, 5, 9, 10],
    bestSeasonNote="夏季地表温度极高。冬季岩坡结冰会关闭或变得危险。",
    permitRequired=False,
    lengthSource="没有 GPX，也没有在 2026-11-10 抓到一份写明里程的 NPS 步道页，所以长度留空，不采用游记里的“3 英里”。",
    ascentSource="没有 GPX，不估算爬升。",
    fees=[
        fee("公园门票", "私家车 30 美元；摩托车 25 美元（7 天）；步行 15 美元/人。", ARCH_FEE, "NPS Arches Fees", "这次抓取的拱门门票页没有写出其他公园那种 100 美元非居民附加费，因此这里不加上。限时入园是否恢复，以 NPS 当季公告为准。"),
    ],
    transport="飞摩押附近的峡谷地机场班次很少，多数人飞盐湖城或格兰德章克申再租车。步道口在公园内 Wolfe Ranch 一带。",
    accommodation="摩押的旅馆，或公园外的营地。拱门步道是当日往返。",
    links=[
        {"label": "NPS：拱门门票", "url": ARCH_FEE},
        {"label": "维基百科：Delicate Arch", "url": "https://en.wikipedia.org/wiki/Delicate_Arch"},
    ],
)


def main():
    # Europe is appended by make_editorial_eu.py if present, else only US is written when run alone.
    extra = Path(__file__).with_name("make_editorial_eu.py")
    routes = list(ROUTES)
    if extra.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("eu", extra)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        routes.extend(mod.ROUTES)
    doc = {
        "meta": {
            "title": "山径手册",
            "owner": "Junwei Zhang",
            "place": "北京",
            "updated": ASOF,
            "gpxLicense": "© OpenStreetMap contributors, ODbL 1.0",
            "gpxLicenseUrl": "https://www.openstreetmap.org/copyright",
            "note": "费用金额只来自查阅当日的官方页面。轨迹长度和高程由 scripts/build_tracks.py 计算后合并。",
        },
        "routes": routes,
    }
    dest = ROOT / "data" / "editorial.json"
    dest.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print("routes", len(routes), "->", dest)


if __name__ == "__main__":
    main()
