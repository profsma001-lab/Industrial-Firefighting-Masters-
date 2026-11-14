# -*- coding: utf-8 -*-
"""Minimal scientific chart engine drawn with PIL, in the deck's visual language."""
import math
import numpy as np
from PIL import Image, ImageDraw
from lib import (Canvas, TEXT, MUTED, DIM, LINE, EMBER, AMBER, RED, TEAL, BLUE,
                 VIOLET, PAL, font)


class Chart:
    def __init__(self, c: Canvas, x, y, w, h, xlim, ylim, xlabel="", ylabel="",
                 xticks=None, yticks=None, xlog=False, ylog=False,
                 grid=True, yfmt=None, xfmt=None, pad_l=86, pad_b=58, pad_t=18, pad_r=22,
                 ytitle_size=16, xtitle_size=16):
        self.c, self.x, self.y, self.w, self.h = c, x, y, w, h
        self.xlim, self.ylim = xlim, ylim
        self.xlog, self.ylog = xlog, ylog
        self.pl, self.pb, self.pt, self.pr = pad_l, pad_b, pad_t, pad_r
        self.px0, self.py0 = x + pad_l, y + pad_t          # top-left of plot
        self.pw, self.ph = w - pad_l - pad_r, h - pad_t - pad_b
        self.xlabel, self.ylabel = xlabel, ylabel
        self.xticks, self.yticks = xticks, yticks
        self.yfmt = yfmt or (lambda v: f"{v:g}")
        self.xfmt = xfmt or (lambda v: f"{v:g}")
        self.ylabel_size, self.xlabel_size = ytitle_size, xtitle_size
        self._axes(grid)

    # ---------------------------------------------------- transforms
    def tx(self, xv):
        if self.xlog:
            a, b = math.log10(self.xlim[0]), math.log10(self.xlim[1])
            t = (math.log10(max(xv, 1e-9)) - a) / (b - a)
        else:
            t = (xv - self.xlim[0]) / (self.xlim[1] - self.xlim[0])
        return self.px0 + t * self.pw

    def ty(self, yv):
        if self.ylog:
            a, b = math.log10(self.ylim[0]), math.log10(self.ylim[1])
            t = (math.log10(max(yv, 1e-9)) - a) / (b - a)
        else:
            t = (yv - self.ylim[0]) / (self.ylim[1] - self.ylim[0])
        return self.py0 + self.ph - t * self.ph

    # ---------------------------------------------------- axes
    def _axes(self, grid=True):
        c = self.c
        x0, y0 = self.px0, self.py0
        x1, y1 = x0 + self.pw, y0 + self.ph
        # plot background
        c.rect(x0, y0, self.pw, self.ph, fill=(13, 19, 31))
        if grid:
            for gv in (self.yticks if self.yticks is not None else self._auto(self.ylim, self.ylog)):
                yy = self.ty(gv)
                c.line([(x0, yy), (x1, yy)], fill=(30, 41, 59), width=0.8)
            for gv in (self.xticks if self.xticks is not None else self._auto(self.xlim, self.xlog)):
                xx = self.tx(gv)
                c.line([(xx, y0), (xx, y1)], fill=(30, 41, 59), width=0.8)
        # frame
        c.line([(x0, y0), (x0, y1)], fill=(58, 74, 100), width=1.2)
        c.line([(x0, y1), (x1, y1)], fill=(58, 74, 100), width=1.2)
        # ticks + labels
        for gv in (self.yticks if self.yticks is not None else self._auto(self.ylim, self.ylog)):
            yy = self.ty(gv)
            c.line([(x0 - 6, yy), (x0, yy)], fill=(78, 94, 120), width=1)
            c.text(x0 - 12, yy, self.yfmt(gv), size=15, color=MUTED, fname="Mono-Regular", anchor="rm")
        for gv in (self.xticks if self.xticks is not None else self._auto(self.xlim, self.xlog)):
            xx = self.tx(gv)
            c.line([(xx, y1), (xx, y1 + 6)], fill=(78, 94, 120), width=1)
            c.text(xx, y1 + 18, self.xfmt(gv), size=15, color=MUTED, fname="Mono-Regular", anchor="ma")
        # axis titles
        if self.xlabel:
            c.text(x0 + self.pw / 2, y1 + 42, self.xlabel, size=self.xlabel_size, color=DIM,
                   fname="Inter-Medium", anchor="ma", track=0.4)
        if self.ylabel:
            from lib import axis_label
            axis_label(c, x0 - 74, y0 + self.ph / 2, self.ylabel, color=DIM, size=self.ylabel_size, rot=90)

    def _auto(self, lim, log):
        a, b = lim
        if log:
            lo, hi = math.ceil(math.log10(a)), math.floor(math.log10(b))
            return [10 ** e for e in range(lo, hi + 1)]
        span = b - a
        step = 10 ** math.floor(math.log10(span / 5))
        for m in (1, 2, 2.5, 5, 10):
            if span / (step * m) <= 6.5:
                step *= m
                break
        vals = []
        v = math.ceil(a / step) * step
        while v <= b + 1e-9:
            vals.append(round(v, 10))
            v += step
        return vals

    # ---------------------------------------------------- series
    def _clip_seg(self, p, q):
        """Liang-Barsky clip of a segment against the plot rectangle."""
        x0, y0 = self.px0, self.py0
        x1, y1 = x0 + self.pw, y0 + self.ph
        (ax, ay), (bx, by) = p, q
        dx, dy = bx - ax, by - ay
        t0, t1 = 0.0, 1.0
        for pp, qq in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
            if abs(pp) < 1e-9:
                if qq < 0:
                    return None
                continue
            r = qq / pp
            if pp < 0:
                if r > t1:
                    return None
                if r > t0:
                    t0 = r
            else:
                if r < t0:
                    return None
                if r < t1:
                    t1 = r
        if t1 - t0 <= 1e-9:
            return None
        return ((ax + t0 * dx, ay + t0 * dy), (ax + t1 * dx, ay + t1 * dy))

    def _clip_path(self, pts):
        """Return a list of subpaths clipped to the plot rectangle."""
        subs, cur = [], []
        for i in range(len(pts) - 1):
            s = self._clip_seg(pts[i], pts[i + 1])
            if s is None:
                if len(cur) > 1:
                    subs.append(cur)
                cur = []
                continue
            if not cur:
                cur = [s[0], s[1]]
            elif math.hypot(cur[-1][0] - s[0][0], cur[-1][1] - s[0][1]) < 1.5:
                cur.append(s[1])
            else:
                if len(cur) > 1:
                    subs.append(cur)
                cur = [s[0], s[1]]
        if len(cur) > 1:
            subs.append(cur)
        return subs

    def line(self, xs, ys, color=EMBER, width=2.6, dash=None, label=None, smooth=True, z=1):
        pts = [(self.tx(a), self.ty(b)) for a, b in zip(xs, ys)]
        if smooth and len(pts) > 2:
            pts = _chaikin(pts, 2)
        for sub in self._clip_path(pts):
            if dash:
                self._dashed(sub, color, width, dash)
            else:
                self.c.line(sub, fill=color, width=width)
        if label:
            self._legend_items = getattr(self, "_legend_items", [])
            self._legend_items.append((label, color))

    def _dashed(self, pts, color, width, dash=8):
        acc, on = 0.0, True
        seg = []
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            L = math.hypot(x2 - x1, y2 - y1)
            if L == 0:
                continue
            n = max(1, int(L / dash))
            for k in range(n):
                t0, t1 = k / n, (k + 1) / n
                if on:
                    seg.append(((x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                                (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)))
                on = not on
        for a, b in seg:
            self.c.line([a, b], fill=color, width=width)

    def area(self, xs, ys, color=EMBER, alpha=42, base=None):
        base = base if base is not None else self.ylim[0]
        pts = [(self.tx(a), self.ty(b)) for a, b in zip(xs, ys)]
        poly = pts + [(self.tx(xs[-1]), self.ty(base)), (self.tx(xs[0]), self.ty(base))]
        ov = Image.new("RGB", self.c.img.size, color)
        mask = Image.new("L", self.c.img.size, 0)
        md = ImageDraw.Draw(mask)
        md.polygon([(self.c.s(a), self.c.s(b)) for a, b in poly], fill=alpha)
        self.c.img.paste(ov, (0, 0), mask)
        self.c.d = ImageDraw.Draw(self.c.img)

    def hline(self, yv, color=RED, width=1.6, dash=10, label=None, lab_side="right"):
        yy = self.ty(yv)
        if dash:
            self._dashed([(self.px0, yy), (self.px0 + self.pw, yy)], color, width, dash)
        else:
            self.c.line([(self.px0, yy), (self.px0 + self.pw, yy)], fill=color, width=width)
        if label:
            tw = self.c.text_width(label, 15, "Inter-SemiBold")
            lx = self.px0 + self.pw - tw - 10 if lab_side == "right" else self.px0 + 10
            self.c.rect(lx - 6, yy - 11, tw + 12, 22, fill=(11, 16, 26), r=4)
            self.c.text(lx, yy, label, size=15, color=color, fname="Inter-SemiBold", anchor="lm")

    def vline(self, xv, color=MUTED, width=1.6, dash=8, label=None, top=True):
        xx = self.tx(xv)
        if dash:
            self._dashed([(xx, self.py0), (xx, self.py0 + self.ph)], color, width, dash)
        else:
            self.c.line([(xx, self.py0), (xx, self.py0 + self.ph)], fill=color, width=width)
        if label:
            self.c.text(xx, self.py0 + 12, label, size=14, color=color, fname="Inter-SemiBold", anchor="ma")

    def band(self, x0, x1, color=(255, 255, 255), alpha=14):
        a, b = self.tx(x0), self.tx(x1)
        ov = Image.new("RGB", self.c.img.size, color)
        mask = Image.new("L", self.c.img.size, 0)
        md = ImageDraw.Draw(mask)
        md.rectangle([self.c.s(a), self.c.s(self.py0), self.c.s(b),
                      self.c.s(self.py0 + self.ph)], fill=alpha)
        self.c.img.paste(ov, (0, 0), mask)
        self.c.d = ImageDraw.Draw(self.c.img)

    def point(self, xv, yv, color=AMBER, r=5, ring=None, label=None, dx=12, dy=-14,
              size=14, lab_color=None):
        xx, yy = self.tx(xv), self.ty(yv)
        if ring:
            self.c.ellipse(xx - r - 5, yy - r - 5, 2 * (r + 5), 2 * (r + 5), outline=ring, width=1.2)
        self.c.ellipse(xx - r, yy - r, 2 * r, 2 * r, fill=color)
        if label:
            self.c.text(xx + dx, yy + dy, label, size=size, color=lab_color or color,
                        fname="Inter-SemiBold", anchor="lm")

    def tag(self, xv, yv, text, color=EMBER, dx=0, dy=-38, size=14, w=None):
        xx, yy = self.tx(xv) + dx, self.ty(yv) + dy
        tw = w or self.c.text_width(text, size, "Inter-SemiBold") + 22
        self.c.rect(xx - tw / 2, yy - 14, tw, 28, fill=(15, 21, 33), outline=color, r=6, width=1)
        self.c.text(xx, yy, text, size=size, color=color, fname="Inter-SemiBold", anchor="mm")

    def legend(self, x=None, y=None, items=None, size=14):
        items = items or getattr(self, "_legend_items", [])
        if not items:
            return
        x = self.px0 + 16 if x is None else x
        y = self.py0 + 18 if y is None else y
        bw = max(self.c.text_width(t, size, "Inter-Medium") for t, _ in items) + 46
        bh = len(items) * 24 + 12
        self.c.rect(x, y, bw, bh, fill=(12, 18, 29), outline=(38, 52, 76), r=8)
        for i, (t, col) in enumerate(items):
            yy = y + 18 + i * 24
            self.c.line([(x + 12, yy), (x + 30, yy)], fill=col, width=3)
            self.c.text(x + 38, yy, t, size=size, color=TEXT, fname="Inter-Medium", anchor="lm")


def _chaikin(pts, n=2):
    for _ in range(n):
        out = [pts[0]]
        for i in range(len(pts) - 1):
            p, q = pts[i], pts[i + 1]
            out.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
            out.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
        out.append(pts[-1])
        pts = out
    return pts


def smooth_curve(f, x0, x1, n=300):
    xs = np.linspace(x0, x1, n)
    return xs, np.array([f(v) for v in xs])


ALPHA = {"slow": 0.00293, "medium": 0.01172, "fast": 0.0469, "ultrafast": 0.1876}
