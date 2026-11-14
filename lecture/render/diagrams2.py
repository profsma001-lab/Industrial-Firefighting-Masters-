# -*- coding: utf-8 -*-
"""Schematics: rooms, warehouses, heat transfer, plumes, sequences."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import (Canvas, TEXT, MUTED, DIM, LINE, EMBER, AMBER, RED, TEAL, BLUE,
                 VIOLET, PANEL, PANEL2, PAL, WHITE)
from diagrams import (with_alpha, srect, flame_path, draw_flame, smoke_fill, person,
                      tag_chip, dotted, table, cards, eq_card)

WALL = (44, 58, 80)
WALL_L = (62, 80, 106)
FLOOR = (30, 40, 56)
STEEL = (86, 102, 126)
CARDBOARD = (146, 116, 78)
PLASTIC = (86, 118, 140)


def hot_color(t):
    """t 0..1 -> smoke colour from grey to orange."""
    t = max(0.0, min(1.0, t))
    a = np.array([86, 94, 108], dtype=float)
    b = np.array([198, 106, 58], dtype=float)
    t = t ** 1.15
    return tuple((a * (1 - t) + b * t).astype(int))


def _grid_noise(shape, cells, seed):
    rng = np.random.default_rng(seed)
    gh, gw = shape
    cy, cx = cells
    g = rng.random((cy, cx)).astype(np.float32)
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((gw, gh), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32) / 255.0


def layer(c, x, y, w, h, frac, temp=0.2, seed=4, alpha=205, interface=True, tex=0.075):
    """Ceiling smoke layer with internal billows. Returns interface polyline."""
    hh = h * frac
    if hh < 4:
        return []
    sc = c.sc
    Wp, Hp = max(2, int(w * sc)), max(2, int(hh * sc))
    gh, gw = 44, 130
    yy, xx = np.mgrid[0:gh, 0:gw]
    tn = yy / (gh - 1.0)
    n = _grid_noise((gh, gw), (5, 22), seed)
    n2 = _grid_noise((gh, gw), (3, 9), seed + 3)
    n3 = _grid_noise((gh, gw), (4, 11), seed + 11)
    edge = 0.88 + 0.16 * (n - 0.5) + 0.05 * (n2 - 0.5)
    a = np.clip((edge - tn) / 0.16, 0, 1) ** 1.15
    prof = 0.74 + 0.26 * (1 - tn)
    a = (a * prof * alpha).astype(np.uint8)

    base = np.array(hot_color(temp), dtype=np.float32)
    mod = (0.86 + tex * (n3 - 0.5) * 2 + 0.10 * (1 - tn))[:, :, None]
    rgb = np.clip(base[None, None, :] * mod, 0, 255).astype(np.uint8)

    lay = Image.fromarray(np.dstack([rgb, a]), mode="RGBA").resize((Wp, Hp), Image.BICUBIC)
    canvas_rgba = c.img.convert("RGBA")
    canvas_rgba.alpha_composite(lay, (int(x * sc), int(y * sc)))
    c.img = canvas_rgba.convert("RGB")
    c.d = ImageDraw.Draw(c.img)

    e_col = 0.88 + 0.16 * (n[-1, :] - 0.5) + 0.05 * (n2[-1, :] - 0.5)
    pts = [(x + w * i / (gw - 1), y + hh * float(e_col[i])) for i in range(gw)]
    if interface:
        edge_col = tuple(min(255, int(v * 1.30) + 24) for v in hot_color(temp))
        c.line(pts, fill=edge_col, width=1.0)
    return pts


def room(c, x, y, w, h, layer_frac=0.0, layer_temp=0.2, fire_x=0.5, fire_w=None,
         flames=0, seed=7, door=None, ceiling_thick=14, labels=True, studs=True):
    """Draw a compartment section. Returns dict of geometry."""
    wt = 14
    # walls
    c.rect(x, y, w, ceiling_thick, fill=(52, 66, 90))
    c.rect(x, y, wt, h, fill=WALL)
    c.rect(x + w - wt, y, wt, h, fill=WALL)
    c.rect(x, y + h - 10, w, 10, fill=FLOOR)
    # inner surface
    c.line([(x + wt, y + ceiling_thick), (x + w - wt, y + ceiling_thick)], fill=(70, 86, 112), width=1)
    # fire
    fx = x + fire_x * w
    fw = fire_w or w * 0.09
    if flames:
        draw_flame(c, fx, y + h - 10, fw, flames, seed=seed)
        with_alpha(c, lambda d, sc: d.ellipse(
            [(fx - fw * 1.4) * sc, (y + h - flames * 1.15) * sc, (fx + fw * 1.4) * sc, (y + h) * sc],
            fill=(255, 140, 40, 26)))
    if layer_frac > 0:
        layer(c, x + wt, y + ceiling_thick, w - 2 * wt, h - ceiling_thick - 10, layer_frac,
              layer_temp, seed=seed)
    # door opening (gap in right wall)
    if door:
        dh = door[1] * h
        c.rect(x + w - wt - 1, y + h - dh, wt + 2, dh, fill=(9, 13, 21))
        c.line([(x + w - wt, y + h - dh), (x + w, y + h - dh)], fill=(70, 86, 112), width=2)
    return dict(x=x, y=y, w=w, h=h, wt=wt, fx=fx, floor=y + h - 10, ceil=y + ceiling_thick)


def vent_arrows(c, x, y, h, out_color=EMBER, in_color=TEAL, n=3, w=26):
    for i in range(n):
        yy = y + h * (0.18 + i * 0.22)
        c.arrow(x + w + 6, yy, x + w + 52, yy, fill=out_color, width=2, head=10)
        yy2 = y + h * (0.68 + i * 0.12)
        c.arrow(x + w + 52, yy2, x + w + 6, yy2, fill=in_color, width=2, head=10)


# ---------------------------------------------------------------- heat transfer
def heat_modes(c, x, y, w, h):
    cw = (w - 40) / 3
    titles = [("CONDUCTION", "through solids", TEAL), ("CONVECTION", "by moving gas", AMBER),
              ("RADIATION", "by electromagnetic waves", EMBER)]
    for i, (t, sub, col) in enumerate(titles):
        cx = x + i * (cw + 20)
        c.panel(cx, y, cw, h, fill=(15, 22, 35), outline=(40, 54, 78), r=14)
        c.text(cx + 22, y + 18, t, size=14, color=col, fname="Inter-SemiBold", track=1.4)
        c.text(cx + 22, y + 40, sub, size=16, color=MUTED, fname="Inter-Regular")
        gx, gy, gw, gh = cx + 22, y + 78, cw - 44, h - 150
        if i == 0:
            c.rect(gx, gy, gw, gh, fill=(24, 32, 47), r=6)
            n = 8
            for k in range(n):
                px = gx + gw * (k + 0.5) / n
                c.rect(px - 2, gy + gh * 0.18, 4, gh * 0.64, fill=STEEL, r=2)
            for k in range(n - 1):
                px = gx + gw * (k + 1.0) / n
                c.arrow(px - 10, gy + gh * 0.5, px + 8, gy + gh * 0.5, fill=(255, 120 + k * 12, 60), width=2, head=8)
        elif i == 1:
            c.rect(gx, gy, gw, gh, fill=(24, 32, 47), r=6)
            draw_flame(c, gx + gw * 0.5, gy + gh * 0.88, gw * 0.16, gh * 0.3, seed=2)
            smoke_fill(c, gx + gw * 0.18, gy + gh * 0.05, gw * 0.64, gh * 0.45, 120, seed=3)
            for k in range(3):
                px = gx + gw * (0.36 + k * 0.14)
                c.arrow(px, gy + gh * 0.66, px, gy + gh * 0.22, fill=AMBER, width=2, head=9)
        else:
            c.rect(gx, gy, gw, gh, fill=(24, 32, 47), r=6)
            sx, sy = gx + gw * 0.22, gy + gh * 0.62
            draw_flame(c, sx, sy, gw * 0.14, gh * 0.22, seed=5)
            for k in range(6):
                a0 = -0.9 + k * 0.36
                px2 = sx + math.cos(a0) * gw * 0.55
                py2 = sy + math.sin(a0) * gh * 0.42
                c.arrow(sx + math.cos(a0) * gw * 0.1, sy + math.sin(a0) * gh * 0.08, px2, py2,
                        fill=(255, 150, 60), width=1.6, head=7, dash=5)
            c.rect(gx + gw * 0.72, gy + gh * 0.2, 8, gh * 0.66, fill=(120, 130, 148))
    eqs = ["q = k A ΔT / L", "q = h A ΔT", "q = ε σ A (T₁⁴ − T₂⁴)"]
    for i, e in enumerate(eqs):
        c.text(x + i * (cw + 20) + cw / 2, y + h - 46, e, size=20, color=TEXT,
               fname="Serif-Regular", anchor="mm")


def conduction_diagram(c, x, y, w, h):
    gx, gy, gw, gh = x, y, w, h * 0.62
    c.panel(gx, gy, gw, gh, fill=(15, 22, 35), outline=(40, 54, 78), r=12)
    # wall
    wx, ww = gx + 60, gw * 0.24
    c.rect(wx, gy + 30, ww, gh - 60, fill=(38, 49, 68))
    for k in range(9):
        yy = gy + 34 + k * (gh - 68) / 8
        c.line([(wx, yy), (wx + ww, yy)], fill=(52, 66, 90), width=1)
    # hot side fire
    draw_flame(c, wx - 34, gy + gh - 60, 34, gh * 0.36, seed=3)
    # temperature gradient
    for k in range(14):
        t = k / 13
        col = tuple(int(v) for v in np.array([255, 120, 40]) * (1 - t) + np.array([70, 120, 200]) * t)
        c.rect(wx + ww * t, gy + 30 + (gh - 60) * t * 0.12, ww / 14 + 1, gh - 60, fill=col)
    c.line([(wx, gy + gh - 60), (wx + ww, gy + gh - 60)], fill=WHITE, width=1)
    # arrows
    for k in range(4):
        yy = gy + 70 + k * (gh - 140) / 3
        c.arrow(wx + 14, yy, wx + ww - 14, yy, fill=(255, 210, 120), width=1.6, head=8)
    c.text(wx + ww / 2, gy + 16, "SOLID BARRIER", size=12, color=MUTED, fname="Inter-SemiBold", anchor="ma", track=1)
    c.text(wx - 34, gy + gh - 34, "HOT SIDE", size=13, color=EMBER, fname="Inter-SemiBold", anchor="ma")
    c.text(wx + ww + 46, gy + gh - 34, "COOL SIDE", size=13, color=BLUE, fname="Inter-SemiBold", anchor="ma")
    # k values
    rows = [("steel", "45"), ("concrete", "1.4"), ("brick", "0.7"), ("mineral wool", "0.04")]
    c.panel(x, y + h * 0.66, w * 0.52, h * 0.3, fill=(16, 23, 36), outline=(40, 54, 78), r=10)
    c.text(x + 18, y + h * 0.66 + 18, "THERMAL CONDUCTIVITY  k  (W/m·K)", size=12, color=AMBER,
           fname="Inter-SemiBold", track=1.0)
    for i, (m, v) in enumerate(rows):
        c.text(x + 18, y + h * 0.66 + 44 + i * 22, m, size=15, color=MUTED, fname="Inter-Regular")
        c.text(x + w * 0.44, y + h * 0.66 + 44 + i * 22, v, size=15, color=TEAL, fname="Mono-Regular", anchor="ra")
    c.text(x + w * 0.56, y + h * 0.72, "Heat flow rises with area and\ntemperature difference; it falls\nwith thickness.",
           size=17, color=TEXT, fname="Inter-Regular", spacing=1.4, maxw=w * 0.44)


def convection_diagram(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(15, 22, 35), outline=(40, 54, 78), r=12)
    g = room(c, x + 30, y + 30, w - 60, h - 70, layer_frac=0.3, layer_temp=0.45,
             fire_x=0.35, flames=h * 0.3, seed=4)
    for k in range(4):
        px = g["fx"] + 6 * k
        c.arrow(px, g["floor"] - h * 0.34, px + 10, g["ceil"] + 20, fill=AMBER, width=2, head=9)
    c.arrow(g["x"] + g["w"] * 0.7, g["ceil"] + h * 0.1, g["x"] + g["w"] * 0.7, g["ceil"] + h * 0.05, fill=AMBER, width=2)
    for k in range(3):
        c.arrow(g["x"] + g["w"] * 0.55 + k * 40, g["ceil"] + h * 0.1, g["x"] + g["w"] * 0.7 + k * 40,
                g["ceil"] + h * 0.1, fill=(255, 150, 70), width=1.6, head=8)
    c.text(x + w - 30, y + h - 22, "HOT GAS EXITS THROUGH OPENINGS", size=12, color=MUTED,
           fname="Inter-SemiBold", anchor="ra", track=0.8)


def radiation_diagram(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(13, 19, 31), outline=(40, 54, 78), r=12)
    floor = y + h - 46
    sx, sy = x + 96, floor - 8
    # floor
    c.line([(x + 20, floor), (x + w - 20, floor)], fill=(52, 66, 90), width=2)
    draw_flame(c, sx, sy, w * 0.055, h * 0.46, seed=6)
    # target plates
    plates = [(sx + 140, 0.86, "20 kW/m²", RED), (sx + 300, 0.72, "9 kW/m²", AMBER),
              (sx + 490, 0.58, "4 kW/m²", TEAL)]
    for px, hf, lab, col in plates:
        ph = (floor - y - 76) * hf
        c.rect(px, floor - ph, 10, ph, fill=(120, 134, 154))
        c.rect(px - 3, floor - ph - 6, 16, 6, fill=(150, 164, 184))
        c.arrow(sx + 26, sy - 20, px - 6, floor - ph * 0.72, fill=col, width=1.4, head=7, dash=5)
        tag_chip(c, px - 24, floor - ph - 46, lab, col, size=11)
    c.text(x + 24, y + 20, "FLUX FALLS WITH DISTANCE SQUARED", size=12, color=MUTED,
           fname="Inter-SemiBold", track=0.9)
    c.text(x + 24, floor + 20, "Radiant heat travels in straight lines: the plate that ignites is the plate the flame can see.",
           size=12, color=DIM, fname="Inter-Regular")
    # irradiance scale at bottom
    c.text(x + w - 24, y + 20, "q″ = εσT⁴", size=20, color=EMBER, fname="Serif-Regular", anchor="ra")


def convection_diagram(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(13, 19, 31), outline=(40, 54, 78), r=12)
    g = room(c, x + 26, y + 30, w - 52, h - 86, layer_frac=0.30, layer_temp=0.45,
             fire_x=0.34, flames=h * 0.24, seed=4)
    # plume arrows
    for k in range(3):
        px = g["fx"] - 14 + k * 14
        c.arrow(px, g["floor"] - h * 0.28, px + 4, g["ceil"] + 16, fill=AMBER, width=2.2, head=9)
    # ceiling jet arrows
    for k in range(3):
        c.arrow(g["fx"] + 40 + k * 70, g["ceil"] + 16, g["fx"] + 96 + k * 70, g["ceil"] + 16,
                fill=(255, 160, 70), width=1.8, head=8)
    # exit arrow at right opening
    c.arrow(g["x"] + g["w"] - 10, g["ceil"] + 26, g["x"] + g["w"] + 44, g["ceil"] + 26,
            fill=EMBER, width=2.4, head=9)
    tag_chip(c, g["x"] + g["w"] + 8, g["ceil"] + 46, "HOT GAS OUT", EMBER, size=11)
    tag_chip(c, g["fx"] + 20, g["floor"] - 120, "PLUME", AMBER, size=11)
    c.text(x + 24, y + 12, "q = h A ΔT", size=18, color=TEAL, fname="Serif-Regular")
    c.text(x + w - 24, y + h - 28, "Most of the energy leaves as hot gas through the openings.",
           size=12, color=MUTED, fname="Inter-Regular", anchor="ra")
# ---------------------------------------------------------------- tetrahedron
def tetrahedron(c, x, y, w, h):
    s = min((h - 150) / 3.0, (w * 0.5 - 210) / 1.9)
    cx, cy = x + w * 0.50, y + h * 0.50 + s * 0.02
    A = (cx, cy - s * 0.80)
    B = (cx - s * 0.92, cy + s * 0.42)
    C = (cx + s * 0.92, cy + s * 0.42)
    D = (cx - s * 0.10, cy + s * 0.96)

    back = ((A, B, C), (255, 176, 32), "HEAT")
    left = ((A, B, D), (255, 107, 26), "FUEL")
    right = ((A, C, D), (45, 212, 191), "OXYGEN")
    bottom = ((B, C, D), (229, 72, 77), "CHAIN")

    def fillf(pts, col, a):
        with_alpha(c, lambda d, sc: d.polygon([(p[0] * sc, p[1] * sc) for p in pts], fill=col + (a,)))

    fillf(back[0], back[1], 20)
    fillf(bottom[0], bottom[1], 46)
    fillf(left[0], left[1], 52)
    fillf(right[0], right[1], 42)
    # hidden edge B-C drawn dashed behind the front faces
    dotted_pts = [B, C]
    for k in range(24):
        t0, t1 = k / 24, (k + 0.55) / 24
        c.line([(B[0] + (C[0] - B[0]) * t0, B[1] + (C[1] - B[1]) * t0),
                (B[0] + (C[0] - B[0]) * t1, B[1] + (C[1] - B[1]) * t1)],
               fill=(120, 132, 150), width=1)
    for pts, col, _ in (left, right, bottom):
        c.line(list(pts) + [pts[0]], fill=col, width=2.0)
    c.line([A, B], fill=back[1], width=1.6)
    c.line([A, C], fill=back[1], width=1.6)

    def centroid(pts):
        return (sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3)

    labels = [
        (back, "HEAT", "energy to start and sustain", (cx - s * 0.02, cy - s * 1.22), "mm", "top"),
        (left, "FUEL", "solid, liquid or gas", (cx - s * 1.72, cy + s * 0.10), "rm", "side"),
        (right, "OXYGEN", "the oxidiser in air", (cx + s * 1.72, cy + s * 0.10), "lm", "side"),
        (bottom, "CHEMICAL CHAIN REACTION", "radical branching keeps the flame alive",
         (cx - s * 0.06, cy + s * 1.50), "mm", "bot"),
    ]
    for (pts, col, _), title, sub, (lx, ly), anc, pos in labels:
        fcx, fcy = centroid(pts)
        target = (lx, ly + 18) if pos == "top" else ((lx, ly - 30) if pos == "bot" else (lx + (12 if anc == "lm" else -12), ly + 12))
        c.line([(fcx, fcy), target], fill=col, width=1.2)
        c.ellipse(fcx - 5, fcy - 5, 10, 10, fill=col)
        c.text(lx, ly - 24, title, size=21, color=col, fname="Inter-SemiBold", anchor=anc, track=0.6)
        c.text(lx, ly + 2, sub, size=13, color=MUTED, fname="Inter-Regular", anchor=anc)
    c.text(x + w / 2, y + h - 4,
           "Four faces, four requirements — remove any one and flaming combustion stops",
           size=17, color=MUTED, fname="Inter-Regular", anchor="mm")


def smoke_layer(c, x, y, w, h):
    rw, rh = w * 0.655, h * 0.62
    rx, ry = x + w * 0.005, y + h * 0.05
    g = room(c, rx, ry, rw, rh, layer_frac=0.46, layer_temp=0.58, fire_x=0.24,
             flames=rh * 0.22, seed=9, door=(0.9, 0.42))
    # door jet arrows
    for k in range(3):
        yy = g["ceil"] + rh * (0.10 + k * 0.07)
        c.arrow(g["x"] + g["w"] - 6, yy, g["x"] + g["w"] + 46, yy, fill=EMBER, width=2, head=8)
    for k in range(3):
        yy = g["floor"] - 16 - k * 14
        c.arrow(g["x"] + g["w"] + 46, yy, g["x"] + g["w"] - 6, yy, fill=TEAL, width=2, head=8)
    np_y = g["floor"] - rh * 0.42
    c.line([(g["x"] + g["w"] - 4, np_y), (g["x"] + g["w"] + 52, np_y)], fill=WHITE, width=1.4)
    c.ellipse(g["x"] + g["w"] + 46, np_y - 4, 8, 8, fill=WHITE)
    # right-hand annotations
    ax = x + w * 0.715
    c.panel(ax, y + 20, w * 0.275, h * 0.72, fill=(14, 20, 31), outline=(40, 54, 78), r=12)
    c.text(ax + 22, y + 40, "READING THE LAYER", size=12, color=AMBER, fname="Inter-SemiBold", track=1.2)
    items = [("Interface height", "depth of hot gas above the floor", AMBER),
             ("Layer temperature", "300–700 °C in a developed fire", EMBER),
             ("Neutral plane", "height of pressure reversal at an opening", WHITE),
             ("Smoke velocity", "rising velocity means a growing fire", TEAL),
             ("Colour and density", "fuel type, soot yield, under-ventilation", MUTED)]
    ty = y + 70
    for a, b, col in items:
        c.rect(ax + 22, ty + 7, 6, 6, fill=col, r=1)
        c.text(ax + 38, ty, a, size=15, color=TEXT, fname="Inter-SemiBold")
        c.text(ax + 38, ty + 20, b, size=13, color=MUTED, fname="Inter-Regular", maxw=w * 0.26)
        ty += 54
    # interface annotation inside the room
    iy = g["ceil"] + (g["floor"] - g["ceil"]) * 0.46
    c.text(g["x"] + 24, iy - 26, "HOT LAYER  400–600 °C", size=13, color=AMBER,
           fname="Inter-SemiBold", track=0.6)
    c.text(g["x"] + 24, g["floor"] - 40, "LOWER LAYER — cooler and clearer, still contaminated",
           size=13, color=TEAL, fname="Inter-Medium")
    c.text(x, y + h - 26,
           "Two-layer model: the height of the interface is the single most useful measure of fire severity.",
           size=16, color=MUTED, fname="Inter-Regular")


def plume_zones(c, x, y, w, h):
    gx = x + w * 0.30
    base = y + h - 40
    top = y + 10
    # ambient
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    draw_flame(c, gx, base, 70, h * 0.22, seed=11)
    # plume widening
    for i, (frac, col, lab) in enumerate([
            (0.16, (255, 240, 200), "CONTINUOUS FLAME"),
            (0.46, (255, 150, 50), "INTERMITTENT FLAME"),
            (1.0, (150, 160, 175), "BUOYANT PLUME")]):
        pass
    # plume body
    def plume_shape(y0, y1, w0, w1, n=36):
        pts_l, pts_r = [], []
        for i in range(n):
            t = i / (n - 1)
            yy = y0 + (y1 - y0) * t
            half = (w0 + (w1 - w0) * t ** 0.8) / 2
            wob = 8 * math.sin(t * 7 + 1.4) * t
            pts_l.append((gx + wob - half, yy))
            pts_r.append((gx + wob + half, yy))
        return pts_l + pts_r[::-1]
    # zones as bands
    z1 = (base - h * 0.24, base)
    z2 = (y + h * 0.36, base - h * 0.24)
    with_alpha(c, lambda d, sc: d.polygon([(p[0] * sc, p[1] * sc) for p in plume_shape(*z1, 70, 120)],
                                          fill=(255, 220, 150, 120)))
    with_alpha(c, lambda d, sc: d.polygon([(p[0] * sc, p[1] * sc) for p in plume_shape(*z2, 120, 260)],
                                          fill=(255, 140, 60, 80)))
    with_alpha(c, lambda d, sc: d.polygon([(p[0] * sc, p[1] * sc) for p in plume_shape(y + h * 0.08, y + h * 0.36, 260, 420)],
                                          fill=(150, 160, 180, 70)))
    # entrainment arrows
    for side in (-1, 1):
        for k in range(4):
            yy = base - h * (0.34 + k * 0.12)
            xx = gx + side * (150 + k * 40)
            c.arrow(xx + side * 50, yy, xx, yy, fill=(110, 180, 190), width=1.5, head=8)
    c.text(gx - 40, base - h * 0.11, "CONTINUOUS\nFLAME", size=14, color=(255, 226, 170),
           fname="Inter-SemiBold", anchor="rm", spacing=1.2)
    c.text(gx - 210, base - h * 0.32, "INTERMITTENT\nFLAME ZONE", size=14, color=(255, 160, 80),
           fname="Inter-SemiBold", anchor="rm", spacing=1.2)
    c.text(gx - 250, base - h * 0.60, "BUOYANT\nPLUME", size=14, color=(170, 182, 198),
           fname="Inter-SemiBold", anchor="rm", spacing=1.2)
    # temperature profile
    px0 = x + w * 0.72
    c.line([(px0, y + h * 0.14), (px0, base)], fill=(60, 76, 100), width=1.2)
    c.text(px0, y + h * 0.10, "TEMPERATURE", size=12, color=MUTED, fname="Inter-Medium", anchor="ma", track=1)
    temp_pts = []
    for i in range(30):
        t = i / 29
        yy = base - t * h * 0.94
        val = 1100 * math.exp(-t * 1.25) + 60
        temp_pts.append((px0 + (val / 1200) * (w * 0.20), yy))
    c.line(temp_pts, fill=EMBER, width=2.5)
    c.text(px0 + (1100 / 1200) * (w * 0.20) + 8, base - h * 0.06, "1100 °C", size=12, color=EMBER,
           fname="Mono-Regular", anchor="lm")
    c.text(px0 + (600 / 1200) * (w * 0.20) + 8, base - h * 0.50, "600 °C", size=12, color=MUTED,
           fname="Mono-Regular", anchor="lm")
    c.text(gx, y + h - 10, "Entrained air roughly triples the plume mass flow every few metres of rise",
           size=14, color=DIM, fname="Inter-Regular", anchor="ma")


def ceiling_jet(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    g = room(c, x + 24, y + 24, w - 48, h - 70, layer_frac=0.26, layer_temp=0.35, fire_x=0.24,
             flames=h * 0.2, seed=13)
    ceil = g["ceil"]
    c.arrow(g["fx"] + 10, g["floor"] - h * 0.24, g["fx"] + 10, ceil + 12, fill=AMBER, width=2.5, head=10)
    for k in range(1, 7):
        px = g["fx"] + k * (g["w"] - g["fx"]) / 7
        c.arrow(g["fx"] + 14 + (k - 1) * 60, ceil + 14, g["fx"] + 14 + k * 60, ceil + 14,
                fill=(255, 170, 60), width=2, head=8)
    for k in range(1, 5):
        c.arrow(g["fx"] - 14 - (k - 1) * 50, ceil + 14, g["fx"] - 14 - k * 50, ceil + 14,
                fill=(255, 170, 60), width=2, head=8)
    c.text(g["fx"] + 6, ceil + 40, "CEILING JET", size=13, color=AMBER, fname="Inter-SemiBold", anchor="ma", track=1)
    # temperature decay curve overlay
    xs = [(g["fx"] + 30 + i * 14, ceil + 46 + 30 * (1 - math.exp(-i * 0.06)) + i * 1.2) for i in range(26)]
    c.text(g["x"] + 26, g["y"] + 46, "ΔT  ∝  Q^(2/3) / H^(5/3)  near the plume", size=15,
           color=MUTED, fname="Serif-Regular")
    c.text(g["x"] + 26, g["y"] + 70, "ΔT  ∝  (Q/r)^(2/3)  away from it", size=15, color=MUTED, fname="Serif-Regular")
    # sprinkler
    sx = g["x"] + g["w"] * 0.72
    c.line([(sx, ceil), (sx, ceil + 22)], fill=(140, 152, 170), width=2)
    c.ellipse(sx - 5, ceil + 20, 10, 7, fill=(200, 120, 60))


def smoke_composition(c, x, y, w, h):
    # concentric distribution
    cx, cy = x + w * 0.30, y + h * 0.46
    r = min(w * 0.24, h * 0.36)
    parts = [("SOOT", 0.30, (128, 138, 154)), ("CO / CO₂", 0.28, (190, 88, 78)), ("HCN / HCl", 0.14, (150, 112, 152)),
             ("IRRITANTS", 0.16, (196, 148, 84)), ("VAPOUR / FUEL", 0.12, (86, 156, 146))]
    a0 = -90
    for lab, frac, col in parts:
        a1 = a0 + frac * 360
        c.d.arc([c.s(cx - r), c.s(cy - r), c.s(cx + r), c.s(cy + r)], a0, a1,
                fill=col, width=int(28 * c.sc))
        a0 = a1
    c.text(cx, cy - 10, "SMOKE", size=22, color=TEXT, fname="Serif-Bold", anchor="mm")
    c.text(cx, cy + 16, "an aerosol", size=13, color=MUTED, fname="Inter-Medium", anchor="mm")
    ly = y + 40
    for lab, frac, col in parts:
        c.rect(x + w * 0.62, ly, 12, 12, fill=col, r=3)
        c.text(x + w * 0.62 + 22, ly + 6, lab, size=15, color=TEXT, fname="Inter-Medium", anchor="lm")
        c.text(x + w * 0.62 + 150, ly + 6, f"{frac*100:.0f}%", size=14, color=MUTED,
               fname="Mono-Regular", anchor="lm")
        ly += 34
    c.text(x + w * 0.62, ly + 32, "Typical composition varies\nwith fuel, temperature\nand ventilation.",
           size=14, color=DIM, fname="Inter-Regular", spacing=1.35)


def energy_balance(c, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    bw, bh = w * 0.30, h * 0.26
    c.panel(cx - bw / 2, cy - bh / 2, bw, bh, fill=(30, 22, 20), outline=EMBER, r=10)
    c.text(cx, cy - 10, "COMBUSTION", size=17, color=EMBER, fname="Inter-SemiBold", anchor="mm", track=1.2)
    c.text(cx, cy + 16, "Q (kW)", size=22, color=TEXT, fname="Serif-Regular", anchor="mm")
    outs = [("STORED in gases\nand structure", -1, -1, TEAL),
            ("LOST through walls\n(conduction, radiation)", 1, -1, BLUE),
            ("LOST through openings\n(convection)", 1, 1, AMBER),
            ("RADIATED to floor\nand exposures", -1, 1, RED)]
    for lab, sx, sy, col in outs:
        tx, ty = cx + sx * w * 0.30, cy + sy * h * 0.30
        c.panel(tx - 130, ty - 40, 260, 80, fill=(16, 23, 36), outline=(44, 58, 82), r=8)
        c.text(tx, ty, lab, size=14, color=col, fname="Inter-Medium", anchor="mm", spacing=1.3)
        x0 = cx + sx * (bw / 2 + 6)
        y0 = cy + sy * (bh / 2 + 6)
        x1 = tx + (-sx) * 130
        y1 = ty + (-sy) * 40
        c.arrow(x0, y0, x1, y1, fill=col, width=2, head=10)
    c.text(cx, y + h - 14, "A well-insulated compartment stores more energy — and gets hotter.",
           size=16, color=MUTED, fname="Inter-Regular", anchor="ma")


def vent_flow(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    g = room(c, x + 20, y + 20, w * 0.60, h - 60, layer_frac=0.44, layer_temp=0.52, fire_x=0.30,
             flames=h * 0.22, seed=17, door=(0.9, 0.52))
    xr = g["x"] + g["w"]
    dh = g["h"] * 0.52
    for k in range(3):
        yy = g["floor"] - dh + 20 + k * 24
        c.arrow(xr - 4, yy, xr + 52, yy, fill=EMBER, width=2.2, head=9)
    for k in range(3):
        yy = g["floor"] - 22 - k * 22
        c.arrow(xr + 52, yy, xr - 4, yy, fill=TEAL, width=2.2, head=9)
    tag_chip(c, xr + 58, g["floor"] - dh + 8, "HOT GAS OUT", EMBER, size=11)
    tag_chip(c, xr + 58, g["floor"] - 34, "AIR IN", TEAL, size=11)
    # formula card
    ax = x + w * 0.70
    c.panel(ax, y + 24, w * 0.28, h - 70, fill=(15, 22, 35), outline=(40, 54, 78), r=10)
    c.text(ax + 18, y + 44, "VENTILATION FACTOR", size=12, color=AMBER, fname="Inter-SemiBold", track=1.1)
    c.text(ax + 18, y + 76, "A√H", size=44, color=TEXT, fname="Serif-Regular")
    c.text(ax + 18, y + 140, "A   opening area (m²)", size=13, color=MUTED, fname="Inter-Regular")
    c.text(ax + 18, y + 162, "H   opening height (m)", size=13, color=MUTED, fname="Inter-Regular")
    c.line([(ax + 18, y + 190), (ax + w * 0.28 - 18, y + 190)], fill=(44, 58, 82), width=1)
    c.text(ax + 18, y + 208, "ṁ_air ≈ 0.5 A√H", size=16, color=TEAL, fname="Serif-Regular")
    c.text(ax + 18, y + 234, "kg/s", size=12, color=MUTED, fname="Inter-Regular")
    c.text(ax + 18, y + 262, "Q_max ≈ 1 500 A√H", size=16, color=EMBER, fname="Serif-Regular")
    c.text(ax + 18, y + 288, "kW", size=12, color=MUTED, fname="Inter-Regular")
    c.text(ax + 18, y + 322, "Height matters: doubling H\nraises flow by only 41 %.", size=12,
           color=MUTED, fname="Inter-Regular", spacing=1.3, maxw=w * 0.25)
# ---------------------------------------------------------------- sequences
def seq_panels(c, x, y, w, h, items, color=EMBER, arrow=True):
    n = len(items)
    gap = 18
    pw = (w - gap * (n - 1)) / n
    for i, (title, body) in enumerate(items):
        px = x + i * (pw + gap)
        c.panel(px, y, pw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.text(px + 18, y + 16, f"{i+1:02d}", size=13, color=color, fname="Mono-Bold", anchor="la")
        c.text(px + 18, y + 40, title.upper(), size=14, color=color, fname="Inter-SemiBold", track=0.9, maxw=pw - 36)
        c.text(px + 18, y + 74, body, size=15, color=TEXT, fname="Inter-Regular", maxw=pw - 36, spacing=1.32)
        if arrow and i < n - 1:
            c.arrow(px + pw + 2, y + h / 2, px + pw + gap - 3, y + h / 2, fill=(90, 108, 136), width=1.6, head=7)


def flashover_seq(c, x, y, w, h):
    items = [
        ("GROWTH", "Fire localised. Layer forms and descends.\nFuel surfaces preheat.", "600 °C"),
        ("PRE-FLASHOVER", "Rollover in the layer. Radiant flux at\nfloor approaches 20 kW/m².", "800 °C"),
        ("TRANSITION", "Exposed surfaces pyrolyse together;\nflames sweep the compartment.", "1 000 °C"),
        ("FULLY DEVELOPED", "Whole compartment alight.\nVentilation-controlled. Unsurvivable.", "> 1 100 °C"),
    ]
    gap = 18
    n = len(items)
    pw = (w - gap * (n - 1)) / n
    for i, (title, body, temp) in enumerate(items):
        px = x + i * (pw + gap)
        c.panel(px, y, pw, h, fill=(16, 23, 37), outline=(40, 54, 78), r=12)
        c.text(px + 18, y + 16, f"{i+1:02d}", size=13, color=EMBER, fname="Mono-Bold", anchor="la")
        c.text(px + pw - 18, y + 16, temp, size=15, color=([TEAL, AMBER, EMBER, RED][i]),
               fname="Mono-Bold", anchor="ra")
        c.text(px + 18, y + 40, title, size=13, color=EMBER, fname="Inter-SemiBold", track=0.9, maxw=pw - 36)
        c.text(px + 18, y + 64, body, size=14, color=TEXT, fname="Inter-Regular", maxw=pw - 36, spacing=1.3)
        # illustration inside the panel
        gx, gy = px + 14, y + 132
        gw, gh = pw - 28, h - 176
        c.panel(gx, gy, gw, gh, fill=(9, 13, 21), outline=(34, 46, 66), r=8)
        frac = [0.16, 0.34, 0.56, 0.74][i]
        tempf = [0.22, 0.42, 0.66, 0.88][i]
        layer(c, gx + 1, gy + 1, gw - 2, gh - 2, frac, tempf, seed=i + 5, interface=True)
        nf = [1, 2, 3, 4][i]
        for k in range(nf):
            fx = gx + gw * (0.22 + 0.56 * k / max(1, nf - 1)) if nf > 1 else gx + gw * 0.5
            draw_flame(c, fx, gy + gh - 8, gw * 0.12, gh * (0.16 + i * 0.09), seed=i * 3 + k + 2)
        if i < n - 1:
            c.arrow(px + pw + 2, y + h / 2, px + pw + gap - 3, y + h / 2,
                    fill=(90, 108, 136), width=1.6, head=7)


def backdraft_seq(c, x, y, w, h):
    seq_panels(c, x, y, w, h, [
        ("UNDER-VENTILATED FIRE", "Hot, fuel-rich, oxygen-poor. No visible flame. Pulsing smoke, sooty glass."),
        ("OPENING MADE", "Air enters as a gravity current along the floor and mixes with pyrolysis gases."),
        ("IGNITION OF THE MIXTURE", "Deflagration at the ceiling; pressure rises rapidly in the compartment."),
        ("PRESSURE RELEASE", "Fireball expelled through the opening — often where the crew is standing."),
    ], RED)


def spread_paths(c, x, y, w, h):
    c.panel(x, y, w, h, fill=(12, 18, 29), outline=(40, 54, 78), r=12)
    bx, by, bw, bh = x + 90, y + 60, w - 180, h - 150
    c.rect(bx, by, bw, bh, outline=(70, 86, 112), width=1.5)
    c.line([(bx, by + bh * 0.62), (bx + bw, by + bh * 0.62)], fill=(70, 86, 112), width=1)
    # source fire
    draw_flame(c, bx + bw * 0.22, by + bh * 0.62, 34, bh * 0.2, seed=2)
    pts = [(bx + bw * 0.22, by + bh * 0.62)]
    # 1 direct flame
    draw_flame(c, bx + bw * 0.34, by + bh * 0.62, 30, bh * 0.18, seed=5)
    c.arrow(bx + bw * 0.235, by + bh * 0.55, bx + bw * 0.31, by + bh * 0.55, fill=AMBER, width=2, head=8)
    # 2 radiation
    c.arrow(bx + bw * 0.25, by + bh * 0.45, bx + bw * 0.62, by + bh * 0.30, fill=EMBER, width=2, head=9, dash=7)
    # 3 convection
    c.arrow(bx + bw * 0.24, by + bh * 0.44, bx + bw * 0.45, by + bh * 0.10, fill=AMBER, width=2, head=9)
    c.arrow(bx + bw * 0.45, by + bh * 0.10, bx + bw * 0.85, by + bh * 0.10, fill=AMBER, width=2, head=9)
    # 4 conduction
    c.rect(bx + bw * 0.66, by + bh * 0.05, 10, bh * 0.9, fill=STEEL)
    c.arrow(bx + bw * 0.30, by + bh * 0.66, bx + bw * 0.66, by + bh * 0.66, fill=TEAL, width=2, head=8, dash=5)
    # 5 transport of burning material
    c.arrow(bx + bw * 0.24, by + bh * 0.72, bx + bw * 0.80, by + bh * 0.78, fill=VIOLET, width=2, head=8, dash=4)
    labels = [("1  DIRECT FLAME", AMBER, bx + bw * 0.30, by + bh * 0.50),
              ("2  RADIATION", EMBER, bx + bw * 0.55, by + bh * 0.40),
              ("3  CONVECTION", AMBER, bx + bw * 0.62, by + bh * 0.16),
              ("4  CONDUCTION", TEAL, bx + bw * 0.50, by + bh * 0.70),
              ("5  BURNING MATERIAL", VIOLET, bx + bw * 0.55, by + bh * 0.84)]
    for lab, col, lx, ly in labels:
        tag_chip(c, lx, ly, lab, col, size=12)
    c.text(x + 24, y + h - 34, "Identify the active mechanism — it tells you which barrier to defend.",
           size=16, color=MUTED, fname="Inter-Regular")


# ---------------------------------------------------------------- warehouse
def warehouse(c, x, y, w, h, layer_frac=0.0, layer_temp=0.2, fires=None, vents=0, doors=0,
              labels=True, arrows=False, sprinkler=False, seed=21, show_tiers=True):
    """Sectional warehouse: 60 m x 9 m, four six-tier racks, doors and roof vents."""
    fires = fires or []
    bx, by = x, y
    bw, bh = w, h * 0.82
    floor = by + bh - 10
    roof = by
    # interior
    c.rect(bx, roof, bw, bh, fill=(14, 20, 31))
    c.rect(bx, roof, 10, bh, fill=(46, 60, 84))
    c.rect(bx + bw - 10, roof, 10, bh, fill=(46, 60, 84))
    c.rect(bx, floor, bw, 10, fill=(34, 45, 62))
    # end-wall door openings
    dh = bh * 0.46
    if doors >= 1:
        c.rect(bx + 10, floor - dh, 30, dh, fill=(8, 12, 19))
        c.rect(bx + 10, floor - dh - 6, 30, 8, fill=(70, 86, 112))
        for k in range(8):
            yy = floor - 12 - k * (dh - 26) / 8
            c.line([(bx + 12, yy), (bx + 38, yy)], fill=(40, 53, 74), width=1)
    if doors >= 2:
        c.rect(bx + bw - 40, floor - dh, 30, dh, fill=(8, 12, 19))
        c.rect(bx + bw - 40, floor - dh - 6, 30, 8, fill=(70, 86, 112))
    # racks
    rack_positions = []
    n_racks = 4
    tiers = 6
    rack_top = by + bh * 0.14
    rack_h = floor - rack_top
    for i in range(n_racks):
        rx = bx + bw * (0.115 + i * 0.215)
        rw = bw * 0.115
        rack_positions.append((rx, rw, rack_top, rack_h))
        c.rect(rx - 3, rack_top, rw + 6, rack_h, fill=(24, 32, 46))
        c.rect(rx, rack_top, 4, rack_h, fill=STEEL)
        c.rect(rx + rw - 4, rack_top, 4, rack_h, fill=STEEL)
        for t_i in range(tiers + 1):
            ty = rack_top + rack_h * t_i / tiers
            c.rect(rx - 2, ty, rw + 4, 3, fill=(104, 120, 144))
        for t_i in range(tiers):
            ty = rack_top + rack_h * (t_i + 0.30) / tiers
            for k in range(3):
                gw = rw / 3.6
                col = CARDBOARD if (k + t_i * 2) % 3 else PLASTIC
                c.rect(rx + 5 + k * (gw + 3), ty - rack_h / tiers * 0.40, gw, rack_h / tiers * 0.46,
                       fill=col, r=2)
    # roof deck + columns
    c.rect(bx, roof - 4, bw, 18, fill=(58, 74, 100))
    for i in range(int(bw / 36)):
        c.line([(bx + i * 36, roof - 4), (bx + i * 36 + 16, roof + 14)], fill=(76, 94, 122), width=1)
    for i in range(1, 6):
        cx = bx + bw * i / 6
        c.rect(cx - 3, roof + 14, 6, bh - 24, fill=(48, 62, 84))
    # fires
    for (ri, tier, size) in fires:
        rx, rw, rt, rh = rack_positions[min(ri, n_racks - 1)]
        fy = rt + rh * (tier + 0.95) / tiers
        fx = rx + rw * 0.5
        draw_flame(c, fx, fy, max(16, rw * 0.30), size, seed=ri + tier + 5)
    # smoke
    if layer_frac > 0:
        layer(c, bx + 10, roof + 14, bw - 20, floor - roof - 14, layer_frac, layer_temp, seed=seed, alpha=200)
    # vents
    for i in range(4):
        vx = bx + bw * (0.16 + i * 0.22)
        vw = bw * 0.045
        opened = i < vents
        if opened:
            c.rect(vx, roof - 26, vw, 26, fill=(10, 15, 24))
            c.rect(vx - 3, roof - 30, vw + 6, 4, fill=(130, 146, 172))
            for k in range(3):
                c.arrow(vx + vw * (0.2 + k * 0.3), roof - 34, vx + vw * (0.2 + k * 0.3) - 8,
                        roof - 74, fill=(150, 162, 184), width=2, head=8)
        else:
            c.rect(vx, roof - 6, vw, 6, fill=(70, 86, 112))
    if sprinkler:
        for i in range(10):
            sx = bx + bw * (0.05 + i * 0.10)
            c.line([(sx, roof + 14), (sx, roof + 34)], fill=(150, 162, 180), width=1.6)
            c.ellipse(sx - 4, roof + 34, 9, 5, fill=(212, 122, 60))
    if labels:
        c.line([(bx, floor + 24), (bx + bw, floor + 24)], fill=(70, 86, 112), width=1)
        for xx in (bx, bx + bw):
            c.line([(xx, floor + 18), (xx, floor + 30)], fill=(70, 86, 112), width=1)
        c.text(bx + bw / 2, floor + 40, "60 m", size=13, color=MUTED, fname="Mono-Regular", anchor="ma")
        c.line([(bx + bw + 24, roof), (bx + bw + 24, floor)], fill=(70, 86, 112), width=1)
        c.text(bx + bw + 34, (roof + floor) / 2, "9 m", size=13, color=MUTED, fname="Mono-Regular", anchor="lm")
    return dict(x=bx, y=by, w=bw, h=bh, floor=floor, roof=roof + 14, racks=rack_positions, tiers=tiers)


