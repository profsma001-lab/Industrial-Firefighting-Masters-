# -*- coding: utf-8 -*-
"""Widgets and schematics for the IF 701 deck (part 1)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import (Canvas, TEXT, MUTED, DIM, LINE, EMBER, AMBER, RED, TEAL, BLUE,
                 VIOLET, PANEL, PANEL2, PAL, WHITE, font, fb)
from charts import Chart, ALPHA

# ---------------------------------------------------------------- utilities


def with_alpha(c, fn):
    lay = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fn(d, c.sc)
    c.img = Image.alpha_composite(c.img.convert("RGBA"), lay).convert("RGB")
    c.d = ImageDraw.Draw(c.img)


def srect(d, sc, x, y, w, h, fill=None, outline=None, width=1, r=0):
    box = [x * sc, y * sc, (x + w) * sc, (y + h) * sc]
    if r:
        d.rounded_rectangle(box, radius=r * sc, fill=fill, outline=outline, width=int(width * sc))
    else:
        d.rectangle(box, fill=fill, outline=outline, width=int(width * sc))


def flame_path(cx, base, w, h, seed=0, wobble=0.22, n=26):
    """Returns polygon points for an organic flame shape."""
    rng = np.random.default_rng(seed)
    left, right = [], []
    for i in range(n):
        t = i / (n - 1)
        y = base - t * h
        half = (w / 2) * (math.sin(math.pi * min(1, t * 1.08)) ** 0.65)
        half *= (1 - 0.55 * t) * (0.92 + 0.16 * math.sin(t * 9 + seed))
        left.append((cx - half, y))
        right.append((cx + half * (0.85 + 0.3 * math.sin(t * 7 + seed * 2)), y))
    top = (cx + math.sin(seed) * w * 0.06, base - h * (0.97 + 0.05 * math.cos(seed)))
    return left + [top] + right[::-1]


def draw_flame(c, cx, base, w, h, seed=0, glow=True):
    if glow:
        with_alpha(c, lambda d, sc: d.ellipse(
            [(cx - w * 1.6) * sc, (base - h * 1.1) * sc, (cx + w * 1.6) * sc, (base + h * 0.1) * sc],
            fill=EMBER + (16,)))
        c.img = c.img.filter(ImageFilter.GaussianBlur(1.2))
        c.d = ImageDraw.Draw(c.img)
    c.poly(flame_path(cx, base, w * 1.18, h, seed), fill=(196, 58, 12))
    c.poly(flame_path(cx, base + h * 0.03, w * 0.86, h * 0.82, seed + 1), fill=(246, 118, 20))
    c.poly(flame_path(cx, base + h * 0.05, w * 0.52, h * 0.58, seed + 2), fill=(255, 186, 54))
    c.poly(flame_path(cx, base + h * 0.07, w * 0.24, h * 0.32, seed + 3), fill=(255, 240, 190))


def smoke_fill(c, x, y, w, h, alpha=110, seed=1, color=(150, 160, 176), spread=0.5):
    """Soft turbulent smoke mass (smooth field, no streaking)."""
    sc = c.sc
    Wp, Hp = max(2, int(w * sc)), max(2, int(h * sc))
    gw, gh = 70, 40
    rng = np.random.default_rng(seed)
    small = rng.random((6, 12)).astype(np.float32)
    small = np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((gw, gh), Image.BICUBIC),
                       dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:gh, 0:gw]
    t = yy / (gh - 1.0)
    a = np.clip((0.95 - t) * 1.6 * (0.35 + small), 0, 1) ** 1.1 * alpha
    im = Image.fromarray(a.astype(np.uint8)).resize((Wp, Hp), Image.BICUBIC)
    col = Image.new("RGB", (Wp, Hp), color)
    c.img.paste(col, (int(x * sc), int(y * sc)), im)
    c.d = ImageDraw.Draw(c.img)
def person(c, x, y, h=78, color=(210, 220, 235), helmet=(255, 190, 40), pack=True, label=None):
    """Simple firefighter silhouette; y is the feet."""
    hd = h * 0.16
    c.ellipse(x - hd / 2, y - h, hd, hd, fill=color)
    c.arc(x - hd * 0.62, y - h * 1.02, hd * 1.24, hd * 0.9, 180, 360, fill=helmet, width=max(2, h * 0.035))
    c.rect(x - h * 0.12, y - h * 0.84, h * 0.24, h * 0.44, fill=color, r=h * 0.05)
    if pack:
        c.rect(x + h * 0.10, y - h * 0.80, h * 0.10, h * 0.30, fill=(120, 130, 145), r=3)
    c.line([(x - h * 0.04, y - h * 0.42), (x - h * 0.09, y)], fill=color, width=max(2, h * 0.07))
    c.line([(x + h * 0.05, y - h * 0.42), (x + h * 0.08, y)], fill=color, width=max(2, h * 0.07))
    if label:
        c.text(x, y + 10, label, size=12, color=MUTED, fname="Inter-Medium", anchor="ma")


def tag_chip(c, x, y, txt, color=EMBER, size=14, solid=False, pad=12):
    tw = c.text_width(txt, size, "Inter-SemiBold")
    c.rect(x, y, tw + pad * 2, size + 14, fill=color if solid else (color[0] // 7 + 10, color[1] // 8 + 14, color[2] // 8 + 20),
           outline=color, r=6, width=1)
    c.text(x + pad, y + (size + 14) / 2, txt, size=size,
           color=(15, 20, 30) if solid else color, fname="Inter-SemiBold", anchor="lm")


def dotted(c, pts, fill=LINE, width=1, dash=4, gap=4):
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1:
            continue
        n = int(L / (dash + gap)) + 1
        for k in range(n):
            t0 = k * (dash + gap) / L
            t1 = min(1, t0 + dash / L)
            if t0 >= 1:
                break
            c.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                    (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=fill, width=width)


def hatched(c, box, color=(60, 80, 110), step=8, width=1):
    x, y, w, h = box
    for i in range(int(-h), int(w), step):
        x1, y1 = x + i, y + h
        x2, y2 = x + i + h, y
        # clip roughly to box
        c.line([(max(x, x1), y + (y1 - (y + h)) if False else y1), (x2, y2)], fill=color, width=width)


# ---------------------------------------------------------------- widgets
def eq_card(c, title, eq, terms, x=None, y=None, w=None, h=None):
    x = 700 if x is None else x
    y = 190 if y is None else y
    w = w or 1080
    h = h or 760
    c.panel(x, y, w, h, fill=(13, 19, 31), outline=(40, 54, 78), r=18)
    c.rect(x, y, 5, h, fill=EMBER)
    c.text(x + 44, y + 42, title.upper(), size=15, color=(255, 152, 92), fname="Inter-SemiBold", track=1.5)
    c.text(x + w / 2, y + h * 0.34, eq, size=64, color=TEXT, fname="Serif-Regular", anchor="mm")
    c.line([(x + 60, y + h * 0.50), (x + w - 60, y + h * 0.50)], fill=(40, 54, 78), width=1)
    ty = y + h * 0.56
    for t in terms:
        c.text(x + 60, ty, "—", size=20, color=EMBER, fname="Inter-Regular", anchor="lm")
        _, hh = c.text(x + 92, ty, t, size=22, color=MUTED, fname="Inter-Regular", maxw=w - 150, spacing=1.3)
        ty += max(38, hh + 14)


def table(c, x, y, w, rows, cols, colw=None, h=None, size=19, header=True, header_color=AMBER,
          row_h=None, zebra=True, align=None, color=TEXT, head_size=15, key_col_color=None):
    n = len(rows)
    colw = colw or [w / len(cols)] * len(cols)
    row_h = row_h or min(82, ((h - 48) / n) if h else 52)
    hy = y
    if header:
        c.rect(x, y, w, 40, fill=(24, 33, 50), r=6)
        cx = x + 16
        for i, col in enumerate(cols):
            c.text(cx, y + 20, col.upper(), size=head_size, color=header_color, fname="Inter-SemiBold",
                   track=1.1, anchor="lm")
            cx += colw[i]
        hy = y + 44
    for r, row in enumerate(rows):
        ry = hy + r * row_h
        if zebra and r % 2 == 1:
            c.rect(x, ry, w, row_h - 2, fill=(16, 23, 36), r=4)
        cx = x + 16
        for i, cell in enumerate(row):
            bold = i == 0
            c.text(cx, ry + row_h / 2 - 1, str(cell), size=size,
                   color=(key_col_color if (bold and key_col_color) else color),
                   fname="Inter-SemiBold" if bold else "Inter-Regular",
                   anchor="lm", maxw=colw[i] - 18, spacing=1.2)
            cx += colw[i]
    c.line([(x, hy - 2), (x + w, hy - 2)], fill=(40, 54, 78), width=1)


def cards(c, x, y, w, h, items, gap=20, title_size=15, body_size=19, accent=EMBER):
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, (title, body) in enumerate(items):
        cx = x + i * (cw + gap)
        c.panel(cx, y, cw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.rect(cx, y, cw, 3, fill=accent)
        c.text(cx + 22, y + 32, title.upper(), size=title_size, color=accent, fname="Inter-SemiBold", track=1.2)
        c.text(cx + 22, y + 62, body, size=body_size, color=TEXT, fname="Inter-Regular", maxw=cw - 44, spacing=1.35)


def key_figures(c, x, y, w, h, items):
    cw, ch = (w - 24) / 2, (h - 24) / 2
    for i, (num, lab, col) in enumerate(items):
        cx = x + (i % 2) * (cw + 24)
        cy = y + (i // 2) * (ch + 24)
        c.panel(cx, cy, cw, ch, fill=(15, 22, 35), outline=(38, 52, 76), r=12)
        c.text(cx + 28, cy + ch * 0.42, num, size=58, color=PAL.get(col, EMBER),
               fname="Serif-Bold", anchor="lm")
        c.text(cx + 28, cy + ch * 0.72, lab, size=17, color=MUTED, fname="Inter-Regular",
               maxw=cw - 56, spacing=1.3)


def process_ring(c, x, y, w, h, items):
    cx, cy = x + w / 2, y + h / 2
    rx, ry = w * 0.33, h * 0.36
    n = len(items)
    cols = [EMBER, AMBER, TEAL, BLUE, VIOLET, RED]
    for i in range(n):
        a0 = -math.pi / 2 + i * 2 * math.pi / n
        a1 = a0 + 2 * math.pi / n
        col = cols[i % len(cols)]
        c.arc(cx - rx, cy - ry, 2 * rx, 2 * ry, math.degrees(a0) + 6, math.degrees(a1) - 6,
              fill=(52, 68, 94), width=3)
    for i, it in enumerate(items):
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / n
        px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
        col = cols[i % len(cols)]
        c.ellipse(px - 7, py - 7, 14, 14, fill=col)
        tx = cx + (rx + 46) * math.cos(a)
        ty = cy + (ry + 42) * math.sin(a)
        anchor = "mm"
        c.text(tx, ty, it, size=18, color=TEXT, fname="Inter-Medium", anchor=anchor, maxw=190, spacing=1.2)
    c.text(cx, cy - 12, "FIRE", size=30, color=TEXT, fname="Serif-Bold", anchor="mm")
    c.text(cx, cy + 20, "as a system", size=15, color=MUTED, fname="Inter-Medium", anchor="mm")


def compare_panels(c, x, y, w, h, left, right):
    cw = (w - 24) / 2
    for i, (title, items) in enumerate([left, right]):
        col = MUTED if i == 0 else EMBER
        cx = x + i * (cw + 24)
        c.panel(cx, y, cw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.text(cx + 24, y + 20, title, size=14, color=col, fname="Inter-SemiBold", track=1.4, anchor="la")
        cy = y + 62
        for it in items:
            c.rect(cx + 24, cy + 9, 6, 6, fill=col, r=1)
            _, hh = c.text(cx + 42, cy, it, size=19, color=TEXT, fname="Inter-Regular", maxw=cw - 66, spacing=1.25)
            cy += hh + 16


def compare_units(c, x, y, w, h, rows):
    row_h = h / (len(rows) + 1)
    heads = ["QUANTITY", "UNIT", "MEANING"]
    cw = [w * 0.26, w * 0.16, w * 0.58]
    cx = x
    for i, hd in enumerate(heads):
        c.text(cx + 8, y, hd, size=13, color=AMBER, fname="Inter-SemiBold", track=1.2, anchor="la")
        cx += cw[i]
    c.line([(x, y + 24), (x + w, y + 24)], fill=(44, 58, 82), width=1)
    for r, (a, b, cc) in enumerate(rows):
        ry = y + 24 + r * row_h
        c.rect(x, ry + 4, w, row_h - 8, fill=(15, 22, 35) if r % 2 == 0 else (13, 19, 30), r=6)
        c.text(x + 8, ry + row_h / 2, a, size=20, color=TEXT, fname="Inter-SemiBold", anchor="lm")
        c.text(x + cw[0] + 8, ry + row_h / 2, b, size=19, color=TEAL, fname="Mono-Regular", anchor="lm")
        c.text(x + cw[0] + cw[1] + 8, ry + row_h / 2, cc, size=17, color=MUTED, fname="Inter-Regular",
               anchor="lm", maxw=cw[2] - 20, spacing=1.2)


def def_cards(c, x, y, w, h, items):
    gap = 18
    cw = (w - gap * (len(items) - 1)) / len(items)
    for i, (t, body) in enumerate(items):
        cx = x + i * (cw + gap)
        c.panel(cx, y, cw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=14)
        c.rect(cx, y, cw, 4, fill=[EMBER, AMBER, TEAL][i % 3])
        c.text(cx + 24, y + 30, t, size=15, color=[EMBER, AMBER, TEAL][i % 3], fname="Inter-SemiBold", track=1.4)
        c.text(cx + 24, y + 64, body, size=20, color=TEXT, fname="Inter-Regular", maxw=cw - 48, spacing=1.42)


# ---------------------------------------------------------------- charts
def fire_stages_chart(c, x, y, w, h, progress=1.0, labels=True):
    ch = Chart(c, x, y, w, h, (0, 1200), (0, 1300), "TIME (s)", "GAS TEMPERATURE (°C)",
               xticks=[0, 200, 400, 600, 800, 1000, 1200],
               yticks=[0, 200, 400, 600, 800, 1000, 1200], yfmt=lambda v: f"{int(v):d}")
    def curve(t):
        if t < 120:
            base = 20 + 40 * (t / 120) ** 1.5
        elif t < 300:
            base = 60 + 340 * ((t - 120) / 180) ** 2.0
        elif t < 330:
            base = 400 + 560 * ((t - 300) / 30) ** 0.8
        elif t < 700:
            base = 960 + 180 * math.sin((t - 330) / 90) - 20 * (t - 330) / 370
        else:
            base = max(120, 1120 * math.exp(-(t - 700) / 210))
        return base
    ts = np.linspace(0, 1200, 400)
    ys = np.array([curve(t) for t in ts])
    ch.band(0, 120, (255, 176, 32), 16)
    ch.band(120, 330, (255, 107, 26), 16)
    ch.band(330, 700, (229, 72, 77), 18)
    ch.band(700, 1200, (76, 141, 255), 14)
    ch.area(ts, ys, EMBER, 34)
    n = max(2, int(len(ts) * progress))
    ch.line(ts[:n], ys[:n], EMBER, 3.2)
    if labels:
        for xv, lab, col in [(60, "INCIPIENT", AMBER), (225, "GROWTH", EMBER),
                             (515, "FULLY DEVELOPED", RED), (950, "DECAY", BLUE)]:
            c.text(ch.tx(xv), ch.py0 + 26, lab, size=15, color=col, fname="Inter-SemiBold", anchor="ma", track=1.2)
        ch.hline(600, RED, 1.2, 8, "FLASHOVER THRESHOLD  ~600 °C")
        ch.vline(330, (255, 255, 255), 1.2, 6, "FLASHOVER")
        ch.vline(700, (255, 255, 255), 1.0, 4)
        c.text(ch.tx(700) + 8, ch.ty(1250), "FUEL OR OXYGEN EXHAUSTED", size=12, color=MUTED,
               fname="Inter-Medium", anchor="lm")
    return ch


def alpha_chart(c, x, y, w, h, annotate=True):
    ch = Chart(c, x, y, w, h, (0, 600), (0, 14000), "TIME (min)", "HEAT RELEASE RATE (MW)",
               xticks=[0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600],
               yticks=[0, 2000, 4000, 6000, 8000, 10000, 12000, 14000],
               xfmt=lambda v: f"{v/60:.0f}" if v else "0",
               yfmt=lambda v: f"{v/1000:.0f}" if v else "0")
    cols = {"slow": BLUE, "medium": TEAL, "fast": AMBER, "ultrafast": RED}
    for k, a in ALPHA.items():
        ts = np.linspace(0, min(600, math.sqrt(14000 / a)), 200)
        ys = a * ts ** 2
        ch.line(ts, ys, cols[k], 2.6, label=k.upper())
    ch.hline(1055, (255, 255, 255), 1.4, 8, "1.0 MW")
    if annotate:
        ch.point(150, 1055, AMBER, 5, label="FAST: 150 s to 1 MW")
        ch.point(300, 1055, TEAL, 5, label="MEDIUM: 300 s to 1 MW")
        c.text(ch.tx(150), ch.ty(5600), "ULTRA-FAST", size=15, color=RED, fname="Inter-SemiBold")
        c.text(ch.tx(300), ch.ty(5400), "FAST", size=15, color=AMBER, fname="Inter-SemiBold")
        c.text(ch.tx(395), ch.ty(2600), "MEDIUM", size=15, color=TEAL, fname="Inter-SemiBold")
        c.text(ch.tx(380), ch.ty(1150), "SLOW", size=15, color=BLUE, fname="Inter-SemiBold")
    return ch


def hrr_bars(c, x, y, w, h):
    items = [("Candle", 0.05), ("Wastebasket", 0.1), ("Armchair", 0.3), ("Car", 3.0),
             ("Retail rack", 12.0), ("Warehouse", 60.0), ("Tank fire (20 m)", 900.0)]
    n = len(items)
    row_h = h / n
    x0 = x + 210
    wmax = w - 260
    lo, hi = -1.7, 3.2  # log10 kW
    for i, (lab, val) in enumerate(items):
        yy = y + i * row_h
        lv = math.log10(val * 1000)
        bw = (lv - lo) / (hi - lo) * wmax
        col = [(120, 140, 170), (150, 160, 180), (255, 176, 32), (255, 140, 40),
               (255, 107, 26), (255, 80, 40), (229, 72, 77)][i]
        c.text(x0 - 14, yy + row_h / 2, lab, size=17, color=TEXT, fname="Inter-Regular", anchor="rm")
        c.rect(x0, yy + row_h * 0.28, wmax, row_h * 0.44, fill=(16, 23, 36), r=4)
        c.rect(x0, yy + row_h * 0.28, max(4, bw), row_h * 0.44, fill=col, r=4)
        unit = f"{val*1000:,.0f} kW" if val < 10 else f"{val:,.0f} MW"
        c.text(x0 + max(4, bw) + 12, yy + row_h / 2, unit, size=16, color=MUTED, fname="Mono-Regular", anchor="lm")
    for e in range(-1, 4):
        xx = x0 + (e - lo) / (hi - lo) * wmax
        c.line([(xx, y - 4), (xx, y + h)], fill=(34, 46, 66), width=1)
        sup = {0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴"}.get(e, str(e))
        c.text(xx, y + h + 16, "10" + sup, size=13, color=DIM, fname="Mono-Regular", anchor="ma")
    c.text(x0, y + h + 42, "LOG SCALE — HEAT RELEASE RATE (kW)", size=13, color=DIM,
           fname="Inter-Medium", track=1.0)
