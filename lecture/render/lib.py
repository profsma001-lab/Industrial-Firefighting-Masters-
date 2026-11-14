# -*- coding: utf-8 -*-
"""Core drawing library for the IF 701 lecture deck."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(os.path.dirname(HERE), "assets", "fonts")
FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1920, 1080          # logical design space

# ---------------------------------------------------------------- palette
BG0 = (7, 11, 18)
BG1 = (12, 18, 30)
PANEL = (17, 24, 38)
PANEL2 = (22, 31, 48)
LINE = (38, 52, 76)
TEXT = (232, 238, 249)
MUTED = (143, 163, 192)
DIM = (99, 116, 143)
EMBER = (255, 107, 26)
AMBER = (255, 176, 32)
RED = (229, 72, 77)
TEAL = (45, 212, 191)
BLUE = (76, 141, 255)
VIOLET = (167, 139, 250)
WHITE = (255, 255, 255)

PAL = {"ember": EMBER, "amber": AMBER, "red": RED, "teal": TEAL,
       "blue": BLUE, "violet": VIOLET, "muted": MUTED, "text": TEXT, "white": WHITE}

_font_cache = {}
_fallback_cache = {}
_cov_cache = {}


def _coverage(path):
    if path not in _cov_cache:
        from fontTools.ttLib import TTFont
        f = TTFont(path, fontNumber=0, lazy=True)
        cps = set()
        for t in f["cmap"].tables:
            cps |= set(t.cmap.keys())
        _cov_cache[path] = cps
    return _cov_cache[path]


def font(name, size):
    key = (name, int(size))
    if key not in _font_cache:
        path = os.path.join(FONT_DIR, name + ".ttf")
        _font_cache[key] = ImageFont.truetype(path, int(size))
    return _font_cache[key]


def coverage_for(fname):
    return _coverage(os.path.join(FONT_DIR, fname + ".ttf"))


def fb(size, bold=False):
    key = ('fb', int(size), bold)
    if key not in _fallback_cache:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else FALLBACK
        _fallback_cache[key] = ImageFont.truetype(path, int(size))
    return _fallback_cache[key]


def _has(f, ch):
    try:
        return f.getmask(ch).getbbox() is not None or f.getlength(ch) > 0
    except Exception:
        return False


class Canvas:
    """Draws in a 1920x1080 logical space onto a supersampled image."""

    def __init__(self, scale=2, bg=None):
        self.sc = scale
        self.img = Image.new("RGB", (int(W * scale), int(H * scale)), bg or BG0)
        self.d = ImageDraw.Draw(self.img)
        self._cov = {}

    # -- primitives ---------------------------------------------------
    def s(self, v):
        return v * self.sc

    def rect(self, x, y, w, h, fill=None, outline=None, width=1, r=0):
        box = [self.s(x), self.s(y), self.s(x + w), self.s(y + h)]
        if r:
            self.d.rounded_rectangle(box, radius=self.s(r), fill=fill,
                                     outline=outline, width=max(1, int(self.s(width))))
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=max(1, int(self.s(width))))

    def line(self, pts, fill=LINE, width=1, joint="curve"):
        self.d.line([(self.s(x), self.s(y)) for x, y in pts], fill=fill,
                    width=max(1, int(self.s(width))), joint=joint)

    def ellipse(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.ellipse([self.s(x), self.s(y), self.s(x + w), self.s(y + h)], fill=fill,
                       outline=outline, width=max(1, int(self.s(width))))

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon([(self.s(x), self.s(y)) for x, y in pts], fill=fill, outline=outline,
                       width=max(1, int(self.s(width))))

    def arc(self, x, y, w, h, a0, a1, fill=LINE, width=2):
        self.d.arc([self.s(x), self.s(y), self.s(x + w), self.s(y + h)], a0, a1, fill=fill,
                   width=max(1, int(self.s(width))))

    def arrow(self, x1, y1, x2, y2, fill=EMBER, width=2.5, head=12, dash=None):
        ang = math.atan2(y2 - y1, x2 - x1)
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1:
            return
        hx, hy = x2 - head * 0.9 * math.cos(ang), y2 - head * 0.9 * math.sin(ang)
        if dash:
            n = max(1, int(L / (dash * 2)))
            for i in range(n):
                t0 = i * 2 * dash / L
                t1 = min(1.0, (i * 2 + 1) * dash / L)
                self.line([(x1 + (hx - x1) * t0, y1 + (hy - y1) * t0),
                           (x1 + (hx - x1) * t1, y1 + (hy - y1) * t1)], fill=fill, width=width)
        else:
            self.line([(x1, y1), (hx, hy)], fill=fill, width=width)
        p1 = (x2, y2)
        p2 = (x2 - head * math.cos(ang - 0.42), y2 - head * math.sin(ang - 0.42))
        p3 = (x2 - head * math.cos(ang + 0.42), y2 - head * math.sin(ang + 0.42))
        self.poly([p1, p2, p3], fill=fill)

    def arrow_curve(self, pts, fill=EMBER, width=2.5, head=12):
        self.line(pts, fill=fill, width=width)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ang = math.atan2(y2 - y1, x2 - x1)
        p2 = (x2 - head * math.cos(ang - 0.42), y2 - head * math.sin(ang - 0.42))
        p3 = (x2 - head * math.cos(ang + 0.42), y2 - head * math.sin(ang + 0.42))
        self.poly([(x2, y2), p2, p3], fill=fill)

    # -- text ---------------------------------------------------------
    def _runs(self, f, text, size, bold=False, fname=None):
        """Split text into (segment, font) runs by glyph coverage."""
        runs, cur, curf = [], "", None
        cov = coverage_for(fname) if fname else None
        fcov = _coverage(FALLBACK)
        for ch in text:
            if ch == "\u00a0":
                ch = " "
            if ch in " \t\n":
                ok = True
            elif cov is not None:
                ok = ord(ch) in cov
            else:
                ok = _has(f, ch)
            if not ok and ord(ch) not in fcov:
                ok = True
            use = f if ok else fb(size, bold)
            if curf is None or use is curf:
                cur += ch
                curf = use
            else:
                runs.append((cur, curf))
                cur, curf = ch, use
        if cur:
            runs.append((cur, curf))
        return runs

    def text(self, x, y, txt, size=24, color=TEXT, fname="Inter-Regular", anchor="la",
             spacing=1.35, bold=False, maxw=None, align="left", track=0.0):
        """Draw text; returns (width, height). Supports \\n lines and maxw wrapping."""
        f = font(fname, size * self.sc)
        lines = self._wrap(txt, f, size, maxw)
        lh = size * spacing
        # vertical anchoring
        total_h = lh * len(lines)
        if anchor[1] == "m":
            y = y - total_h / 2 + lh / 2
        elif anchor[1] == "b":
            y = y - total_h + lh / 2
        maxwid = 0
        for i, ln in enumerate(lines):
            lw = self.text_width(ln, size, fname, track)
            maxwid = max(maxwid, lw)
            if anchor[0] == "m" or align == "center":
                cx = x - lw / 2
            elif anchor[0] == "r" or align == "right":
                cx = x - lw
            else:
                cx = x
            self._draw_line(cx, y + i * lh, ln, size, color, fname, track, bold)
        return maxwid, total_h

    def _draw_line(self, x, cy, ln, size, color, fname, track, bold):
        f = font(fname, size * self.sc)
        cx = x
        for seg_txt, fnt in self._runs(f, ln, size * self.sc, bold, fname):
            self.d.text((self.s(cx), self.s(cy)), seg_txt, font=fnt, fill=color, anchor="lm")
            cx += fnt.getlength(seg_txt) / self.sc
            if track:
                cx += track * len(seg_txt)

    def _wrap(self, txt, f, size, maxw):
        out = []
        for para in str(txt).split("\n"):
            if maxw is None:
                out.append(para)
                continue
            words, line = para.split(" "), ""
            for wd in words:
                trial = (line + " " + wd).strip()
                if self.text_width(trial, size, f.name if False else None, 0, fnt=f) <= maxw or not line:
                    line = trial
                else:
                    out.append(line)
                    line = wd
            out.append(line)
        return out

    def text_width(self, txt, size, fname="Inter-Regular", track=0.0, fnt=None):
        from PIL import ImageFont
        if fnt is not None:
            # fnt is already scaled; measure with fallback awareness
            w = 0.0
            for ch in txt:
                w += fnt.getlength(ch)
            return w / self.sc
        f = font(fname, size * self.sc)
        w = 0.0
        for seg_txt, fnt2 in self._runs(f, txt, size * self.sc, False, fname):
            w += fnt2.getlength(seg_txt)
        return w / self.sc + track * max(0, len(txt) - 1)

    # -- composite helpers --------------------------------------------
    def panel(self, x, y, w, h, fill=PANEL, outline=LINE, r=16, alpha=255):
        if alpha < 255:
            lay = Image.new("RGB", self.img.size, fill)
            mask = Image.new("L", self.img.size, 0)
            md = ImageDraw.Draw(mask)
            md.rounded_rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                                 radius=self.s(r), fill=alpha)
            self.img.paste(lay, (0, 0), mask)
            if outline:
                self.d.rounded_rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                                         radius=self.s(r), outline=outline,
                                         width=max(1, int(self.s(1))))
        else:
            self.rect(x, y, w, h, fill=fill, outline=outline, r=r)

    def soft_glow(self, x, y, w, h, color, alpha=70, blur=60):
        lay = Image.new("RGB", self.img.size, (0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse([self.s(x), self.s(y), self.s(x + w), self.s(y + h)], fill=color)
        lay = lay.filter(ImageFilter.GaussianBlur(self.s(blur)))
        if alpha < 255:
            lay = Image.blend(Image.new("RGB", lay.size, (0, 0, 0)), lay, alpha / 255.0)
        self.img.paste(Image.blend(self.img, Image.eval(self.img, lambda v: v), 0), (0, 0))
        arr = np.asarray(self.img).astype(np.int16) + np.asarray(lay).astype(np.int16)
        self.img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        self.d = ImageDraw.Draw(self.img)

    def finish(self, out_size=None):
        im = self.img
        if out_size:
            im = im.resize(out_size, Image.LANCZOS)
        return im


# ---------------------------------------------------------------- backgrounds
def _vgrad(size, top, bottom):
    w, h = size
    t = np.linspace(0, 1, h).reshape(h, 1, 1)
    top = np.array(top).reshape(1, 1, 3)
    bot = np.array(bottom).reshape(1, 1, 3)
    arr = (top * (1 - t) + bot * t).astype(np.uint8)
    return np.repeat(arr, w, axis=1)


def _fbm(shape, octaves=5, seed=3, persistence=0.5):
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, dtype=np.float32)
    amp = 1.0
    total = 0.0
    for o in range(octaves):
        res = max(2, int(2 ** (o + 2)))
        gh, gw = res, int(res * w / h) + 1
        g = rng.random((gh, gw)).astype(np.float32)
        gi = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                      dtype=np.float32) / 255.0
        out += gi * amp
        total += amp
        amp *= persistence
    return out / total


def background(canvas, ember=0.55, grid=True, seed=3):
    """Deep navy background with warm ember glow and a fine technical grid."""
    sc = canvas.sc
    Wp, Hp = int(W * sc), int(H * sc)
    arr = _vgrad((Wp, Hp), (10, 16, 27), (6, 9, 16)).astype(np.float32)

    yy, xx = np.mgrid[0:Hp, 0:Wp].astype(np.float32)
    cx, cy = Wp * 0.86, Hp * 0.94
    r = np.sqrt(((xx - cx) / Wp) ** 2 + ((yy - cy) / Hp) ** 2)
    glow = np.clip(1 - r / 0.66, 0, 1) ** 2.2
    arr[:, :, 0] += glow * 118 * ember
    arr[:, :, 1] += glow * 46 * ember
    arr[:, :, 2] += glow * 12 * ember

    cx2, cy2 = Wp * 0.08, Hp * -0.06
    r2 = np.sqrt(((xx - cx2) / Wp) ** 2 + ((yy - cy2) / Hp) ** 2)
    glow2 = np.clip(1 - r2 / 0.55, 0, 1) ** 2.5
    arr[:, :, 0] += glow2 * 22
    arr[:, :, 1] += glow2 * 32
    arr[:, :, 2] += glow2 * 56

    noise = _fbm((Hp, Wp), octaves=5, seed=seed)
    arr += (noise[:, :, None] - 0.5) * 6

    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if grid:
        lay = Image.new("L", (Wp, Hp), 0)
        ld = ImageDraw.Draw(lay)
        step = 64
        for gx in range(0, W + 1, step):
            ld.line([(gx * sc, 0), (gx * sc, Hp)], fill=13, width=1)
        for gy in range(0, H + 1, step):
            ld.line([(0, gy * sc), (Wp, gy * sc)], fill=13, width=1)
        grid_rgb = Image.new("RGB", (Wp, Hp), (128, 156, 200))
        base = Image.composite(grid_rgb, base, lay)
    canvas.img = base
    canvas.d = ImageDraw.Draw(canvas.img)


def soft_glow(canvas, x, y, w, h, color, alpha=70, blur=60):
    lay = Image.new("RGB", canvas.img.size, (0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.ellipse([canvas.s(x), canvas.s(y), canvas.s(x + w), canvas.s(y + h)], fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(canvas.s(blur)))
    lay = Image.eval(lay, lambda v: int(v * alpha / 255.0))
    arr = np.asarray(canvas.img).astype(np.int16) + np.asarray(lay).astype(np.int16)
    canvas.img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    canvas.d = ImageDraw.Draw(canvas.img)


def hero_image(w=1920, h=1080, seed=11, heat=1.0):
    """Procedural fire/ember hero background."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    arr[:, :, 0] = 6
    arr[:, :, 1] = 8
    arr[:, :, 2] = 14

    # base glow from bottom
    base = np.clip((yy / h - 0.15) / 0.85, 0, 1) ** 2.4
    arr[:, :, 0] += base * 165 * heat
    arr[:, :, 1] += base * 62 * heat
    arr[:, :, 2] += base * 18 * heat

    # turbulent flame field
    n1 = _fbm((h, w), octaves=6, seed=seed)
    n2 = _fbm((h, w), octaves=5, seed=seed + 7)
    field = np.clip(n1 * 1.25 - yy / h * 0.75 + 0.30, 0, 1) ** 1.9
    field *= (0.55 + 0.9 * n2)
    arr[:, :, 0] += field * 235 * heat
    arr[:, :, 1] += field ** 1.35 * 120 * heat
    arr[:, :, 2] += field ** 3.0 * 40 * heat

    # smoke haze upper area
    haze = np.clip((0.75 - yy / h), 0, 1) * n2
    arr[:, :, 0] += haze * 26
    arr[:, :, 1] += haze * 30
    arr[:, :, 2] += haze * 44

    # vignette
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    arr *= np.clip(1.18 - 0.55 * r, 0.25, 1.3)[:, :, None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return im.filter(ImageFilter.GaussianBlur(1.6))


def add_grain(im, amount=4.0, seed=5):
    arr = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(seed)
    arr += rng.normal(0, amount, arr.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ---------------------------------------------------------------- chrome
def header(c, kicker, title, sub=None, compact=False):
    top = 54 if not compact else 40
    # kicker
    c.ellipse(96, top + 9, 9, 9, fill=EMBER)
    c.text(116, top + 14, kicker.upper(), size=17, color=(255, 150, 90),
           fname="Inter-SemiBold", track=1.6, anchor="lm")
    ty = top + 44
    size = 58 if not compact else 46
    if compact:
        size = 44 if len(title) < 60 else 40
    else:
        size = 58 if len(title) < 52 else (50 if len(title) < 66 else 44)
    wid, hgt = c.text(96, ty, title, size=size, color=TEXT, fname="Serif-SemiBold", spacing=1.14, maxw=1720)
    y = ty + hgt + 6
    if sub:
        _, h2 = c.text(96, y + 8, sub, size=23, color=MUTED, fname="Inter-Regular", spacing=1.3, maxw=1560)
        y += h2 + 12
    c.line([(96, y + 14), (1824, y + 14)], fill=(255, 255, 255), width=1)
    c.d.line([(c.s(96), c.s(y + 14)), (c.s(1824), c.s(y + 14))], fill=LINE, width=max(1, int(round(c.sc))))
    return y + 14


def footer(c, idx, total, section, timecode=None, progress=True):
    y = 1012
    c.d.line([(c.s(96), c.s(y - 26)), (c.s(1824), c.s(y - 26))], fill=(26, 36, 54), width=max(1, int(round(c.sc))))
    c.text(96, y, "IF 701  ·  FIRE DYNAMICS", size=15, color=DIM, fname="Inter-Medium", track=1.2, anchor="lm")
    c.text(960, y, "TRIUNE BIBLICAL UNIVERSITY  ·  GLOBAL EXTENSION", size=13, color=(85, 100, 124),
           fname="Inter-Medium", track=1.4, anchor="mm")
    right = f"{idx:02d} / {total:02d}"
    if timecode:
        right = timecode + "     " + right
    c.text(1824, y, right, size=15, color=DIM, fname="Mono-Regular", anchor="rm")
    if progress:
        frac = idx / max(1, total)
        c.rect(96, 1038, 1728, 3, fill=(28, 38, 56))
        c.rect(96, 1038, 1728 * frac, 3, fill=EMBER)


def section_badge(c, x, y, num, label, color=EMBER):
    c.panel(x, y, 300, 64, fill=(20, 27, 42), outline=(44, 58, 82), r=10)
    c.rect(x, y, 6, 64, fill=color)
    c.text(x + 24, y + 20, num, size=26, color=color, fname="Serif-Bold", anchor="lm")
    c.text(x + 24, y + 46, label.upper(), size=12, color=MUTED, fname="Inter-SemiBold", track=1.2, anchor="lm")


def bullet_list(c, x, y, items, width, size=25, gap=16, color=TEXT, marker=EMBER, maxh=None):
    cy = y
    for it in items:
        if not it:
            cy += gap * 0.7
            continue
        c.rect(x, cy + size * 0.44, 7, 7, fill=marker, r=1)
        _, hh = c.text(x + 24, cy, it, size=size, color=color, fname="Inter-Regular",
                       spacing=1.34, maxw=width - 24)
        cy += hh + gap
    return cy


def caption(c, x, y, txt, color=DIM, size=15, maxw=600):
    c.text(x, y, txt, size=size, color=color, fname="Inter-Medium", spacing=1.3, maxw=maxw, track=0.2)


def axis_label(c, x, y, txt, color=MUTED, size=16, rot=0):
    if rot == 0:
        c.text(x, y, txt, size=size, color=color, fname="Inter-Medium", anchor="mm", track=0.6)
    else:
        w = c.text_width(txt, size, "Inter-Medium")
        tmp = Image.new("RGBA", (int(w * c.sc) + 8, int(size * c.sc) + 8), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        f = font("Inter-Medium", size * c.sc)
        td.text((4, 4), txt, font=f, fill=color + (255,))
        tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC)
        c.img.paste(tmp, (int(c.s(x) - tmp.size[0] / 2), int(c.s(y) - tmp.size[1] / 2)), tmp)
        c.d = ImageDraw.Draw(c.img)
