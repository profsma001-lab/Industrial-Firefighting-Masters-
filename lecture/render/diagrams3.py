# -*- coding: utf-8 -*-
"""Remaining schematics, worked-example panels and case visuals."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import (Canvas, TEXT, MUTED, DIM, LINE, EMBER, AMBER, RED, TEAL, BLUE,
                 VIOLET, PANEL, PANEL2, PAL, WHITE)
from charts import Chart, ALPHA
from diagrams import (with_alpha, table, cards, tag_chip, person, draw_flame,
                      smoke_fill, srect, eq_card)
from diagrams2 import (room, layer, warehouse, hot_color, _grid_noise, CARDBOARD, PLASTIC, STEEL)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# ------------------------------------------------------------------ small data visuals


def fuel_classes(c, x, y, w, h):
    items = [("SOLID", "pyrolysis → vapour", ["timber", "cartons", "polymers", "rubber"], CARDBOARD),
             ("LIQUID", "evaporation → vapour", ["petrol", "diesel", "solvents", "oils"], (120, 90, 60)),
             ("GAS", "already a fuel", ["LPG", "methane", "hydrogen", "acetylene"], (70, 110, 140)),
             ("DUST", "suspension → cloud", ["flour", "sugar", "polyethylene", "coal"], (110, 110, 110))]
    cw = (w - 36) / 4
    for i, (t, mech, ex, col) in enumerate(items):
        cx = x + i * (cw + 12)
        c.panel(cx, y, cw, h, fill=(15, 22, 35), outline=(40, 54, 78), r=12)
        c.rect(cx, y, cw, 4, fill=col if i != 0 else CARDBOARD)
        c.text(cx + 16, y + 22, t, size=13, color=TEXT, fname="Inter-SemiBold", track=1.2)
        c.text(cx + 16, y + 44, mech, size=13, color=MUTED, fname="Inter-Regular", maxw=cw - 30)
        by = y + h * 0.42
        # icon
        if i == 0:
            c.rect(cx + cw * 0.28, by, cw * 0.44, h * 0.2, fill=(96, 72, 50), r=3)
            draw_flame(c, cx + cw * 0.5, by, cw * 0.14, h * 0.12, seed=2)
        elif i == 1:
            c.ellipse(cx + cw * 0.26, by + h * 0.12, cw * 0.48, h * 0.09, fill=(110, 88, 60))
            draw_flame(c, cx + cw * 0.5, by + h * 0.13, cw * 0.14, h * 0.11, seed=4)
        elif i == 2:
            c.rect(cx + cw * 0.34, by - 4, cw * 0.32, h * 0.22, fill=(60, 84, 106), r=8)
            c.rect(cx + cw * 0.42, by - 12, cw * 0.16, 8, fill=(80, 104, 128), r=3)
            c.text(cx + cw * 0.5, by + h * 0.13, "LPG", size=12, color=TEXT, fname="Mono-Bold", anchor="mm")
        else:
            for k in range(26):
                px = cx + cw * 0.24 + (k % 7) * cw * 0.075
                py = by + h * 0.06 + (k // 7) * h * 0.05
                c.ellipse(px, py, 3, 3, fill=(170, 150, 120))
        ty = y + h * 0.74
        for e in ex:
            c.text(cx + 16, ty, e, size=13, color=MUTED, fname="Inter-Regular")
            ty += 18


def oxygen_gauge(c, x, y, w, h):
    bar_y = y + h * 0.42
    bar_h = 46
    c.rect(x, bar_y, w, bar_h, fill=(18, 25, 38), r=8)
    zones = [(0, 0.14, (120, 40, 40)), (0.14, 0.16, (90, 60, 40)), (0.16, 0.21, (24, 46, 44)),
             (0.21, 0.235, (40, 52, 40)), (0.235, 0.26, (70, 44, 24))]
    for a, b, col in zones:
        c.rect(x + w * a, bar_y, w * (b - a), bar_h, fill=col)
    for pct, lab, col in [(0.14, "14%", RED), (0.21, "21%", TEAL), (0.235, "23.5%", AMBER)]:
        xx = x + w * pct
        c.line([(xx, bar_y - 8), (xx, bar_y + bar_h + 8)], fill=col, width=2)
        c.text(xx, bar_y + bar_h + 22, lab, size=14, color=col, fname="Mono-Bold", anchor="ma")
    c.text(x + w * 0.07, bar_y - 18, "NO FLAME", size=12, color=RED, fname="Inter-SemiBold", anchor="ma", track=0.8)
    c.text(x + w * 0.185, bar_y - 18, "AIR", size=12, color=TEAL, fname="Inter-SemiBold", anchor="ma", track=0.8)
    c.text(x + w * 0.245, bar_y - 18, "ENRICHED", size=12, color=AMBER, fname="Inter-SemiBold", anchor="ma", track=0.8)
    c.text(x, y, "OXYGEN CONCENTRATION BY VOLUME", size=12, color=MUTED, fname="Inter-SemiBold", track=1.1)
    c.text(x, bar_y + 62, "Below 14 % flaming stops — but smouldering continues at 5–8 %.\nAbove 23.5 % materials burn violently and ignition energy falls.",
           size=14, color=MUTED, fname="Inter-Regular", spacing=1.35, maxw=w)


def heat_path_trace(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    bx = x + 40
    bw = w - 80
    floor = y + h - 60
    # two racks
    for i, rx in enumerate([bx + bw * 0.18, bx + bw * 0.62]):
        c.rect(rx, y + 90, 26, floor - y - 90, fill=(96, 112, 136))
        c.rect(rx + 120, y + 90, 26, floor - y - 90, fill=(96, 112, 136))
        for t in range(4):
            ty = y + 120 + t * (floor - y - 160) / 4
            c.rect(rx + 26, ty, 94, 8, fill=(104, 120, 144))
            c.rect(rx + 30, ty - 26, 86, 24, fill=(146, 116, 78), r=2)
    draw_flame(c, bx + bw * 0.18 + 60, floor, 40, 90, seed=6)
    # ceiling layer
    layer(c, bx, y + 40, bw, floor - y - 60, 0.20, 0.5, seed=21)
    # arrows
    c.arrow(bx + bw * 0.18 + 70, floor - 100, bx + bw * 0.18 + 70, y + 70, fill=AMBER, width=2.4, head=10)
    tag_chip(c, bx + bw * 0.18 + 86, y + 96, "CONVECTION — plume to ceiling", AMBER, size=12)
    c.arrow(bx + bw * 0.18 + 90, y + 60, bx + bw * 0.55, y + 60, fill=(255, 150, 60), width=2, head=9)
    tag_chip(c, bx + bw * 0.40, y + 18, "CEILING JET spreads the layer", (255, 150, 60), size=12)
    c.arrow(bx + bw * 0.30, y + 120, bx + bw * 0.50, y + 200, fill=EMBER, width=2, head=9, dash=6)
    tag_chip(c, bx + bw * 0.40, y + 200, "RADIATION from the layer", EMBER, size=12)
    c.arrow(bx + bw * 0.60, y + 210, bx + bw * 0.30, y + 210, fill=EMBER, width=2, head=9, dash=6)
    c.arrow(bx + bw * 0.18 + 140, floor - 30, bx + bw * 0.60, floor - 30, fill=TEAL, width=2, head=9, dash=5)
    tag_chip(c, bx + bw * 0.36, floor - 62, "CONDUCTION through steel rack and floor", TEAL, size=12)
    c.text(bx, floor + 24, "Every mechanism suggests a different intervention: cool the layer, cool the steel, cool the exposure.",
           size=14, color=MUTED, fname="Inter-Regular")


def calorimetry(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(15, 22, 35), outline=(40, 54, 78), r=12)
    # exhaust hood
    hx, hy = x + w * 0.10, y + h * 0.16
    hw, hh = w * 0.34, h * 0.20
    c.poly([(hx + hw * 0.12, hy), (hx + hw * 0.88, hy), (hx + hw, hy + hh), (hx, hy + hh)],
           fill=(26, 36, 52), outline=(110, 126, 152), width=2)
    c.rect(hx + hw * 0.42, y + 8, hw * 0.16, hy - y - 4, fill=(26, 36, 52), outline=(110, 126, 152), width=2)
    for k in range(4):
        c.arrow(hx + hw * 0.5, hy + hh - 6, hx + hw * 0.5, hy + 8, fill=(150, 165, 185), width=2, head=9)
    tag_chip(c, hx + hw * 0.56, hy + 6, "EXHAUST DUCT", (150, 165, 185), size=11)
    # sample platform
    sy = y + h * 0.80
    c.rect(hx + hw * 0.34, sy, hw * 0.32, 14, fill=(120, 132, 150))
    c.rect(hx + hw * 0.38, sy - 16, hw * 0.24, 16, fill=CARDBOARD, r=2)
    draw_flame(c, hx + hw * 0.5, sy - 14, 26, h * 0.13, seed=9)
    # cone heater
    c.poly([(hx + hw * 0.30, sy - h * 0.20), (hx + hw * 0.70, sy - h * 0.20),
            (hx + hw * 0.62, sy - h * 0.06), (hx + hw * 0.38, sy - h * 0.06)], fill=(60, 30, 26),
           outline=(190, 90, 60), width=2)
    tag_chip(c, hx + hw * 0.72, sy - h * 0.18, "CONE HEATER  25–75 kW/m²", RED, size=11)
    c.text(hx, sy + 26, "SAMPLE  100 × 100 mm", size=12, color=MUTED, fname="Inter-Medium")
    # analyser
    ax = x + w * 0.62
    c.panel(ax, y + h * 0.20, w * 0.32, h * 0.30, fill=(19, 27, 41), outline=(50, 66, 92), r=8)
    c.text(ax + 18, y + h * 0.24, "O₂ ANALYSER", size=12, color=TEAL, fname="Inter-SemiBold", track=1.1)
    c.text(ax + 18, y + h * 0.30, "inlet   20.9 %", size=14, color=MUTED, fname="Mono-Regular")
    c.text(ax + 18, y + h * 0.35, "outlet  17.4 %", size=14, color=AMBER, fname="Mono-Regular")
    c.text(ax + 18, y + h * 0.40, "ΔO₂     3.5 %", size=14, color=TEXT, fname="Mono-Bold")
    c.line([(hx + hw * 0.92, hy + hh * 0.5), (ax, y + h * 0.33)], fill=(70, 86, 112), width=1.4)
    c.text(x + 24, y + h - 62, "13.1 MJ of energy is released per kg of oxygen consumed.", size=15,
           color=AMBER, fname="Inter-Medium")
    c.text(x + 24, y + h - 36, "HRR = 13.1 × (mass flow of air × oxygen depletion fraction)", size=15,
           color=MUTED, fname="Serif-Regular")


def scaling_tree(c, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    c.panel(cx - 130, cy - 52, 260, 104, fill=(40, 24, 18), outline=EMBER, r=12)
    c.text(cx, cy - 16, "HEAT RELEASE RATE", size=14, color=EMBER, fname="Inter-SemiBold", anchor="mm", track=1)
    c.text(cx, cy + 14, "Q  (kW)", size=26, color=TEXT, fname="Serif-Regular", anchor="mm")
    branches = [("FLAME LENGTH", "L ∝ Q^0.4", -1, -1, AMBER),
                ("PLUME MASS FLOW", "ṁ ∝ Q_c^0.33", 1, -1, TEAL),
                ("SMOKE PRODUCTION", "∝ Q × soot yield", 1, 1, (150, 160, 175)),
                ("RADIANT FLUX", "q″ ∝ Q / r²", -1, 1, RED)]
    for lab, form, sx, sy, col in branches:
        tx, ty = cx + sx * w * 0.26, cy + sy * h * 0.30
        c.panel(tx - 128, ty - 38, 256, 76, fill=(16, 23, 36), outline=(44, 58, 82), r=8)
        c.text(tx, ty - 10, lab, size=13, color=col, fname="Inter-SemiBold", anchor="mm", track=1)
        c.text(tx, ty + 16, form, size=17, color=TEXT, fname="Serif-Regular", anchor="mm")
        c.arrow(cx + sx * 132, cy + sy * 54, tx + (-sx) * 128, ty + (-sy) * 38, fill=col, width=1.8, head=9)


def ait_table(c, x, y, w, h):
    rows = [("Paper", "230", "thin, fast to heat"),
            ("Wood", "250–300", "geometry dependent"),
            ("Polyurethane foam", "≈ 300", "low density, high surface"),
            ("Propane", "450", "gas"),
            ("Methane", "537", "gas"),
            ("Hydrogen", "585", "very low ignition energy"),
            ("Petrol vapour", "280–456", "wide range")]
    table(c, x, y, w, [(a, b, cc) for a, b, cc in rows], ["MATERIAL", "AIT (°C)", "COMMENT"],
          colw=[w * 0.34, w * 0.20, w * 0.46], h=h, size=18)


def flash_table(c, x, y, w, h):
    rows = [("Petrol", "−43", "280–456", "1.4–7.6"),
            ("Methanol", "11", "464", "6.7–36"),
            ("Ethanol", "13", "363", "3.3–19"),
            ("Kerosene", "38–74", "≈ 220", "0.7–5.0"),
            ("Diesel", "52–60", "≈ 250", "0.6–7.5"),
            ("Hydrogen", "—", "585", "4–75"),
            ("Propane (LPG)", "−104", "450", "2.1–9.5")]
    table(c, x, y, w, [(a, b, cc, d) for a, b, cc, d in rows],
          ["FUEL", "FLASH POINT °C", "AIT °C", "FLAMMABLE RANGE %"],
          colw=[w * 0.28, w * 0.24, w * 0.20, w * 0.28], h=h, size=17)


def hrr_table(c, x, y, w, h):
    rows = [("Candle", "0.05", "open"), ("Wastebasket", "0.02–0.1", "open"),
            ("Armchair", "0.2–0.4", "open"), ("Car", "1.5–5", "open"),
            ("Retail rack", "5–30", "sprinklered design"), ("Warehouse", "50–100+", "rack storage"),
            ("Petrol tank 20 m", "900–1 500", "foam design")]
    table(c, x, y, w, [(a, b, cc) for a, b, cc in rows], ["ITEM", "PEAK HRR (MW)", "CONTEXT"],
          colw=[w * 0.34, w * 0.28, w * 0.38], h=h, size=18)


def phenomena_table(c, x, y, w, h):
    rows = [("Rollover", "flames in the hot layer", "flashover approaching"),
            ("Flashover", "all surfaces ignite together", "transition to ventilation control"),
            ("Backdraft", "deflagration on air entry", "quiet, hot, fuel-rich compartment"),
            ("Smoke explosion", "pre-mixed cloud ignites", "unburnt gas outside the fire room"),
            ("Flash fire", "vapour cloud deflagration", "no significant overpressure"),
            ("Boilover", "water bottom flashes to steam", "tank fire, audible change"),
            ("BLEVE", "vessel rupture under fire", "rising pressure, flame impingement"),
            ("Dust explosion", "dust cloud deflagration", "layers, conveying, bagging")]
    table(c, x, y, w, [(a, b, cc) for a, b, cc in rows], ["PHENOMENON", "MECHANISM", "WARNING SIGN"],
          colw=[w * 0.22, w * 0.38, w * 0.40], h=h, size=16)


def regime_diagnosis(c, x, y, w, h):
    rows = [("Smoke colour", "light grey to brown", "dense, black, opaque"),
            ("Smoke velocity", "steady, strong outward", "pulsing, in and out"),
            ("Flame", "bright, attached, tall", "lazy, detached, or external"),
            ("Layer temperature", "rises with fuel area", "rises with openings"),
            ("CO concentration", "moderate", "high"),
            ("Response to water", "HRR falls at once", "steam conversion, slow effect")]
    cw = w / 3
    c.text(x + 8, y, "EVIDENCE", size=13, color=MUTED, fname="Inter-SemiBold", track=1.1)
    c.text(x + cw + 8, y, "FUEL-CONTROLLED", size=13, color=AMBER, fname="Inter-SemiBold", track=1.1)
    c.text(x + 2 * cw + 8, y, "VENTILATION-CONTROLLED", size=13, color=RED, fname="Inter-SemiBold", track=1.1)
    c.line([(x, y + 24), (x + w, y + 24)], fill=(44, 58, 82), width=1)
    rh = (h - 30) / len(rows)
    for i, (a, b, cc) in enumerate(rows):
        ry = y + 30 + i * rh
        if i % 2 == 0:
            c.rect(x, ry, w, rh - 2, fill=(15, 22, 35), r=4)
        c.text(x + 8, ry + rh / 2, a, size=16, color=TEXT, fname="Inter-Medium", anchor="lm")
        c.text(x + cw + 8, ry + rh / 2, b, size=16, color=(210, 200, 180), fname="Inter-Regular",
               anchor="lm", maxw=cw - 16)
        c.text(x + 2 * cw + 8, ry + rh / 2, cc, size=16, color=(226, 186, 176), fname="Inter-Regular",
               anchor="lm", maxw=cw - 16)


# ------------------------------------------------------------------ charts of worked examples


def worked_panel(c, x, y, w, h, steps, result=None, title="SOLUTION"):
    c.panel(x, y, w, h, fill=(15, 22, 35), outline=(40, 54, 78), r=12)
    c.text(x + 22, y + 20, title, size=12, color=AMBER, fname="Inter-SemiBold", track=1.3)
    cy = y + 48
    for i, s in enumerate(steps):
        if s.startswith("="):
            c.text(x + 22, cy, s[1:], size=17, color=TEXT, fname="Serif-Regular", maxw=w - 44)
            cy += 30
        elif s.startswith(">"):
            c.text(x + 22, cy, s[1:], size=15, color=(255, 170, 110), fname="Inter-SemiBold",
                   maxw=w - 44, spacing=1.3)
            cy += 26
        else:
            _, hh = c.text(x + 22, cy, s, size=14, color=MUTED, fname="Inter-Regular",
                           maxw=w - 44, spacing=1.3)
            cy += hh + 8
    if result:
        c.rect(x + 16, y + h - 66, w - 32, 50, fill=(38, 22, 16), r=8)
        c.text(x + 30, y + h - 41, result, size=17, color=EMBER, fname="Inter-SemiBold",
               anchor="lm", maxw=w - 60)


def worked_t2(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.68, (0, 600), (0, 16000), "TIME (s)", "HRR (kW)",
               xticks=[0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600],
               yticks=[0, 4000, 8000, 12000, 16000], yfmt=lambda v: f"{v/1000:.0f} MW")
    ts = np.linspace(0, 600, 400)
    ys = 0.0469 * ts ** 2
    ch.area(ts, np.minimum(ys, 14000), EMBER, 30)
    ch.line(ts[ys < 14000], ys[ys < 14000], EMBER, 3.0)
    ch.hline(14000, RED, 1.6, 10, "VENTILATION LIMIT  14 MW")
    for t in (60, 120, 146, 300, 450):
        q = 0.0469 * t ** 2
        ch.point(t, min(q, 14000), AMBER, 5)
        c.text(ch.tx(t) + 10, ch.ty(min(q, 14000)) - 14, f"{q/1000:.2f} MW" if q < 1000 else f"{q/1000:.1f} MW",
               size=12, color=AMBER, fname="Mono-Regular", anchor="lm")
    ch.vline(math.sqrt(14000 / 0.0469), (255, 255, 255), 1.2, 6, "PLATEAU")
    c.text(ch.tx(300), ch.ty(15500), "Q = 0.0469 t²   (fast growth)", size=14, color=EMBER,
           fname="Serif-Regular")
    worked_panel(c, x, y + h * 0.70, w, h * 0.30,
                 ["The fire quadruples each time the clock doubles.",
                  "At 5 min the assumed curve reaches 4.2 MW.",
                  ">Plateau at 9.1 min: air, not fuel, becomes the limit."],
                 result="Illustrative growth only — not an incident forecast")


def worked_vent(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    blocks = [("OPENING AREA A", "6.0 m²", "two doors, 3 m² each", TEAL),
              ("OPENING HEIGHT H", "2.4 m", "√H = 1.55", TEAL),
              ("VENTILATION FACTOR", "A√H = 9.3", "m²·m^0.5", AMBER),
              ("AIR MASS FLOW", "4.65 kg/s", "0.5 × A√H", AMBER),
              ("MAXIMUM HRR", "14 MW", "1 500 × A√H", EMBER)]
    bw = (w - 40) / len(blocks)
    for i, (t, v, sub, col) in enumerate(blocks):
        bx = x + i * (bw + 10)
        c.panel(bx, y + 40, bw, h * 0.44, fill=(16, 23, 37), outline=(42, 56, 80), r=10)
        c.text(bx + 16, y + 58, t, size=11, color=col, fname="Inter-SemiBold", track=1.0, maxw=bw - 30)
        c.text(bx + 16, y + 96, v, size=25, color=TEXT, fname="Serif-SemiBold", maxw=bw - 30)
        c.text(bx + 16, y + 140, sub, size=13, color=MUTED, fname="Inter-Regular", maxw=bw - 30)
        if i < len(blocks) - 1:
            c.arrow(bx + bw + 2, y + 40 + h * 0.22, bx + bw + 8, y + 40 + h * 0.22, fill=(90, 108, 136), width=1.6, head=6)
    # check bar
    c.text(x, y + h * 0.62, "CROSS-CHECK: 4.65 kg/s × 3.0 MJ/kg = 13.9 MW  ≈  14 MW", size=16,
           color=TEAL, fname="Inter-SemiBold")
    c.text(x, y + h * 0.70, "Same assumptions: consistency check, not independent validation.",
           size=15, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h * 0.80, "Open the roller shutter and A rises: the fire's ceiling rises with it.",
           size=15, color=(255, 170, 110), fname="Inter-Medium")


def worked_radiation(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.66, (2, 20), (1, 30), "DISTANCE FROM FIRE (m)", "RADIANT FLUX (kW/m²)",
               ylog=True, xlog=False, yticks=[1, 2, 5, 10, 20, 30],
               xticks=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    rs = np.linspace(2, 20, 200)
    qs = 0.3 * 10000 / (4 * math.pi * rs ** 2)
    ch.line(rs, qs, EMBER, 3.0)
    for q, col, lab in [(20, RED, "illustrative contour"), (12.5, AMBER, "illustrative contour"),
                        (4.7, TEAL, "illustrative contour"), (2.5, BLUE, "illustrative contour")]:
        ch.hline(q, col, 1.2, 7, f"{q} kW/m²  ·  {lab}")
        r = math.sqrt(0.3 * 10000 / (4 * math.pi * q))
        ch.point(r, q, col, 4)
    worked_panel(c, x, y + h * 0.69, w, h * 0.31,
                 ["Q = 10 MW, 30 % radiated.  q″ = 0.3Q / 4πr²",
                  ">r = √(0.3 × 10 000 / (4π × q″))",
                  "These contours are not safe exposure or stand-off limits."],
                 result="4.4 m at 12.5 kW/m²  ·  9.8 m at 2.5 kW/m²")


def worked_flashover(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.66, (0, 480), (0, 4000), "TIME (s)", "HRR (kW)",
               xticks=[0, 60, 120, 180, 240, 300, 360, 420, 480],
               yticks=[0, 1000, 2000, 3000, 4000], yfmt=lambda v: f"{v/1000:.0f} MW")
    for a, col, lab in [(0.01172, TEAL, "medium"), (0.0469, AMBER, "fast"), (0.1876, RED, "ultra-fast")]:
        ts = np.linspace(0, 480, 300)
        ys = a * ts ** 2
        ch.line(ts, np.minimum(ys, 4000), col, 2.4)
        t = math.sqrt(2000 / a)
        ch.point(t, 2000, col, 5)
        c.text(ch.tx(t) + 8, ch.ty(2000) - 16 - (8 if a == 0.01172 else 0), f"{lab}: {t/60:.1f} min",
               size=13, color=col, fname="Inter-SemiBold")
    ch.hline(2000, WHITE, 1.6, 8, "FLASHOVER  ≈ 2.0 MW")
    worked_panel(c, x, y + h * 0.69, w, h * 0.31,
                 ["A = 1.8 m², H = 2.0 m → A√H = 2.55",
                  "Thomas 1.9 MW · McCaffrey ≈ 2.0 MW → use 2.0 MW",
                  ">Flashover in 3.4 min (fast) or 1.7 min (ultra-fast)."],
                 result="Assumed threshold only — not a safe-entry clock")


def worked_water(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.66, (0, 20), (0, 3000), "HEAT RELEASE RATE (MW)", "WATER FLOW (L/min)",
               xticks=[0, 5, 10, 15, 20], yticks=[0, 500, 1000, 1500, 2000, 2500, 3000])
    xs = np.linspace(0.5, 20, 100)
    for eff, col, lab in [(1.0, TEAL, "100 % (theoretical)"), (0.35, AMBER, "35 % contact efficiency"),
                          (0.18, RED, "18 % assumed utilisation")]:
        ys = xs * 60 / (2.591 * eff)  # L/min
        ch.line(xs, ys, col, 2.4, label=lab)
    ch.point(14, 14 * 60 / (2.591 * 0.35), AMBER, 6, ring=AMBER,
             label="14 MW → 926 L/min", dx=-10, dy=-24)
    ch.legend()
    worked_panel(c, x, y + h * 0.69, w, h * 0.31,
                 ["1 kg water: 4.18 × 80 K + 2 257 kJ = 2.59 MJ",
                  "14 MW ÷ 2.59 MJ/kg = 5.4 kg/s = 324 L/min minimum",
                  ">Assumed 35 % utilisation: ≈ 926 L/min, not a design flow."],
                 result="Energy balance only — not operational fire-flow sizing")


# ------------------------------------------------------------------ CFD + tools


def cfd_field(c, x, y, w, h, seed=5):
    Wp, Hp = 520, 300
    yy, xx = np.mgrid[0:Hp, 0:Wp].astype(np.float32)
    X, Y = xx / Wp, yy / Hp
    field = np.zeros((Hp, Wp), dtype=np.float32)
    for cx, amp in [(0.22, 1.0), (0.46, 0.55)]:
        width = 0.035 + 0.13 * Y
        field += amp * np.exp(-((X - cx) ** 2) / (2 * width ** 2)) * np.exp(-Y * 0.8)
    field += 0.55 * np.exp(-((Y - 0.12) ** 2) / (2 * 0.06 ** 2)) * (0.4 + 0.6 * np.exp(-((X - 0.3) ** 2) / 0.4))
    for (vx, vy, sg) in [(0.62, 0.42, 0.10), (0.78, 0.30, 0.08), (0.35, 0.55, 0.09)]:
        field += 0.28 * np.exp(-(((X - vx) ** 2 + (Y - vy) ** 2)) / (2 * sg ** 2))
    fmin, fmax = float(field.min()), float(field.max())
    field = (field - fmin) / (fmax - fmin + 1e-9)
    stops = [(0.0, (8, 10, 18)), (0.25, (52, 26, 74)), (0.5, (150, 42, 52)),
             (0.75, (240, 120, 30)), (1.0, (255, 238, 170))]
    arr = np.zeros((Hp, Wp, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        a, ca = stops[i]
        b, cb = stops[i + 1]
        m = (field >= a) & (field <= b)
        t = ((field - a) / (b - a + 1e-6))[..., None]
        arr += np.where(m[..., None], np.array(ca, dtype=np.float32) * (1 - t) + np.array(cb, dtype=np.float32) * t - arr, 0)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize(
        (int(w * 0.62), int(w * 0.62 * Hp / Wp)), Image.BICUBIC)
    c.img.paste(img, (int(x * c.sc), int(y * c.sc)))
    c.d = ImageDraw.Draw(c.img)
    ih = w * 0.62 * Hp / Wp
    for i in range(1, 16):
        c.line([(x + w * 0.62 * i / 16, y), (x + w * 0.62 * i / 16, y + ih)], fill=(255, 255, 255), width=0.3)
    for i in range(1, 8):
        c.line([(x, y + ih * i / 8), (x + w * 0.62, y + ih * i / 8)], fill=(255, 255, 255), width=0.3)
    c.rect(x, y, w * 0.62, ih, outline=(90, 108, 136), width=1)
    c.text(x + 12, y + 12, "TEMPERATURE FIELD  ·  LES  ·  10 cm cells", size=12, color=WHITE,
           fname="Inter-SemiBold", track=0.8)
    cbx = x + w * 0.65
    c.text(cbx, y, "°C", size=12, color=MUTED, fname="Inter-Medium")
    steps = 60
    for i in range(steps):
        t = 1 - i / steps
        idx = t * (len(stops) - 1)
        i0 = min(int(idx), len(stops) - 2)
        f = idx - i0
        ca = np.array(stops[i0][1], dtype=float)
        cb2 = np.array(stops[i0 + 1][1], dtype=float)
        col = tuple(int(v) for v in (ca * (1 - f) + cb2 * f))
        c.rect(cbx, y + 22 + i * (ih - 30) / steps, 18, (ih - 30) / steps + 1, fill=col)
    for val, frac in [(20, 0.0), (200, 0.33), (600, 0.66), (1000, 1.0)]:
        yy2 = y + 22 + (1 - frac) * (ih - 30)
        c.text(cbx + 26, yy2, f"{val}", size=12, color=MUTED, fname="Mono-Regular", anchor="lm")
    ax = x + w * 0.65
    notes = [("PLUME", "entrainment and acceleration", EMBER),
             ("CEILING JET", "radial spread under the roof", AMBER),
             ("HOT LAYER", "descending interface", TEAL),
             ("VORTICES", "turbulent mixing controls combustion", VIOLET)]
    ty = y + ih + 26
    for a, b, col in notes:
        c.rect(ax, ty + 5, 6, 6, fill=col, r=1)
        c.text(ax + 16, ty, a, size=14, color=col, fname="Inter-SemiBold", track=0.6)
        c.text(ax + 16, ty + 18, b, size=12, color=MUTED, fname="Inter-Regular", maxw=w * 0.33)
        ty += 46


def tools_grid(c, x, y, w, h):
    items = [("THERMAL IMAGING", "layer interface, hot steel, hidden heat — surface temperature only", EMBER, "tic"),
             ("SMOKE OBSERVATION", "colour, velocity, density, direction, pulsing", AMBER, "smoke"),
             ("FIRE MODELLING", "pre-plans, training, reconstruction — not entry decisions", TEAL, "model"),
             ("MONITORING", "gas detection, pressure, structural sensors, drones", BLUE, "monitor")]
    cw, chh = (w - 24) / 2, (h - 24) / 2
    for i, (t, b, col, kind) in enumerate(items):
        cx = x + (i % 2) * (cw + 24)
        cy = y + (i // 2) * (chh + 24)
        c.panel(cx, cy, cw, chh, fill=(15, 22, 36), outline=(40, 54, 78), r=12)
        c.text(cx + 22, cy + 20, t, size=13, color=col, fname="Inter-SemiBold", track=1.2)
        c.text(cx + 22, cy + 48, b, size=16, color=MUTED, fname="Inter-Regular", maxw=cw - 44, spacing=1.35)
        # icon
        ix, iy = cx + cw - 90, cy + chh - 70
        if kind == "tic":
            c.rect(ix, iy, 60, 44, fill=(20, 28, 42), outline=col, r=6)
            c.rect(ix + 8, iy + 8, 44, 28, fill=(120, 40, 60))
            c.rect(ix + 8, iy + 8, 44, 10, fill=(240, 160, 60))
            c.rect(ix + 24, iy - 6, 12, 8, fill=col)
        elif kind == "smoke":
            smoke_fill(c, ix - 10, iy, 90, 54, 150, seed=5, color=(140, 148, 160))
        elif kind == "model":
            for k in range(4):
                c.line([(ix, iy + k * 14), (ix + 60, iy + k * 14)], fill=col, width=1)
            for k in range(5):
                c.line([(ix + k * 15, iy), (ix + k * 15, iy + 42)], fill=col, width=1)
            c.rect(ix + 12, iy + 12, 18, 18, fill=col, r=3)
        else:
            c.rect(ix, iy + 10, 60, 34, fill=(20, 28, 42), outline=col, r=4)
            xs = [(ix + 4 + k * 5, iy + 30 - 12 * math.sin(k * 0.6)) for k in range(12)]
            c.line(xs, fill=col, width=2)


def case_cards(c, x, y, w, h):
    items = [("2003", "WEST PHARMACEUTICALS", "Kinston, USA", "Combustible polyethylene dust deflagration", RED),
             ("2005", "BUNCEFIELD OIL TERMINAL", "Hemel Hempstead, UK", "Vapour cloud explosion and multi-tank fire", AMBER),
             ("2017", "GRENFELL TOWER", "London, UK", "Combustible cladding and vertical spread", EMBER)]
    cw = (w - 36) / 3
    for i, (yr, t, place, mech, col) in enumerate(items):
        cx = x + i * (cw + 18)
        c.panel(cx, y, cw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.text(cx + 22, y + 22, yr, size=42, color=col, fname="Serif-Bold")
        c.text(cx + 22, y + 78, t, size=15, color=TEXT, fname="Inter-SemiBold", track=0.6, maxw=cw - 40)
        c.text(cx + 22, y + 104, place, size=13, color=MUTED, fname="Inter-Regular")
        c.line([(cx + 22, y + 132), (cx + cw - 22, y + 132)], fill=(44, 58, 82), width=1)
        c.text(cx + 22, y + 150, mech, size=16, color=(214, 222, 236), fname="Inter-Regular",
               maxw=cw - 44, spacing=1.4)


def decision_matrix(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    stages = [("EVIDENCE", ["layer depth", "neutral plane", "smoke velocity", "structural assessment"], AMBER),
              ("REGIME", ["fuel-controlled", "ventilation-controlled", "under-ventilated"], EMBER),
              ("DECISION", ["offensive", "transitional", "defensive"], TEAL),
              ("TRIGGER", ["worsening conditions", "structural concern", "water shortfall", "escape compromised"], RED)]
    bw = (w - 60) / 4
    for i, (t, items, col) in enumerate(stages):
        bx = x + 20 + i * (bw + 7)
        c.panel(bx, y + 40, bw, h - 80, fill=(16, 23, 37), outline=(42, 56, 80), r=10)
        c.rect(bx, y + 40, bw, 4, fill=col)
        c.text(bx + 16, y + 60, t, size=12, color=col, fname="Inter-SemiBold", track=1.1)
        cy = y + 88
        for it in items:
            c.rect(bx + 16, cy + 6, 5, 5, fill=col, r=1)
            _, hh = c.text(bx + 28, cy, it, size=15, color=TEXT, fname="Inter-Regular", maxw=bw - 44, spacing=1.25)
            cy += hh + 14
        if i < 3:
            c.arrow(bx + bw + 1, y + h / 2, bx + bw + 6, y + h / 2, fill=(90, 108, 136), width=1.4, head=5)
    c.text(x + 20, y + h - 22, "The decision is only as good as the observation that fed it.", size=14,
           color=MUTED, fname="Inter-Regular")


def sizeup_table(c, x, y, w, h):
    rows = [("1  BUILDING", "volume, openings, construction, cladding", "how fast can it fill and spread?"),
            ("2  FUEL", "commodity, height, arrangement, dust or vapour", "how big can it get?"),
            ("3  SMOKE", "colour, velocity, density, layer depth", "what stage and regime?"),
            ("4  HEAT", "TIC limitations, heat exposure, structure", "what are the limits of the evidence?"),
            ("5  AIR TRACK", "direction and strength at openings", "where is it drawing from?"),
            ("6  PREDICTION", "regime, stage, HRR, next transition", "what do we do, and when?")]
    cw = [w * 0.20, w * 0.42, w * 0.38]
    c.text(x, y, "STEP", size=12, color=AMBER, fname="Inter-SemiBold", track=1.1)
    c.text(x + cw[0], y, "OBSERVE", size=12, color=AMBER, fname="Inter-SemiBold", track=1.1)
    c.text(x + cw[0] + cw[1], y, "INTERPRET", size=12, color=AMBER, fname="Inter-SemiBold", track=1.1)
    c.line([(x, y + 22), (x + w, y + 22)], fill=(44, 58, 82), width=1)
    rh = (h - 30) / len(rows)
    for i, (a, b, cc) in enumerate(rows):
        ry = y + 28 + i * rh
        if i % 2 == 0:
            c.rect(x, ry, w, rh - 2, fill=(15, 22, 35), r=4)
        c.text(x + 6, ry + rh / 2, a, size=16, color=TEXT, fname="Inter-SemiBold", anchor="lm")
        c.text(x + cw[0], ry + rh / 2, b, size=15, color=(200, 210, 226), fname="Inter-Regular",
               anchor="lm", maxw=cw[1] - 14)
        c.text(x + cw[0] + cw[1], ry + rh / 2, cc, size=15, color=(226, 200, 176), fname="Inter-Regular",
               anchor="lm", maxw=cw[2] - 14)


def assessment_list(c, x, y, w, h, items):
    colw = (w - 30) / 2
    for i, it in enumerate(items):
        col = i // 5
        row = i % 5
        cx = x + col * (colw + 30)
        cy = y + row * (h / 5.2)
        c.text(cx, cy, f"{i+1:02d}", size=22, color=EMBER, fname="Serif-Bold", anchor="la")
        c.text(cx + 44, cy, it, size=16, color=TEXT, fname="Inter-Regular", maxw=colw - 50, spacing=1.34)


# ------------------------------------------------------------------ demonstration


def demo_state(t, phase):
    """Return warehouse parameters for demonstration time t (seconds)."""
    if phase == "growth":
        q = 0.0469 * t ** 2 / 1000.0  # MW
        frac = min(0.52, 0.02 + t / 180 * 0.24)
        fires = [(1, 1 + int(t > 90), 40 + t * 0.55)]
        doors, vents = 0, 0
        temp = 0.15 + 0.35 * min(1, t / 180)
    elif phase == "spread":
        q = 0.0469 * t ** 2 / 1000.0
        frac = min(0.72, 0.26 + (t - 180) / 180 * 0.22)
        fires = [(1, 3, 120), (2, 2, 90)]
        doors, vents = 0, 0
        temp = 0.5 + 0.25 * min(1, (t - 180) / 180)
    elif phase == "vent":
        q = 14000 / 1000.0
        frac = 0.74
        fires = [(1, 3, 140), (2, 2, 110), (2, 3, 90)]
        doors, vents = 1, 1
        temp = 0.85
    else:
        q = 14.0
        frac = 0.80
        fires = [(0, 3, 120), (1, 3, 150), (2, 2, 120)]
        doors, vents = 1, 1
        temp = 0.9
    return dict(q=q, frac=frac, fires=fires, doors=doors, vents=vents, temp=temp)


def demo_setup(c, x, y, w, h):
    g = warehouse(c, x + 8, y + 40, w - 16, h - 110, layer_frac=0.0, fires=[(1, 1, 55)], doors=0, vents=0,
                  sprinkler=True, labels=True)
    # annotations
    ann = [("60 m × 30 m × 9 m", g["x"] + 30, g["y"] + 26, TEAL),
           ("six-tier racking to 7 m", g["x"] + g["w"] * 0.30, g["y"] + 30, AMBER),
           ("four roller shutters — closed", g["x"] + 24, g["floor"] - 90, MUTED),
           ("roof vents — closed", g["x"] + g["w"] * 0.52, g["y"] - 34, MUTED),
           ("ignition: electrical fault, rack 3, 1 m", g["x"] + g["w"] * 0.40, g["floor"] - 180, EMBER)]
    for t, lx, ly, col in ann:
        tag_chip(c, lx, ly, t, col, size=12)
    c.text(x, y + h - 34, "Illustrative only: assigned fast growth, suppression omitted; not a validated simulation.",
           size=14, color=MUTED, fname="Inter-Regular")


def demo_frame(c, x, y, w, h, t, phase="growth", two_panel=False, scenario="uncoord"):
    st = demo_state(t, phase)
    if two_panel:
        half = (w - 30) / 2
        for i, modes in enumerate([("uncoord", "DOOR OPENING: POSSIBLE ESCALATION"), ("coord", "ROOF VENTING: OUTCOME UNCERTAIN")]):
            bx = x + i * (half + 30)
            c.text(bx, y, modes[1], size=13, color=(RED if i == 0 else TEAL), fname="Inter-SemiBold", track=1.0)
            if modes[0] == "uncoord":
                g = warehouse(c, bx, y + 26, half, h - 90, layer_frac=0.78, layer_temp=0.9,
                              fires=[(0, 2, 130), (1, 2, 150), (2, 3, 110)], doors=2, vents=0,
                              sprinkler=False, labels=False, seed=33)
                c.text(bx + 10, y + 40, "door opened, no line charged", size=12, color=RED, fname="Inter-Medium")
                c.text(bx + 10, y + h - 54, "Illustration only: no calculated HRR or layer height", size=13,
                       color=(255, 160, 150), fname="Inter-SemiBold")
            else:
                g = warehouse(c, bx, y + 26, half, h - 90, layer_frac=0.42, layer_temp=0.55,
                              fires=[(1, 2, 110)], doors=1, vents=2, sprinkler=True, labels=False, seed=44)
                c.text(bx + half - 10, y + 40, "roof vented above the fire", size=12, color=TEAL,
                       fname="Inter-Medium", anchor="ra")
                c.text(bx + 10, y + h - 54, "Not a safe-advance prediction; assess actual effects", size=13,
                       color=(160, 240, 226), fname="Inter-SemiBold")
        return
    g = warehouse(c, x, y, w, h - 40, layer_frac=st["frac"], layer_temp=st["temp"], fires=st["fires"],
                  doors=st["doors"], vents=st["vents"], sprinkler=True, seed=21 + int(t // 10))
    # HUD readout (inside the frame, top right)
    c.panel(x + w - 322, y + 14, 306, 64, fill=(10, 15, 24), outline=(70, 88, 116), r=8, alpha=235)
    c.text(x + w - 304, y + 32, f"t = {t//60}:{t%60:02d}", size=21, color=TEXT, fname="Mono-Bold")
    c.text(x + w - 304, y + 58, f"Q ≈ {st['q']:.1f} MW", size=14, color=EMBER, fname="Inter-SemiBold")
    c.text(x + w - 190, y + 58, "layer: schematic", size=14, color=AMBER, fname="Inter-SemiBold")
    # layer depth indicator
    lx = x + 24
    ly0, ly1 = y + 20, y + 20 + (h - 40) * st["frac"]
    c.line([(lx, ly0), (lx, ly1)], fill=AMBER, width=1.5)
    for yy in (ly0, ly1):
        c.line([(lx - 5, yy), (lx + 5, yy)], fill=AMBER, width=1.5)
    c.text(lx + 10, (ly0 + ly1) / 2, "LAYER", size=11, color=AMBER, fname="Inter-SemiBold", anchor="lm", track=0.6)


def warehouse_spread(c, x, y, w, h):
    g = warehouse(c, x + 10, y + 60, w - 20, h - 140, layer_frac=0.34, layer_temp=0.45,
                  fires=[(1, 0, 90), (1, 2, 70)], doors=1, vents=0, sprinkler=False, labels=False)
    for k in range(3):
        c.arrow(g["x"] + g["w"] * (0.30 + k * 0.02), g["floor"] - 60 - k * 40,
                g["x"] + g["w"] * (0.30 + k * 0.02), g["floor"] - 190 - k * 40, fill=AMBER, width=2, head=9)
    tag_chip(c, g["x"] + g["w"] * 0.33, g["y"] + 60, "VERTICAL: flue spaces, rack face, roof void", AMBER, size=12)
    c.arrow(g["x"] + g["w"] * 0.30, g["floor"] - 120, g["x"] + g["w"] * 0.62, g["floor"] - 120,
            fill=EMBER, width=2, head=9, dash=6)
    tag_chip(c, g["x"] + g["w"] * 0.38, g["floor"] - 160, "HORIZONTAL: aisle radiation + ceiling jet", EMBER, size=12)
    c.text(x, y + h - 40, "High-piled storage turns a single-storey shell into a multi-storey combustible structure.",
           size=15, color=MUTED, fname="Inter-Regular")


def escalation_chain(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    # tanks
    positions = [(x + w * 0.14, y + h * 0.55), (x + w * 0.42, y + h * 0.36), (x + w * 0.70, y + h * 0.55)]
    for i, (tx, ty) in enumerate(positions):
        tw, th = w * 0.16, h * 0.26
        c.rect(tx - tw / 2, ty - th, tw, th, fill=(38, 48, 66), outline=(96, 112, 136), r=4)
        c.ellipse(tx - tw / 2, ty - th - 10, tw, 18, fill=(52, 66, 90))
        if i == 0:
            draw_flame(c, tx, ty - th - 8, tw * 0.5, h * 0.16, seed=4)
        if i == 1:
            draw_flame(c, tx, ty - th - 6, tw * 0.3, h * 0.09, seed=8)
        lbl = ["INITIAL FIRE", "RADIATION + FLAME", "VESSEL FAILURE"][i]
        col = [EMBER, AMBER, RED][i]
        c.text(tx, ty + 12, lbl, size=12, color=col, fname="Inter-SemiBold", anchor="ma", track=0.8)
        c.pool = None
    for i in range(2):
        a = positions[i]
        b = positions[i + 1]
        c.arrow(a[0] + w * 0.09, a[1] - h * 0.12, b[0] - w * 0.09, b[1] - h * 0.12,
                fill=AMBER if i == 0 else RED, width=2, head=10, dash=7)
    c.text(x + w * 0.14, y + h * 0.88, "20 min", size=13, color=MUTED, fname="Mono-Regular", anchor="ma")
    c.text(x + w * 0.70, y + h * 0.88, "45 min", size=13, color=MUTED, fname="Mono-Regular", anchor="ma")
    c.text(x + 20, y + 20, "DOMINO EFFECT", size=12, color=RED, fname="Inter-SemiBold", track=1.2)
    c.text(x + 20, y + h - 26, "Spacing, bunding, drainage and cooling water are fire dynamics controls.",
           size=14, color=MUTED, fname="Inter-Regular")


def material_props(c, x, y, w, h):
    # left: reaction to fire ladder
    c.text(x, y, "REACTION TO FIRE", size=12, color=AMBER, fname="Inter-SemiBold", track=1.1)
    classes = [("A1", "non-combustible", 0.08, TEAL), ("B", "very limited", 0.24, (80, 190, 180)),
               ("C", "limited", 0.42, AMBER), ("D", "medium", 0.58, (255, 150, 50)),
               ("E", "high", 0.74, EMBER), ("F", "unclassified", 0.92, RED)]
    bar_w = w * 0.44
    for i, (cl, desc, frac, col) in enumerate(classes):
        yy = y + 30 + i * 44
        c.rect(x, yy, bar_w * (1 - frac * 0.6), 26, fill=col, r=4)
        c.text(x + 10, yy + 13, cl, size=14, color=(15, 20, 30), fname="Mono-Bold", anchor="lm")
        c.text(x + bar_w * (1 - frac * 0.6) + 12, yy + 13, desc, size=13, color=MUTED,
               fname="Inter-Regular", anchor="lm")
    # right: fire resistance
    rx = x + w * 0.52
    c.text(rx, y, "FIRE RESISTANCE", size=12, color=TEAL, fname="Inter-SemiBold", track=1.1)
    for i, (code, desc) in enumerate([("R", "load-bearing capacity"), ("E", "integrity — no flame passage"),
                                      ("I", "insulation — temperature limit")]):
        yy = y + 40 + i * 74
        c.rect(rx, yy, 54, 54, fill=(20, 30, 46), outline=TEAL, r=8)
        c.text(rx + 27, yy + 27, code, size=26, color=TEAL, fname="Serif-Bold", anchor="mm")
        c.text(rx + 72, yy + 18, desc, size=14, color=TEXT, fname="Inter-Regular", maxw=w * 0.44)
        c.text(rx + 72, yy + 38, ["minutes of function retained", "stops fire and smoke", "stops heat"][i],
               size=12, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h - 40, "A combustible core can pass a fire resistance test and still destroy the building.",
           size=14, color=(255, 170, 110), fname="Inter-Medium")


def panel_section(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    px, py = x + 70, y + 60
    pw, ph = w * 0.30, h * 0.70
    # outer skins
    c.rect(px, py, pw, 12, fill=(150, 162, 180))
    c.rect(px, py + ph, pw, 12, fill=(150, 162, 180))
    # core
    for k in range(int(ph / 10)):
        col = (62, 72, 88) if k % 2 else (54, 64, 80)
        c.rect(px + 4, py + 14 + k * 10, pw - 8, 10, fill=col)
    # fire inside core at bottom left
    draw_flame(c, px + pw * 0.28, py + ph, 44, ph * 0.34, seed=12)
    with_alpha(c, lambda d, sc: d.rectangle(
        [px * sc, py * sc, (px + pw) * sc, (py + ph * 0.6) * sc], fill=(60, 60, 70, 60)))
    c.text(px + pw / 2, py - 18, "METAL SKIN", size=11, color=MUTED, fname="Inter-SemiBold", anchor="ma", track=1)
    c.text(px + pw / 2, py + ph / 2, "PLASTIC CORE\nPIR / PUR / EPS", size=15, color=(226, 232, 244),
           fname="Inter-SemiBold", anchor="mm", spacing=1.3)
    # chimney arrows
    for k in range(4):
        c.arrow(px + pw * 0.52, py + ph * 0.7 - k * 60, px + pw * 0.52, py + ph * 0.7 - k * 60 - 40,
                fill=EMBER, width=2.2, head=9)
    tag_chip(c, px + pw * 0.60, py + 20, "CAVITY CHIMNEY", EMBER, size=11)
    # right text
    tx = x + w * 0.46
    items = [("MELT", "core melts and pyrolyses inside the panel", EMBER),
             ("BURN", "combustion is hidden behind the metal skins", AMBER),
             ("RISE", "the vertical cavity acts as a chimney", RED),
             ("LEAPFROG", "fire emerges far from the origin", (226, 160, 90))]
    ty = y + 40
    for a, b, col in items:
        c.text(tx, ty, a, size=13, color=col, fname="Inter-SemiBold", track=1.1)
        c.text(tx, ty + 20, b, size=15, color=TEXT, fname="Inter-Regular", maxw=w * 0.5)
        ty += 62
    c.text(tx, y + h - 60, "Cold stores, clean rooms, warehouses and facades share this construction.",
           size=14, color=MUTED, fname="Inter-Regular", maxw=w * 0.52)


def structure_response(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.62, (0, 900), (0, 100), "TEMPERATURE (°C)", "STRENGTH RETAINED (%)",
               xticks=[0, 200, 400, 600, 800], yticks=[0, 25, 50, 75, 100])
    ts = np.linspace(20, 900, 200)
    steel = np.where(ts < 100, 100, np.where(ts < 550, 100 - (ts - 100) * 0.10, np.maximum(8, 55 - (ts - 550) * 0.10)))
    concrete = np.where(ts < 300, 100 - (ts - 20) * 0.03, np.maximum(25, 91 - (ts - 300) * 0.13))
    timber = np.maximum(25, 100 - ts * 0.045)
    ch.line(ts, steel, EMBER, 2.6, label="unprotected steel")
    ch.line(ts, concrete, (150, 160, 175), 2.4, label="concrete")
    ch.line(ts, timber, (146, 116, 78), 2.4, label="heavy timber (char)")
    ch.vline(550, RED, 1.4, 8, "550 °C")
    ch.legend()
    c.text(x, y + h * 0.66, "Indicators of impending structural failure", size=14, color=AMBER,
           fname="Inter-SemiBold", track=1.0)
    items = ["deflection and sagging of roof or floor", "new cracking, spalling, water boiling off",
             "roaring or rumbling, falling debris", "fire appearing through the structure"]
    cy = y + h * 0.72
    for it in items:
        c.rect(x, cy + 7, 5, 5, fill=RED, r=1)
        c.text(x + 16, cy, it, size=14, color=TEXT, fname="Inter-Regular")
        cy += 22


def confined_space(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    # silo
    sx, sy, sw, sh = x + 90, y + 70, w * 0.34, h * 0.60
    c.poly([(sx, sy + 40), (sx + sw, sy + 40), (sx + sw * 0.86, sy + sh), (sx + sw * 0.14, sy + sh)],
           fill=(30, 40, 56), outline=(96, 112, 136), width=2)
    c.ellipse(sx, sy + 26, sw, 28, fill=(38, 50, 68))
    # dust / gas layers
    with_alpha(c, lambda d, sc: d.rectangle(
        [sx * sc, (sy + sh * 0.45) * sc, (sx + sw) * sc, (sy + sh) * sc], fill=(150, 140, 110, 40)))
    c.text(sx + sw / 2, sy + sh * 0.62, "DUST / VAPOUR\nACCUMULATION", size=13, color=(220, 200, 150),
           fname="Inter-SemiBold", anchor="mm", spacing=1.3)
    c.text(sx + sw / 2, sy + sh * 0.90, "smouldering", size=12, color=EMBER, fname="Inter-Regular", anchor="ma")
    # monitor
    mx = x + w * 0.52
    items = [("O₂", "19.5 – 23.5 %", "deficiency kills without warning", TEAL),
             ("LEL", "< 10 %", "flammable atmosphere", AMBER),
             ("CO", "< 30 ppm", "asphyxiant, cumulative", RED),
             ("H₂S / VOC", "site limits", "toxic and flammable", VIOLET)]
    cy = y + 60
    for a, b, cc, col in items:
        c.text(mx, cy, a, size=15, color=col, fname="Mono-Bold")
        c.text(mx + 110, cy, b, size=15, color=TEXT, fname="Mono-Regular")
        c.text(mx, cy + 20, cc, size=12, color=MUTED, fname="Inter-Regular")
        cy += 62
    c.text(x + 24, y + h - 34, "Never trust a confined space: monitor, isolate, ventilate, then plan the rescue.",
           size=14, color=MUTED, fname="Inter-Regular")


def large_volume(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    bx, by, bw, bh = x + 20, y + 30, w - 40, h - 70
    c.rect(bx, by, bw, bh, fill=(14, 20, 31))
    c.rect(bx, by, bw, 14, fill=(58, 74, 100))
    c.rect(bx, by, 10, bh, fill=(46, 60, 84))
    c.rect(bx + bw - 10, by, 10, bh, fill=(46, 60, 84))
    c.rect(bx, by + bh - 10, bw, 10, fill=(34, 45, 62))
    # stratification
    for i in range(3):
        layer(c, bx + 10, by + 14, bw - 20, (bh - 24) * (0.30 + i * 0.16), 1.0, 0.55 - i * 0.13,
              seed=30 + i, alpha=150 - i * 35, interface=(i == 0))
    # fire
    draw_flame(c, bx + bw * 0.30, by + bh - 12, 42, bh * 0.20, seed=8)
    c.text(bx + 26, by + bh * 0.30, "SMOKE RESERVOIR — slow to descend", size=13, color=AMBER,
           fname="Inter-SemiBold", track=0.7)
    c.text(bx + 26, by + bh * 0.55, "THERMAL STRATIFICATION — cool layer persists", size=13,
           color=TEAL, fname="Inter-SemiBold", track=0.7)
    c.text(bx + 26, by + bh - 36, "WORKING LEVEL — tenable for longer", size=13, color=(180, 200, 220),
           fname="Inter-SemiBold", track=0.7)
    # travelling fire arrow
    c.arrow(bx + bw * 0.36, by + bh - 26, bx + bw * 0.72, by + bh - 26, fill=EMBER, width=2, head=10, dash=7)
    c.text(bx + bw * 0.74, by + bh - 30, "TRAVELLING FIRE", size=12, color=EMBER, fname="Inter-SemiBold")


def model_types(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    bands = [("EMPIRICAL", "Alpert · Heskestad · Thomas", "fast, transparent, narrow", 0.32, TEAL),
             ("ZONE MODEL", "CFAST · two layers", "fast, simple geometry", 0.62, AMBER),
             ("FIELD MODEL", "FDS · LES · CFD", "detailed, expensive, powerful", 0.94, EMBER)]
    for i, (t, sub, note, frac, col) in enumerate(bands):
        bw = w * 0.62 * frac
        bx = x + 30 + (w * 0.62 - bw) / 2
        by = y + 60 + i * 92
        c.rect(bx, by, bw, 74, fill=(20, 28, 44), outline=col, r=8)
        c.text(bx + 18, by + 20, t, size=14, color=col, fname="Inter-SemiBold", track=1.1)
        c.text(bx + 18, by + 42, sub, size=13, color=TEXT, fname="Inter-Regular")
        c.text(bx + 18, by + 60, note, size=11, color=MUTED, fname="Inter-Regular")
    c.text(x + w * 0.66, y + 40, "FIDELITY", size=12, color=MUTED, fname="Inter-SemiBold", track=1.2)
    c.text(x + w * 0.66, y + 80, "Cost and skill rise with fidelity.\nChoose the simplest model that\nanswers the question.",
           size=14, color=TEXT, fname="Inter-Regular", spacing=1.4, maxw=w * 0.30)
    c.arrow(x + w * 0.66, y + h - 60, x + w * 0.66, y + 120, fill=(90, 108, 136), width=1.6, head=8)


def model_limits(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.66, (0, 900), (0, 16000), "TIME (s)", "HRR (kW)",
               xticks=[0, 150, 300, 450, 600, 750, 900], yticks=[0, 4000, 8000, 12000, 16000],
               yfmt=lambda v: f"{v/1000:.0f} MW")
    ts = np.linspace(0, 900, 300)
    ch.line(ts, 0.0469 * ts ** 2, EMBER, 2.2, label="t² model (unlimited)")
    real = []
    for t in ts:
        q = 0.0469 * t ** 2
        if t > 380:
            q = 6300 + 1200 * math.sin((t - 380) / 60)
            if t > 460:
                q = max(3500, 14000 * math.exp(-(t - 460) / 260))
        real.append(min(q, 16000))
    ch.line(ts, np.array(real), TEAL, 2.6, label="real fire (ventilation + fuel)")
    ch.hline(14000, RED, 1.4, 8, "VENTILATION LIMIT")
    ch.vline(380, (255, 255, 255), 1.0, 5, "ventilation begins to limit")
    ch.legend()
    c.text(x, y + h * 0.72, "Use t² for growth; use ventilation and fuel for the plateau and decay.",
           size=15, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h * 0.79, "A model outside its assumptions is a story, not a prediction.",
           size=15, color=(255, 170, 110), fname="Inter-Medium")


def smoke_drivers(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    bx, by, bw, bh = x + w * 0.06, y + 30, w * 0.46, h - 80
    # building section with 3 floors
    c.rect(bx, by, bw, bh, fill=(15, 22, 34), outline=(70, 86, 112), width=1.5)
    for i in range(1, 3):
        c.line([(bx, by + bh * i / 3), (bx + bw, by + bh * i / 3)], fill=(70, 86, 112), width=1)
    c.rect(bx + bw * 0.18, by + bh * 0.2, 10, bh * 0.8, fill=(50, 64, 88))
    # smoke in stairwell and top floor
    for f in range(3):
        fy = by + bh * f / 3
        if f >= 1:
            layer(c, bx + 2, fy, bw - 4, bh / 3, 0.35, 0.45, seed=40 + f, alpha=150)
    draw_flame(c, bx + bw * 0.6, by + bh - 4, 26, bh * 0.16, seed=6)
    # arrows
    c.arrow(bx + bw * 0.20, by + bh * 0.75, bx + bw * 0.20, by + bh * 0.25, fill=AMBER, width=2, head=9)
    tag_chip(c, bx + bw * 0.24, by + bh * 0.45, "STACK EFFECT", AMBER, size=11)
    c.arrow(bx + bw * 0.55, by + bh * 0.9, bx + bw * 0.55, by + bh * 0.16, fill=EMBER, width=2, head=9)
    tag_chip(c, bx + bw * 0.58, by + bh * 0.62, "BUOYANCY", EMBER, size=11)
    c.arrow(bx - 10, by + bh * 0.62, bx + 6, by + bh * 0.62, fill=TEAL, width=2, head=9)
    tag_chip(c, bx - 6, by + bh * 0.70, "WIND", TEAL, size=11)
    # right list
    items = [("Buoyancy", "Δρ from ΔT", EMBER), ("Expansion", "1 m³ air → ≈3 m³ smoke", AMBER),
             ("Stack effect", "vertical pressure from temperature", TEAL),
             ("Wind", "pressure on the facade", BLUE), ("HVAC", "ducts and air handlers", VIOLET)]
    lx = x + w * 0.56
    cy = y + 44
    for a, b, col in items:
        c.text(lx, cy, a, size=15, color=col, fname="Inter-SemiBold")
        c.text(lx, cy + 20, b, size=13, color=MUTED, fname="Inter-Regular")
        cy += 62
    c.text(lx, y + h - 40, "Smoke takes the paths we forgot.", size=14, color=TEXT, fname="Inter-Medium")


def visibility_chart(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.84, (0.01, 2.0), (0.5, 30), "OPTICAL DENSITY (1/m)", "VISIBILITY (m)",
               xlog=True, ylog=True, xticks=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0],
               yticks=[1, 2, 5, 10, 20, 30])
    od = np.linspace(0.01, 2.0, 200)
    for kv, col, lab in [(3, RED, "K = 3 (reflective signs)"), (5, AMBER, "K = 5"), (8, TEAL, "K = 8 (light-emitting)")]:
        ch.line(od, kv / od, col, 2.2, label=lab)
    ch.hline(10, WHITE, 1.2, 7, "TENABILITY TARGET  10 m")
    ch.legend()
    c.text(x, y + h * 0.87, "Visibility of 5 m or less: crews cannot find the seat, a casualty or an exit.",
           size=15, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h * 0.93, "Soot yield and optical density — not flame size — set the pace of the attack.",
           size=15, color=(255, 170, 110), fname="Inter-Medium")


def layer_build(c, x, y, w, h):
    panels = 4
    pw = (w - 54) / panels
    for i in range(panels):
        px = x + i * (pw + 18)
        frac = [0.14, 0.32, 0.52, 0.72][i]
        temp = [0.18, 0.38, 0.60, 0.85][i]
        c.panel(px, y, pw, h, fill=(11, 16, 25), outline=(34, 46, 66), r=10)
        gx, gy, gw, gh = px + 10, y + 12, pw - 20, h - 76
        c.rect(gx, gy, gw, gh, fill=(13, 19, 30))
        c.rect(gx, gy, gw, 8, fill=(52, 66, 90))
        c.rect(gx, gy + gh - 6, gw, 6, fill=(34, 45, 62))
        layer(c, gx, gy + 8, gw, gh - 14, frac, temp, seed=50 + i)
        draw_flame(c, gx + gw * 0.5, gy + gh - 6, gw * 0.20, gh * (0.14 + i * 0.06), seed=i + 2)
        # feedback arrows
        for k in range(3):
            c.arrow(gx + gw * (0.25 + k * 0.25), gy + gh * (1 - frac) + 10,
                    gx + gw * (0.25 + k * 0.25), gy + gh * (1 - frac) + 54 + i * 8,
                    fill=(255, 140, 60), width=1.6, head=7)
        t = ["100 °C", "250 °C", "450 °C", "600 °C"][i]
        c.text(px + 14, y + h - 54, f"LAYER {t}", size=13, color=AMBER, fname="Inter-SemiBold", track=0.8)
        c.text(px + 14, y + h - 32, ["5 kW/m² at floor", "10 kW/m²", "18 kW/m²", "25 kW/m²"][i],
               size=12, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h - 6, "Radiant feedback from the layer accelerates pyrolysis — the loop that ends in flashover.",
           size=14, color=MUTED, fname="Inter-Regular")


def vent_transition(c, x, y, w, h):
    seq_panels_local = [("SUFFICIENT AIR", "Fire follows fuel surface. Bright flame, efficient burning, lower CO.", AMBER),
                        ("REDUCED AIR", "Fire becomes fuel-rich. Dark smoke, high CO, unburnt gas accumulates.", VIOLET),
                        ("AIR RE-ENTERS", "Mixture ignites. Flashover or backdraft. Pressure and flame at the opening.", RED)]
    cw = (w - 36) / 3
    for i, (t, b, col) in enumerate(seq_panels_local):
        px = x + i * (cw + 18)
        c.panel(px, y, cw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.rect(px, y, cw, 4, fill=col)
        c.text(px + 18, y + 22, t, size=13, color=col, fname="Inter-SemiBold", track=1.0)
        c.text(px + 18, y + 48, b, size=15, color=TEXT, fname="Inter-Regular", maxw=cw - 36, spacing=1.35)
        gx, gy, gw, gh = px + 16, y + h * 0.52, cw - 32, h * 0.40
        c.rect(gx, gy, gw, gh, fill=(11, 16, 25))
        c.rect(gx, gy, gw, 6, fill=(52, 66, 90))
        c.rect(gx, gy + gh - 5, gw, 5, fill=(34, 45, 62))
        layer(c, gx, gy + 6, gw, gh - 10, 0.30 + i * 0.16, 0.3 + i * 0.2, seed=60 + i)
        draw_flame(c, gx + gw * 0.4, gy + gh - 5, gw * (0.22 - i * 0.04), gh * (0.2 + i * 0.05), seed=i)
        if i == 2:
            for k in range(2):
                c.arrow(gx + 2, gy + gh - 20 - k * 16, gx + gw * 0.35, gy + gh - 20 - k * 16,
                        fill=TEAL, width=2, head=8)


def flashover_predict(c, x, y, w, h):
    ch = Chart(c, x, y, w, h * 0.80, (0, 25), (0, 16000), "A√H (m²·m^0.5)", "Q AT FLASHOVER (kW)",
               xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 4000, 8000, 12000, 16000],
               yfmt=lambda v: f"{v/1000:.0f} MW")
    xs = np.linspace(0.5, 25, 100)
    ch.line(xs, 750 * xs, EMBER, 2.6, label="Thomas: 750 A√H")
    ch.line(xs, 610 * np.sqrt(0.07 * 63.2 * xs), TEAL, 2.4, label="McCaffrey (h_k A_T = 4.4 kW/K)")
    ch.point(2.55, 1913, AMBER, 6, ring=AMBER, label="5 × 4 m room, one door", dx=14, dy=-18)
    ch.legend()
    c.text(x, y + h * 0.84, "They meet at the design point — a 5 × 4 m room, one door: ≈ 2.0 MW.",
           size=15, color=MUTED, fname="Inter-Regular")
    c.text(x, y + h * 0.91, "Thomas grows faster with size because it ignores heat loss through the linings.",
           size=15, color=(255, 170, 110), fname="Inter-Medium")


def fuel_vs_vent_chart(c, x, y, w, h):
    ch = Chart(c, x, y, w, h, (0, 1800), (0, 16000), "TIME (s)", "HRR (kW)",
               xticks=[0, 300, 600, 900, 1200, 1500, 1800], yticks=[0, 4000, 8000, 12000, 16000],
               yfmt=lambda v: f"{v/1000:.0f} MW")
    ts = np.linspace(0, 1800, 400)
    fuel = np.where(ts < 700, 0.0117 * ts ** 2, np.maximum(0, 9200 * np.exp(-(ts - 700) / 320)))
    vent = np.where(ts < 520, 0.0469 * ts ** 2, np.minimum(14000, 14000 - 200 * np.sin((ts - 520) / 90)))
    vent = np.where(ts > 1200, np.maximum(0, 14000 * np.exp(-(ts - 1200) / 220)), vent)
    ch.line(ts, fuel, TEAL, 2.6, label="fuel-controlled")
    ch.line(ts, vent, EMBER, 2.6, label="ventilation-controlled")
    ch.vline(math.sqrt(14000 / 0.0469), (255, 255, 255), 1.0, 5, "ventilation limits")
    ch.legend()
    c.text(x, y + h + 22, "The same fuel package produces a different fire, depending on the air available.",
           size=14, color=MUTED, fname="Inter-Regular")


def case_compare(c, x, y, w, h):
    rows = [("West Pharmaceutical (2003)", "polyethylene dust", "dust deflagration, secondary explosions",
             "distributed fuel + building geometry"),
            ("Buncefield (2005)", "petrol vapour", "vapour cloud explosion, multi-tank fire",
             "flash point, dispersion, radiation"),
            ("Grenfell Tower (2017)", "ACM-PE cladding, PIR", "external vertical spread",
             "combustible insulation in a cavity")]
    table(c, x, y, w, [(a, b, cc, d) for a, b, cc, d in rows],
          ["CASE", "FUEL", "MECHANISM", "FIRE DYNAMICS LESSON"],
          colw=[w * 0.28, w * 0.20, w * 0.28, w * 0.24], h=h, size=16)


# ------------------------------------------------------------------ case study visuals
def _photo_card(c, x, y, w, h, img, caption, accent=EMBER):
    if img and os.path.exists(img):
        im = Image.open(img).convert("RGB")
        tw, th = int(w * c.sc), int(h * c.sc)
        im = im.resize((tw, th), Image.LANCZOS)
        # darken
        arr = np.asarray(im).astype(np.float32) * 0.78
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        c.img.paste(im, (int(x * c.sc), int(y * c.sc)))
        c.d = ImageDraw.Draw(c.img)
        # gradient bottom for caption
        with_alpha(c, lambda d, sc: d.rectangle(
            [x * sc, (y + h * 0.72) * sc, (x + w) * sc, (y + h) * sc], fill=(6, 9, 15, 210)))
        c.rect(x, y, w, h, outline=(60, 76, 102), width=1)
        c.text(x + 16, y + h - 34, caption, size=12, color=(200, 210, 226), fname="Inter-Regular",
               maxw=w - 32, spacing=1.25)
    else:
        c.panel(x, y, w, h, fill=(15, 22, 35), outline=(44, 58, 82), r=10)


def case_visual(c, x, y, w, h, key, title, meta, bullets, accent=EMBER):
    img = os.path.join(ASSETS, "img", key + ".jpg")
    _photo_card(c, x, y, w * 0.46, h, img, "Illustrative reconstruction — not the actual incident")
    tx = x + w * 0.50
    c.text(tx, y + 4, title, size=22, color=accent, fname="Serif-SemiBold", maxw=w * 0.50)
    c.text(tx, y + 40, meta, size=13, color=MUTED, fname="Inter-Regular", maxw=w * 0.50)
    cy = y + 74
    for b in bullets:
        c.rect(tx, cy + 7, 6, 6, fill=accent, r=1)
        _, hh = c.text(tx + 18, cy, b, size=15, color=TEXT, fname="Inter-Regular", maxw=w * 0.48, spacing=1.3)
        cy += hh + 12
