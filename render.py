#!/usr/bin/env python3
"""Render the news-image-20261123 V1fresh2 front page (1024x1024 PNG).

Drawn from scratch in this session with Pillow: flat geometric scenes,
a numbered-pin world map, and typography. No network, no external assets,
no timestamps. Deterministic: same input data -> same bytes.

PUTARAN 2 (25 Nov 01:xx WIB, sesi utama, Gas Kevin 01:01 WIB):
- #14 diganti: Asia Power Index (sumber primer Lowy 22 Nov, bukan 23 Nov)
  -> China sentences official to death for spying (Baomiguan post Senin
  23 Nov; Reuters/CNN/SCMP/Sowetan 23 Nov). Tempat BEIJING, AS, REPORTED.
- Pin 14: Wellington (salah) -> Beijing (116.4, 39.9), offset (-16, 8).
- Strip UTC 10:00 POWER INDEX -> 07:30 CUCUTA DRONE (#33, komunike polisi
  ~02:30 COT = 07:30 UTC; laporan pers menyebut 02:15 = 07:15 UTC).
- Masthead tetap "15 FIELDS": bidang research ikut pergi bersama #14,
  markets masuk (#39) -> 15 bidang berbeda; masthead, data, taksonomi
  kini sepakat di angka 15 (lihat sumber-V1fresh2.md).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # outer margin
CW = W - 2 * M              # content width = 992
GAP = 8

PAPER = (246, 240, 225)
INK = (28, 26, 23)
TEAL = (18, 59, 56)         # primary dark (ink-teal)
TEAL_DK = (12, 42, 40)
TEAL_LT = (216, 228, 222)   # light teal tint
BRICK = (179, 64, 42)
CREAM = (252, 248, 238)     # card face
SAND = (232, 220, 196)
SAGE = (139, 156, 122)      # map land
SAGE_DK = (110, 128, 96)
SKY = (176, 203, 212)
MUTED = (110, 102, 88)      # secondary text on paper
RULE = (190, 178, 152)      # hairline

REGION = {  # name -> (label, colour) ; colour used in bar, card number, map pin
    "AF": ("AF", (122, 90, 24)),
    "ME": ("ME", (160, 58, 42)),
    "AM": ("AM", (47, 93, 138)),
    "AS": ("AS", (122, 59, 110)),
    "EU": ("EU", (63, 110, 78)),
    "OC": ("OC", (140, 94, 10)),
    "WORLD": ("WORLD", (85, 85, 85)),
}
STATUS = {  # word -> RGB tuple
    "CONFIRMED": (46, 110, 70),
    "REPORTED": (140, 94, 10),
    "CLAIM": (179, 64, 42),
}

FDIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: ImageFont.truetype(
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# ---------------------------------------------------------------- data
# Leads: (n, place, field, region, status, title, deck, big, biglabel, scene)
LEADS = [
    (1, "BENGHAZI, LIBYA", "CONFLICT", "AF", "CLAIM",
     "Ukraine claims it sank a Russian warship off Libya",
     "Seven naval drones hit the corvette Merkury and the cargo ship Angara, Kyiv says.",
     "7", "NAVAL DRONES", "nightsea"),
    (2, "STRAIT OF HORMUZ", "CONFLICT", "ME", "CLAIM",
     "Iran vows to fight the US blockade",
     "Tehran said Sunday it shot down a US drone; blasts reported in the Strait of Hormuz.",
     "1", "DRONE DOWN", "strait"),
    (3, "SILICON VALLEY, USA", "BUSINESS", "AM", "CONFIRMED",
     "Nvidia brings back Jensen Huang",
     "Shares jump 33% and Wall Street rallies as the CEO returns 11 days after resigning.",
     "+33%", "SHARE JUMP", "chipchart"),
]

# Grid cards #4-#11: (n, place, field, region, status, title, big, biglabel, scene)
GRID = [
    (4, "ANTALYA, TÜRKIYE", "CLIMATE", "OC", "REPORTED",
     "COP31 fallout: Australia blames, Pacific despairs", "0", "NO DEAL", "climate"),
    (5, "KYIV, UKRAINE", "CONFLICT", "EU", "CONFIRMED",
     "Russia fires 153 drones; Dymer toll rises to 11", "153", "DRONES", "drones"),
    (6, "WARSAW, POLAND", "CONFLICT", "EU", "CONFIRMED",
     "NATO to send AWACS jets to Poland", "3", "MISSILES", "awacs"),
    (7, "BRUSSELS, BELGIUM", "POLITICS", "EU", "CONFIRMED",
     "EU proposes 22nd Russia sanctions package", "22ND", "PACKAGE", "sanctions"),
    (8, "WASHINGTON, USA", "POLITICS", "AM", "CONFIRMED",
     "Democrats take 258 seats, most since 1992", "258", "SEATS", "capitol"),
    (9, "BEIJING, CHINA", "DIPLOMACY", "AS", "REPORTED",
     "China rejects 'sphere of influence' after summit", "19", "SUMMIT DAY", "diplomacy"),
    (10, "JAKARTA, INDONESIA", "POLITICS", "AS", "CONFIRMED",
     "Prabowo names Amran & Sugiono as VP picks", "2", "VP PICKS", "podium"),
    (11, "CIKANDE, INDONESIA", "DISASTER", "AS", "CONFIRMED",
     "Factory fire toll confirmed: 24 dead, 30 missing", "24", "DEAD", "fire"),
]

# List #12-#41: (n, short title, place, region, status)
LIST = [
    (12, "'El Chapo Isidro' captured in Sinaloa", "SINALOA", "AM", "CONFIRMED"),
    (13, "India gives $1.62bn aid to flood-hit Nepal", "NEW DELHI", "AS", "CONFIRMED"),
    (14, "China sentences official to death for spying", "BEIJING", "AS", "REPORTED"),
    (15, "India–New Zealand Test ends in draw", "WELLINGTON", "OC", "CONFIRMED"),
    (16, "Mali beats Belgium 2–1, U17 World Cup", "DOHA", "AF", "CONFIRMED"),
    (17, "FIFA names Women's World Cup hosts 2031 & 2035", "ZURICH", "EU", "CONFIRMED"),
    (18, "BepiColombo safe in stable orbit around Mercury", "SPACE", "WORLD", "CONFIRMED"),
    (19, "Rare ancient star found, clues to early universe", "BENGALURU", "AS", "CONFIRMED"),
    (20, "Ariane 6 Amazon Leo launch halted, retry Tuesday", "KOUROU", "AM", "CONFIRMED"),
    (21, "Germany to use Kyiv's Delta battle tool", "BERLIN", "EU", "CONFIRMED"),
    (22, "Seoul names new foreign minister, spy chief", "SEOUL", "AS", "CONFIRMED"),
    (23, "US sanctions dozens in Iran shadow banking", "WASHINGTON", "ME", "CONFIRMED"),
    (24, "Indonesia names 6 treason suspects", "JAKARTA", "AS", "REPORTED"),
    (25, "Bolsonaro stable in ICU; no surgery for now", "BRASÍLIA", "AM", "CONFIRMED"),
    (26, "US blacklists Megaspeed, Alibaba unit over AI chips", "WASHINGTON", "AM", "CONFIRMED"),
    (27, "UK recognises Rohingya genocide, sanctions 5 officers", "LONDON", "EU", "CONFIRMED"),
    (28, "Omo-Agege survives assassination attempt; 4 die", "DELTA", "AF", "REPORTED"),
    (29, "Libya's eastern govt seeks UN probe into Benghazi strike", "BENGHAZI", "AF", "CONFIRMED"),
    (30, "Saudi strike on Hodeidah telecom site kills 17", "HODEIDAH", "ME", "REPORTED"),
    (31, "Hamas executes Qassam operative for 'collaborating'", "GAZA", "ME", "REPORTED"),
    (32, "Rep. Jimmy Gomez resigns after ethics report", "WASHINGTON", "AM", "CONFIRMED"),
    (33, "Drone attack on police base in Cúcuta injures 3", "CÚCUTA", "AM", "CONFIRMED"),
    (34, "Houthi attacks in Taiz kill 2, injure 8", "TAIZ", "ME", "REPORTED"),
    (35, "Murmansk governor detained for embezzlement", "MURMANSK", "EU", "REPORTED"),
    (36, "Armenia proposes new constitution, drops Karabakh claim", "YEREVAN", "EU", "CONFIRMED"),
    (37, "Molly Meldrum dies aged 83", "MELBOURNE", "OC", "CONFIRMED"),
    (38, "Virginia & Oregon sue Musk firms over Grok", "VIRGINIA", "AM", "CONFIRMED"),
    (39, "SK hynix shares +20% on Huang return", "SEOUL", "AS", "CONFIRMED"),
    (40, "Trump halts lead-azide detonation in Iowa", "IOWA", "AM", "CONFIRMED"),
    (41, "NHS starts largest AI breast-screening trial", "CAMBRIDGE", "EU", "CONFIRMED"),
]

# UTC strip: (time, label, story n)
UTC = [
    ("06:00", "153 DRONES", 5),
    ("07:00", "BENGHAZI CLAIM", 1),
    ("07:30", "CÚCUTA DRONE", 33),
    ("11:00", "VP PICKS", 10),
    ("13:30", "COP31 BACKLASH", 4),
    ("14:00", "HUANG RETURNS", 3),
]

# Numbers ribbon: (big, label, contrast line, story n)
RIBBON = [
    ("153", "DRONES IN ONE NIGHT", "134 stopped or jammed", 5),
    ("7", "NAVAL DRONES", "1 corvette claimed sunk", 1),
    ("33%", "NVIDIA SHARE JUMP", "S&P 500 up 4.82%", 3),
    ("258", "HOUSE SEATS", "biggest majority since 1992", 8),
    ("24", "DEAD IN FACTORY FIRE", "about 30 still missing", 11),
    ("$1.62bn", "AID FOR NEPAL", "after deadly floods", 13),
]

COUNTS = [("AF", 4), ("ME", 5), ("AM", 10), ("AS", 9), ("EU", 9), ("OC", 3), ("WORLD", 1)]

# Map pins: n -> (lon, lat, dx, dy) ; dx/dy spread pins sharing a city.
PINS = {
    1: (19.7, 32.1, -8, -6), 2: (56.5, 26.5, 13, -11), 3: (-122.0, 37.4, 0, 0), 4: (30.7, 36.9, 0, -1),
    5: (30.5, 50.4, -20, -2), 6: (21.0, 52.2, 18, 6), 7: (4.35, 50.85, -20, 14), 8: (-77.0, 38.9, 2, -7),
    9: (116.4, 39.9, 0, 3), 10: (106.8, -6.2, -12, -10), 11: (106.3, -6.2, -18, 8), 12: (-107.2, 24.8, 0, 0),
    13: (77.2, 28.6, 1, 1), 14: (116.4, 39.9, -16, 8), 15: (174.8, -41.3, -2, -12), 16: (51.5, 25.3, -15, 13),
    17: (8.54, 47.38, -8, 20), 19: (77.6, 13.0, 0, 0), 20: (-52.6, 5.2, 0, 0), 21: (13.4, 52.5, -4, -28),
    22: (127.0, 37.5, -16, -18), 23: (-77.0, 38.9, -18, -15), 24: (106.8, -6.2, 14, 10), 25: (-47.9, -15.8, 0, 0),
    26: (-77.0, 38.9, 18, -10), 27: (-0.13, 51.5, -22, -8), 28: (6.5, 5.5, 0, 0), 29: (19.7, 32.1, 18, 6),
    30: (42.95, 14.8, -22, -10), 31: (34.5, 31.4, 18, 14), 32: (-77.0, 38.9, 1, 19), 33: (-72.5, 7.9, 0, 0),
    34: (44.0, 13.6, 22, 4), 35: (33.0, 69.0, 1, -1), 36: (44.5, 40.2, 2, 2), 37: (145.0, -37.8, 0, 0),
    38: (-77.4, 37.5, -3, 4), 39: (127.0, 37.5, 14, 10), 40: (-93.6, 41.9, 0, 3), 41: (0.12, 52.2, 30, -4),
}
# Story 18 orbits Mercury: no pin on the Earth map (said so in the caption).

# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)

def rrect(draw, box, rad, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

def hline(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

def status_chip(draw, x, y, status, fnt):
    """Small dot + status word at (x, y); returns width used."""
    col = STATUS[status]
    draw.ellipse([x, y + 2, x + 7, y + 9], fill=col)
    draw.text((x + 11, y), status, font=fnt, fill=col)
    return 11 + draw.textlength(status, font=fnt)

def region_chip(draw, x, y, region, fnt):
    col = REGION[region][1]
    draw.rectangle([x, y, x + 9, y + 9], fill=col)
    return 12

# ---------------------------------------------------------------- scenes
def _stars(d, x0, y0, x1, y1, n, seed=7):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randint(x0 + 4, x1 - 4)
        y = rnd.randint(y0 + 4, y1 - 4)
        d.ellipse([x, y, x + 2, y + 2], fill=(240, 235, 210))

def _dashed(d, p0, p1, fill, width=2, dash=5, gap=4):
    x0, y0, x1, y1 = p0[0], p0[1], p1[0], p1[1]
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    steps = int(L // (dash + gap))
    for i in range(steps + 1):
        t0 = i * (dash + gap) / L
        t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=fill, width=width)

def scene_nightsea(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(16, 44, 52))
    _stars(d, x0, y0, x1, y0 + int(h * 0.45), 14)
    d.ellipse([x1 - 34, y0 + 8, x1 - 12, y0 + 30], fill=(238, 222, 170))
    sea = y0 + int(h * 0.62)
    d.rectangle([x0, sea, x1, y1], fill=(24, 68, 80))
    for yy in range(sea + 6, y1 - 4, 9):
        d.line([(x0 + 6, yy), (x0 + 26, yy)], fill=(120, 170, 180), width=1)
        d.line([(x1 - 46, yy + 4), (x1 - 20, yy + 4)], fill=(120, 170, 180), width=1)
    # seven naval drones converging on the ship
    sx, sy = x0 + int(w * 0.52), sea + 6
    for i, (dx, dy) in enumerate([(-70, -38), (-46, -48), (-20, -52), (8, -50), (34, -40), (58, -28), (-58, -18)]):
        px, py = sx + dx, sy + dy
        _dashed(d, (px, py), (sx, sy), (220, 200, 140), width=1, dash=3, gap=3)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 220, 150))
    # corvette silhouette
    d.polygon([(sx - 42, sy + 12), (sx + 46, sy + 12), (sx + 34, sy + 2),
               (sx + 12, sy + 2), (sx + 8, sy - 8), (sx - 6, sy - 8),
               (sx - 10, sy + 2), (sx - 34, sy + 2)], fill=(10, 12, 14))
    # blast star above the ship
    bx, by = sx + 30, sy - 16
    d.polygon([(bx, by - 12), (bx + 3, by - 3), (bx + 12, by), (bx + 3, by + 3),
               (bx, by + 12), (bx - 3, by + 3), (bx - 12, by), (bx - 3, by - 3)],
              fill=(235, 150, 40))

def scene_strait(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(226, 208, 168))
    d.polygon([(x0, y0 + int(h * 0.42)), (x1, y0 + int(h * 0.18)),
               (x1, y0 + int(h * 0.62)), (x0, y0 + int(h * 0.86))], fill=(52, 110, 140))
    d.polygon([(x0, y0 + int(h * 0.86)), (x1, y0 + int(h * 0.62)),
               (x1, y1), (x0, y1)], fill=(196, 172, 120))
    # red sun over the strait
    d.ellipse([x1 - 52, y0 + 6, x1 - 26, y0 + 32], fill=(190, 70, 44))
    # tanker silhouette crossing the strait
    tx, ty = x0 + int(w * 0.42), y0 + int(h * 0.48)
    d.polygon([(tx - 46, ty + 10), (tx + 50, ty + 10), (tx + 40, ty),
               (tx - 38, ty)], fill=(20, 22, 26))
    d.rectangle([tx - 6, ty - 12, tx + 8, ty], fill=(20, 22, 26))
    d.rectangle([tx + 14, ty - 8, tx + 24, ty], fill=(20, 22, 26))
    # dashed blockade line across the strait (kept clear of the top-left
    # corner, where the big number + label sit)
    _dashed(d, (x0 + int(w * 0.40), y0 + int(h * 0.38)), (x1 - 10, y0 + int(h * 0.16)),
            (179, 64, 42), width=2, dash=6, gap=5)

def scene_chipchart(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(16, 52, 44))
    for gx in range(x0 + 14, x1 - 8, 26):
        d.line([(gx, y0 + 8), (gx, y1 - 8)], fill=(30, 74, 64), width=1)
    for gy in range(y0 + 14, y1 - 8, 24):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(30, 74, 64), width=1)
    # chip
    cx, cy, cs = x0 + int(w * 0.16), y0 + int(h * 0.42), 46
    for i in range(4):
        px = cx + 8 + i * 11
        d.line([(px, cy - 8), (px, cy)], fill=(200, 210, 190), width=2)
        d.line([(px, cy + cs), (px, cy + cs + 8)], fill=(200, 210, 190), width=2)
    d.rectangle([cx, cy, cx + cs, cy + cs], fill=(110, 190, 90), outline=(30, 90, 40), width=2)
    d.rectangle([cx + 12, cy + 12, cx + cs - 12, cy + cs - 12], fill=(16, 52, 44))
    d.text((cx + 17, cy + 16), "NV", font=SANS_B(13), fill=(220, 235, 210))
    # rising chart line
    pts = [(x0 + int(w * 0.42), y0 + int(h * 0.72)), (x0 + int(w * 0.55), y0 + int(h * 0.60)),
           (x0 + int(w * 0.66), y0 + int(h * 0.64)), (x0 + int(w * 0.78), y0 + int(h * 0.42)),
           (x0 + int(w * 0.90), y0 + int(h * 0.24))]
    d.line(pts, fill=(240, 235, 210), width=3, joint="curve")
    for px, py in pts[1:]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 235, 210))

def scene_climate(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(238, 226, 196))
    d.ellipse([x1 - int(w * 0.20), y0 + 1, x1 - int(w * 0.04), y0 + int(h * 0.38)],
              fill=(235, 170, 60))
    # mountain + sea (peak near the top so the panel reads as a scene)
    d.polygon([(x0 + 4, y1), (x0 + int(w * 0.40), y0 + int(h * 0.08)),
               (x0 + int(w * 0.74), y1)], fill=(110, 140, 96))
    d.polygon([(x0 + int(w * 0.40), y0 + int(h * 0.08)), (x0 + int(w * 0.52), y0 + int(h * 0.34)),
               (x0 + int(w * 0.30), y0 + int(h * 0.34))], fill=(250, 248, 240))
    d.polygon([(x0 + int(w * 0.60), y1), (x0 + int(w * 0.82), y0 + int(h * 0.42)),
               (x1 - 2, y1)], fill=(90, 118, 80))
    d.rectangle([x0, y1 - int(h * 0.20), x1, y1], fill=(120, 160, 170))
    # thermometer
    tx = x0 + int(w * 0.78)
    d.rounded_rectangle([tx, y0 + int(h * 0.16), tx + 10, y1 - int(h * 0.30)],
                        radius=5, fill=(252, 248, 238), outline=(90, 80, 66), width=2)
    d.rectangle([tx + 2, y0 + int(h * 0.55), tx + 8, y1 - int(h * 0.32)],
                fill=(190, 70, 44))
    d.ellipse([tx - 3, y1 - int(h * 0.38), tx + 13, y1 - int(h * 0.14)],
              fill=(190, 70, 44))

def scene_drones(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(18, 38, 54))
    _stars(d, x0, y0, x1, y0 + int(h * 0.5), 10, seed=11)
    # city blocks with lit windows
    base = y1 - 4
    for i, (bx, bw, bh) in enumerate([(8, 30, 22), (44, 24, 34), (74, 30, 18), (110, 26, 30),
                                      (142, 30, 22), (176, 26, 36), (208, 24, 20)]):
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(10, 14, 18))
        for wy in range(base - bh + 5, base - 4, 8):
            for wx in range(x0 + bx + 5, x0 + bx + bw - 4, 9):
                if (wx + wy) % 17 < 8:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 210, 120))
    # drone swarm dots + one blast
    for dx, dy in [(30, 14), (70, 8), (110, 18), (150, 10), (190, 20), (220, 12)]:
        d.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2], fill=(240, 220, 150))
    bx, by = x0 + 130, y0 + 34
    d.polygon([(bx, by - 9), (bx + 2, by - 2), (bx + 9, by), (bx + 2, by + 2),
               (bx, by + 9), (bx - 2, by + 2), (bx - 9, by), (bx - 2, by - 2)],
              fill=(235, 150, 40))

def scene_awacs(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(168, 196, 212))
    d.ellipse([x0 + 10, y0 + 8, x0 + 60, y0 + 22], fill=(235, 240, 242))
    d.ellipse([x0 + 150, y0 + 14, x0 + 210, y0 + 26], fill=(235, 240, 242))
    d.ellipse([x0 + 90, y0 + 2, x0 + 130, y0 + 12], fill=(225, 232, 234))
    # AWACS silhouette: fuselage + radar dome + tail
    cx, cy = x0 + int(w * 0.5), y0 + int(h * 0.58)
    d.polygon([(cx - 88, cy + 7), (cx + 88, cy + 7), (cx + 78, cy - 7),
               (cx - 78, cy - 7)], fill=(40, 44, 50))
    d.polygon([(cx + 62, cy - 7), (cx + 84, cy - 26), (cx + 70, cy - 7)], fill=(40, 44, 50))
    d.ellipse([cx - 18, cy - 24, cx + 18, cy - 4], fill=(52, 58, 66))
    d.line([(cx - 18, cy - 14), (cx + 18, cy - 14)], fill=(40, 44, 50), width=2)
    _dashed(d, (x0 + 8, y1 - 10), (x1 - 8, y1 - 14), (120, 140, 150), width=1, dash=4, gap=4)

def scene_sanctions(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(52, 88, 138))
    cx, cy, r = x0 + int(w * 0.28), y0 + int(h * 0.50), max(12, int(h * 0.34))
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        k = max(2, int(h * 0.07))
        d.polygon([(sx, sy - k), (sx + 1, sy - 1), (sx + k, sy), (sx + 1, sy + 1),
                   (sx, sy + k), (sx - 1, sy + 1), (sx - k, sy), (sx - 1, sy - 1)],
                  fill=(240, 210, 110))
    # document
    dx = x0 + int(w * 0.58)
    d.rectangle([dx, y0 + int(h * 0.18), dx + 66, y1 - int(h * 0.18)],
                fill=(252, 248, 238), outline=(30, 40, 60), width=2)
    for i, yy in enumerate(range(y0 + int(h * 0.38), y1 - int(h * 0.22), max(6, int(h * 0.14)))):
        ln = 50 if i % 2 == 0 else 38
        d.line([(dx + 8, yy), (dx + 8 + ln, yy)], fill=(90, 90, 90), width=2)
    d.rectangle([dx + 8, y0 + int(h * 0.22), dx + 22, y0 + int(h * 0.34)],
                fill=(179, 64, 42))

def scene_capitol(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(214, 224, 226))
    d.rectangle([x0, y1 - int(h * 0.18), x1, y1], fill=(120, 140, 120))
    cx = x0 + int(w * 0.5)
    # dome + wings
    d.rectangle([x0 + 16, y1 - int(h * 0.62), x0 + 52, y1 - int(h * 0.18)],
                fill=(250, 248, 240))
    d.rectangle([x1 - 52, y1 - int(h * 0.62), x1 - 16, y1 - int(h * 0.18)],
                fill=(250, 248, 240))
    d.rectangle([cx - 34, y1 - int(h * 0.72), cx + 34, y1 - int(h * 0.18)],
                fill=(244, 240, 230))
    d.pieslice([cx - 30, y1 - int(h * 0.98), cx + 30, y1 - int(h * 0.42)],
               180, 360, fill=(244, 240, 230))
    d.rectangle([cx - 3, y1 - int(h * 1.06), cx + 3, y1 - int(h * 0.96)],
                fill=(90, 90, 90))
    for xx in range(cx - 28, cx + 29, 10):
        d.line([(xx, y1 - int(h * 0.64)), (xx, y1 - int(h * 0.22))],
               fill=(160, 150, 130), width=2)
    for xx in (x0 + 24, x0 + 34, x0 + 44, x1 - 44, x1 - 34, x1 - 24):
        d.line([(xx, y1 - int(h * 0.54)), (xx, y1 - int(h * 0.22))],
               fill=(160, 150, 130), width=2)

def scene_diplomacy(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(232, 220, 196))
    # two flags facing each other
    for fx, col in [(x0 + 22, (190, 60, 44)), (x1 - 62, (52, 96, 140))]:
        d.line([(fx, y0 + 10), (fx, y1 - 12)], fill=(90, 80, 66), width=2)
        d.polygon([(fx, y0 + 10), (fx + 40, y0 + 16), (fx, y0 + 24)], fill=col)
    # document in the middle
    dx = x0 + int(w * 0.38)
    d.rectangle([dx, y0 + 14, dx + 62, y1 - 12], fill=(252, 248, 238),
                outline=(90, 80, 66), width=2)
    for yy in range(y0 + 24, y1 - 20, 7):
        d.line([(dx + 8, yy), (dx + 54, yy)], fill=(120, 112, 96), width=2)
    d.polygon([(dx + 24, y1 - 22), (dx + 38, y1 - 22), (dx + 31, y1 - 12)], fill=(179, 64, 42))

def scene_podium(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(226, 214, 190))
    # two red-white flags
    for fx in (x0 + 26, x1 - 58):
        d.line([(fx, y0 + 8), (fx, y1 - 14)], fill=(90, 80, 66), width=2)
        d.rectangle([fx, y0 + 8, fx + 32, y0 + 16], fill=(200, 50, 44))
        d.rectangle([fx, y0 + 16, fx + 32, y0 + 24], fill=(250, 248, 240))
    # podium with two name plates
    cx = x0 + int(w * 0.5)
    d.rectangle([cx - 52, y1 - 34, cx + 52, y1 - 8], fill=(90, 66, 44))
    d.rectangle([cx - 52, y1 - 40, cx + 52, y1 - 34], fill=(60, 44, 30))
    d.rectangle([cx - 44, y1 - 28, cx - 6, y1 - 14], fill=(252, 248, 238))
    d.rectangle([cx + 6, y1 - 28, cx + 44, y1 - 14], fill=(252, 248, 238))
    d.line([(cx - 40, y1 - 21), (cx - 10, y1 - 21)], fill=(120, 110, 96), width=2)
    d.line([(cx + 10, y1 - 21), (cx + 40, y1 - 21)], fill=(120, 110, 96), width=2)

def scene_fire(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(40, 36, 34))
    d.ellipse([x0 + int(w * 0.62), y0 + int(h * 0.06), x0 + int(w * 0.74), y0 + int(h * 0.42)],
              fill=(120, 120, 120))
    d.ellipse([x0 + int(w * 0.70), y0 + int(h * 0.20), x0 + int(w * 0.82), y0 + int(h * 0.56)],
              fill=(100, 100, 100))
    # factory block
    d.rectangle([x0 + 14, y1 - int(h * 0.55), x1 - 14, y1 - int(h * 0.14)],
                fill=(70, 62, 56))
    d.rectangle([x0 + 14, y1 - int(h * 0.72), x0 + 70, y1 - int(h * 0.55)],
                fill=(70, 62, 56))
    d.rectangle([x1 - 46, y1 - int(h * 0.95), x1 - 34, y1 - int(h * 0.55)],
                fill=(70, 62, 56))
    # flames
    fx = x0 + int(w * 0.42)
    d.polygon([(fx - 26, y1 - int(h * 0.55)), (fx - 12, y1 - int(h * 0.98)),
               (fx - 2, y1 - int(h * 0.72)), (fx + 10, y1 - h),
               (fx + 22, y1 - int(h * 0.72)), (fx + 30, y1 - int(h * 0.55))],
              fill=(235, 150, 40))
    d.polygon([(fx - 12, y1 - int(h * 0.55)), (fx - 4, y1 - int(h * 0.82)),
               (fx + 4, y1 - int(h * 0.68)), (fx + 12, y1 - int(h * 0.85)),
               (fx + 16, y1 - int(h * 0.55))], fill=(240, 200, 80))
    for xx in range(x0 + 22, x1 - 20, 18):
        d.rectangle([xx, y1 - int(h * 0.45), xx + 8, y1 - int(h * 0.25)],
                    fill=(240, 200, 90))

SCENES = {
    "nightsea": scene_nightsea, "strait": scene_strait, "chipchart": scene_chipchart,
    "climate": scene_climate, "drones": scene_drones, "awacs": scene_awacs,
    "sanctions": scene_sanctions, "capitol": scene_capitol, "diplomacy": scene_diplomacy,
    "podium": scene_podium, "fire": scene_fire,
}

def grid_illustration(d, box, scene, big, biglabel):
    """Grid illustration: scene fills the box; a calm solid band over the
    bottom holds the one big number + its label (never over the objects)."""
    x0, y0, x1, y1 = box
    band = 18
    SCENES[scene](d, (x0, y0, x1, y1))
    d.rectangle([x0, y1 - band, x1, y1], fill=TEAL)
    d.text((x0 + 6, y1 - band + 2), big, font=SANS_B(13), fill=(255, 255, 255))
    bw = d.textlength(big, font=SANS_B(13))
    d.text((x0 + 10 + bw, y1 - band + 5), biglabel, font=SANS_B(8), fill=(200, 220, 214))

# ---------------------------------------------------------------- map
# Coarse continent outlines (lon, lat), drawn from general geography.
POLYS = [
    # North America
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 57), (-130, 54),
     (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
     (-97, 16), (-92, 15), (-86, 12), (-83, 9), (-80, 8), (-77, 7), (-79, 9),
     (-82, 13), (-87, 13), (-90, 14), (-92, 15), (-94, 17), (-97, 19),
     (-97, 22), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26),
     (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 44), (-65, 44),
     (-60, 47), (-55, 47), (-53, 50), (-56, 52), (-60, 55), (-65, 58),
     (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-90, 68), (-95, 69),
     (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    # Greenland
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76),
     (-35, 78), (-50, 76), (-58, 74), (-55, 70), (-52, 64), (-48, 61)],
    # South America
    [(-77, 7), (-72, 12), (-64, 11), (-60, 8), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-52, -33), (-58, -38),
     (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-74, -53), (-73, -45),
     (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-80, -6), (-81, -3),
     (-80, 1), (-77, 4)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (25, 32), (30, 31), (33, 27), (35, 23), (37, 18),
     (39, 15), (43, 12), (48, 11), (51, 10), (46, 5), (41, 1), (40, -5),
     (39, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32),
     (15, -27), (13, -18), (12, -10), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 12)],
    # Eurasia
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 55), (10, 57), (12, 56), (18, 56), (21, 55), (24, 58),
     (28, 60), (30, 62), (32, 66), (35, 68), (40, 68), (45, 68), (50, 69),
     (55, 68), (60, 69), (65, 69), (70, 70), (75, 72), (80, 73), (85, 74),
     (90, 75), (95, 76), (100, 77), (105, 78), (110, 76), (115, 73), (120, 72),
     (125, 71), (130, 71), (135, 71), (140, 72), (145, 72), (150, 70),
     (155, 69), (158, 66), (162, 62), (160, 58), (156, 52), (150, 59),
     (142, 55), (140, 50), (138, 46), (135, 42), (130, 42), (127, 40),
     (126, 38), (122, 38), (120, 35), (122, 31), (120, 28), (118, 25),
     (112, 22), (108, 20), (105, 18), (103, 16), (100, 14), (98, 10),
     (97, 8), (94, 16), (92, 21), (89, 22), (86, 20), (82, 17), (80, 15),
     (77, 8), (76, 10), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26),
     (56, 27), (52, 28), (50, 29), (48, 30), (47, 30), (44, 29), (43, 26),
     (42, 25), (40, 24), (39, 21), (38, 18), (35, 18), (33, 20), (32, 22),
     (30, 24), (28, 25), (26, 27), (24, 29), (22, 31), (20, 32), (18, 34),
     (15, 36), (12, 38), (10, 38), (8, 39), (5, 38), (3, 37), (0, 36),
     (-2, 37), (-6, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (142, 42), (144, 44), (142, 45), (140, 41), (138, 38), (136, 36),
     (133, 35), (131, 33)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -15), (135, -12), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (178, -37), (176, -40),
     (173, -41), (170, -43)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -25), (43, -21)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-22, 65)],
]

def _project(box, lon, lat):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (78.0 - lat) / 136.0 * (y1 - y0)
    return (x, y)

def draw_map(d, box):
    d.rectangle(box, fill=(233, 238, 236), outline=RULE, width=1)
    for poly in POLYS:
        pts = [_project(box, lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=SAGE, outline=SAGE_DK)
    # island dots too small for polygons
    for lon, lat in [(114, 0), (102, -2), (110, -7), (141, -4), (96, -2),
                     (103, 1), (121, -1), (126, -5), (131, -3), (139, -5)]:
        x, y = _project(box, lon, lat)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=SAGE, outline=SAGE_DK)

def region_of(n):
    for lst, reg in [(LEADS, None), (GRID, None)]:
        for row in lst:
            if row[0] == n:
                return row[3]
    for row in LIST:
        if row[0] == n:
            return row[3]
    return "WORLD"

def draw_pins(d, box):
    positions = {}
    for n, (lon, lat, dx, dy) in sorted(PINS.items()):
        bx, by = _project(box, lon, lat)
        x, y = bx + dx, by + dy
        positions[n] = (x, y)
        if dx or dy:
            d.line([(bx, by), (x, y)], fill=(140, 130, 110), width=1)
        reg = region_of(n)
        col = REGION[reg][1]
        r = 7
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255),
                  outline=col, width=2)
        s = str(n)
        f = SANS_B(8 if n < 10 else 7)
        tw = d.textlength(s, font=f)
        d.text((x - tw / 2, y - 5 if n < 10 else -5 + y), s, font=f, fill=INK)
    return positions

# ---------------------------------------------------------------- page
def fit_serif(text, start, maxw):
    size = start
    while size > 20:
        f = SERIF_B(size)
        if ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(text, font=f) <= maxw:
            return f, size
        size -= 1
    return SERIF_B(size), size

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M

    # ---- kicker bar
    text(d, (x0, 8), "THE MAP THAT MONDAY MADE", SANS_B(13), INK)
    rt = "PRESS TIME 24:00 UTC"
    text(d, (x1 - d.textlength(rt, font=SANS_B(13)), 8), rt, SANS_B(13), BRICK)
    hline(d, x0, x1, 28, fill=INK, width=2)

    # ---- date: largest text on the page
    date_s = "MONDAY 23 NOVEMBER 2026"
    df, dsize = fit_serif(date_s, 56, CW)
    text(d, (x0, 32), date_s, df, INK)
    date_h = dsize + 6

    # ---- tension subhead
    ty = 32 + date_h + 2
    text(d, (x0, ty), "War spreads to a new sea. A blockade tightens. A CEO comes back.",
         SERIF_I(17), BRICK)

    # ---- counts bar
    cy = ty + 26
    text(d, (x0, cy), "41 STORIES  ·  7 REGIONS  ·  15 FIELDS  ·  ALL DATED MONDAY 23 NOVEMBER 2026",
         SANS_B(12), INK)
    cx = x1
    for reg, cnt in reversed(COUNTS):
        lab = "%s %d" % (reg, cnt)
        wlab = d.textlength(lab, font=SANS_B(11))
        cx -= wlab + 12
        d.rectangle([cx, cy + 1, cx + 9, cy + 10], fill=REGION[reg][1])
        text(d, (cx + 11, cy), lab, SANS_B(11), INK)
        cx -= 8
    hline(d, x0, x1, cy + 20, fill=RULE, width=1)

    # ---- UTC strip: 6 event cells + press-time end cell, one line per label
    uy = cy + 28
    text(d, (x0, uy), "THE DAY IN UTC", SANS_B(11), MUTED)
    cell_w = CW / 7.0
    hline(d, x0, x1, uy + 20, fill=INK, width=2)
    for i, (t, lab, n) in enumerate(UTC):
        ccx = x0 + i * cell_w
        d.ellipse([ccx + cell_w / 2 - 3, uy + 17, ccx + cell_w / 2 + 3, uy + 23],
                  fill=TEAL)
        text(d, (ccx + 6, uy + 26), t, SANS_B(14), TEAL)
        text(d, (ccx + 6, uy + 44), lab, SANS_B(11), INK)
    ccx = x0 + 6 * cell_w
    d.ellipse([ccx + cell_w / 2 - 3, uy + 17, ccx + cell_w / 2 + 3, uy + 23], fill=BRICK)
    text(d, (ccx + 6, uy + 26), "24:00", SANS_B(14), BRICK)
    text(d, (ccx + 6, uy + 44), "PRESS TIME", SANS_B(11), BRICK)
    strip_bottom = uy + 60

    # ---- numbers ribbon
    ry = strip_bottom + 6
    rh = 64
    d.rectangle([x0, ry, x1, ry + rh], fill=TEAL)
    for i, (big, lab, contra, n) in enumerate(RIBBON):
        ccx = x0 + i * (CW / 6.0)
        text(d, (ccx + 8, ry + 6), big, SANS_B(27), (255, 255, 255))
        tag = "#%d" % n
        text(d, (ccx + CW / 6.0 - 26, ry + 8), tag, SANS_B(10), (150, 175, 168))
        text(d, (ccx + 8, ry + 36), lab, SANS_B(10), (208, 224, 218))
        text(d, (ccx + 8, ry + 50), contra, SANS(10), (168, 190, 184))
        if i:
            d.line([(ccx, ry + 8), (ccx, ry + rh - 8)], fill=(40, 84, 78), width=1)

    # ---- three equal leads
    ly = ry + rh + 8
    lw = [325, 325, 326]
    lx = [x0, x0 + 325 + GAP, x0 + 325 + GAP + 325 + GAP]
    ill_h = 132
    for k, lead in enumerate(LEADS):
        n, place, field, reg, status, title, deck, big, biglab, scene = lead
        bx0, bx1 = lx[k], lx[k] + lw[k]
        d.rectangle([bx0, ly, bx1, ly + 244], fill=CREAM, outline=(200, 190, 170), width=1)
        SCENES[scene](d, (bx0 + 1, ly + 1, bx1 - 1, ly + ill_h))
        # one big number baked into a calm patch of the illustration
        if scene == "nightsea":
            text(d, (bx0 + 12, ly + 8), big, SANS_B(34), (240, 220, 150))
            text(d, (bx0 + 12, ly + 46), biglab, SANS_B(9), (240, 220, 150))
        elif scene == "strait":
            text(d, (bx0 + 12, ly + 8), big, SANS_B(34), INK)
            text(d, (bx0 + 12, ly + 46), biglab, SANS_B(9), INK)
        else:
            text(d, (bx0 + 12, ly + 8), big, SANS_B(30), (240, 235, 210))
            text(d, (bx0 + 12, ly + 42), biglab, SANS_B(9), (240, 235, 210))
        ty2 = ly + ill_h + 8
        region_chip(d, bx0 + 8, ty2 + 1, reg, SANS_B(10))
        kick = "%d  ·  %s  ·  %s" % (n, place, field)
        text(d, (bx0 + 22, ty2), kick, SANS_B(10), INK)
        tlines = wrap(d, title, SERIF_B(19), lw[k] - 16)
        yy = ty2 + 18
        for ln in tlines[:3]:
            text(d, (bx0 + 8, yy), ln, SERIF_B(19), INK)
            yy += 23
        dlines = wrap(d, deck, SANS(12), lw[k] - 16)
        for ln in dlines[:2]:
            text(d, (bx0 + 8, yy + 2), ln, SANS(12), (60, 56, 48))
            yy += 15
        status_chip(d, bx0 + 8, yy + 2, status, SANS_B(11))

    # ---- grid: 8 cards, 4 x 2
    gy = ly + 244 + 8
    gw = (CW - 3 * GAP) // 4
    gh = 112
    for idx, card in enumerate(GRID):
        n, place, field, reg, status, title, big, biglab, scene = card
        row, col = divmod(idx, 4)
        bx0 = x0 + col * (gw + GAP)
        by0 = gy + row * (gh + GAP)
        bx1, by1 = bx0 + gw, by0 + gh
        bg = CREAM if (row + col) % 2 == 0 else (238, 234, 220)
        d.rectangle([bx0, by0, bx1, by1], fill=bg, outline=(200, 190, 170), width=1)
        grid_illustration(d, (bx0 + 1, by0 + 1, bx1 - 1, by0 + 44), scene, big, biglab)
        ty3 = by0 + 50
        region_chip(d, bx0 + 6, ty3 + 1, reg, SANS_B(9))
        kick = "%d  ·  %s  ·  %s" % (n, place, field)
        text(d, (bx0 + 19, ty3), kick, SANS_B(9), INK)
        tlines = wrap(d, title, SANS_B(12), gw - 12)
        yy = ty3 + 13
        for ln in tlines[:2]:
            text(d, (bx0 + 6, yy), ln, SANS_B(12), INK)
            yy += 14
        status_chip(d, bx0 + 6, by1 - 14, status, SANS_B(9))

    # ---- bottom: map (left) + numbered list (right)
    by = gy + 2 * gh + GAP + 8
    text(d, (x0, by), "WHERE IT HAPPENED", SANS_B(12), INK)
    map_box = (x0, by + 18, x0 + 400, by + 186)
    draw_map(d, map_box)
    draw_pins(d, map_box)
    text(d, (x0, by + 190), "Pins carry each story's number; colour = region. 18 orbits Mercury.",
         SANS(9), MUTED)

    lx0 = x0 + 400 + 8
    text(d, (lx0, by), "ALSO ON MONDAY — 30 MORE STORIES, NUMBERED AS ON THE MAP",
         SANS_B(12), INK)
    # legend at the head of the list (status used on every card)
    leg_y = by + 18
    lx_ = lx0
    for st, desc in [("CONFIRMED", "verified by 2+ sources"),
                     ("REPORTED", "single source"),
                     ("CLAIM", "one side's claim")]:
        col = STATUS[st]
        d.ellipse([lx_, leg_y + 2, lx_ + 7, leg_y + 9], fill=col)
        text(d, (lx_ + 10, leg_y), st, SANS_B(10), col)
        w1 = d.textlength(st, font=SANS_B(10))
        text(d, (lx_ + 13 + w1, leg_y), desc, SANS(10), MUTED)
        lx_ += 13 + w1 + d.textlength(desc, font=SANS(10)) + 18
    # list items, two columns of 15
    col_w = (x1 - lx0 - GAP) // 2
    iy = leg_y + 14
    for i, row in enumerate(LIST):
        n, title, place, reg, status = row
        col = i // 15
        r = i % 15
        ix = lx0 + col * (col_w + GAP)
        yy = iy + r * 11.5
        colr = REGION[reg][1]
        num = "%d." % n
        text(d, (ix, yy), num, SANS_B(10), colr)
        nx = ix + d.textlength(num, font=SANS_B(10)) + 4
        maxw = ix + col_w - 34 - nx
        t = title
        while d.textlength(t, font=SANS(10)) > maxw and len(t) > 4:
            t = t[:-2]
        if t != title:
            t = t.rstrip() + "…"
        text(d, (nx, yy), t, SANS(10), INK)
        lab = "· " + reg
        text(d, (ix + col_w - 34, yy), lab, SANS_B(10), colr)
        d.ellipse([ix + col_w - 8, yy + 2, ix + col_w - 1, yy + 9],
                  fill=STATUS[status])

    # ---- DATE CHECK: its own box, separate from everything else
    dy0, dy1 = 978, 1010
    d.rectangle([x0, dy0, x1, dy1], fill=CREAM, outline=TEAL, width=2)
    text(d, (x0 + 8, dy0 + 5), "DATE CHECK — ", SANS_B(11), TEAL)
    w0 = d.textlength("DATE CHECK — ", font=SANS_B(11))
    text(d, (x0 + 8 + w0, dy0 + 5),
         "Every story above is dated Monday 23 November 2026. Press time 24:00 UTC.",
         SANS(11), INK)
    text(d, (x0 + 8, dy0 + 21),
         "Left out (other days): COP31 collapse (Sun) · Nigeria boat toll (Fri–Sun) · Liverpool 4–0 Man Utd (Sat) · Lula runoff win (25 Oct) · Pakistan's first astronaut (7 Nov).",
         SANS(10), MUTED)

    # ---- footer
    text(d, (x0, 1012),
         "Sources: Reuters, AP, AFP, BBC, CNN, Al Jazeera, The Hindu, SCMP, ABC, NZ Herald, Vanguard, El Colombiano + official statements. Pictures and map drawn in code.",
         SANS(9), MUTED)
    return img

def main():
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)

if __name__ == "__main__":
    main()
