# -*- coding: utf-8 -*-
"""Slide layouts and the visual dispatch table."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import (Canvas, background, header, footer, bullet_list, caption, hero_image,
                 add_grain, W, H, TEXT, MUTED, DIM, LINE, EMBER, AMBER, RED, TEAL, BLUE,
                 VIOLET, PANEL, PAL, WHITE, section_badge, soft_glow, font)
import diagrams as dg
import diagrams2 as d2
import diagrams3 as d3

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# ---------------------------------------------------------------- dispatch


def _v(key, params):
    p = params or {}
    table = {
        "hero_ember": lambda c, x, y, w, h: None,
        "key_figures": lambda c, x, y, w, h: dg.key_figures(c, x, y, w, h, p["items"]),
        "process_ring": lambda c, x, y, w, h: dg.process_ring(c, x, y, w, h, p["items"]),
        "compare_panels": lambda c, x, y, w, h: dg.compare_panels(c, x, y, w, h, p["left"], p["right"]),
        "def_cards": lambda c, x, y, w, h: dg.def_cards(c, x, y, w, h, p["items"]),
        "compare_units": lambda c, x, y, w, h: dg.compare_units(c, x, y, w, h, p["rows"]),
        "eq_card": lambda c, x, y, w, h: dg.eq_card(c, p.get("title", ""), p["eq"], p["terms"],
                                                   x=x, y=y, w=w, h=h),
        "tetrahedron": d2.tetrahedron,
        "fuel_classes": d3.fuel_classes,
        "oxygen_gauge": d3.oxygen_gauge,
        "heat_modes": d2.heat_modes,
        "conduction_diagram": d2.conduction_diagram,
        "convection_diagram": d2.convection_diagram,
        "radiation_diagram": d2.radiation_diagram,
        "heat_path_trace": d3.heat_path_trace,
        "ignition_curve": lambda c, x, y, w, h: _ignition_curve(c, x, y, w, h),
        "ait_table": d3.ait_table,
        "flash_table": d3.flash_table,
        "hrr_table": d3.hrr_table,
        "fire_stages_chart": lambda c, x, y, w, h: dg.fire_stages_chart(c, x, y, w, h),
        "incipient_viz": lambda c, x, y, w, h: _stage_viz(c, x, y, w, h, 0),
        "growth_viz": lambda c, x, y, w, h: _stage_viz(c, x, y, w, h, 1),
        "fully_dev_viz": lambda c, x, y, w, h: _stage_viz(c, x, y, w, h, 2),
        "decay_viz": lambda c, x, y, w, h: _stage_viz(c, x, y, w, h, 3),
        "hrr_bars": dg.hrr_bars,
        "calorimetry": d3.calorimetry,
        "scaling_tree": d3.scaling_tree,
        "alpha_table": lambda c, x, y, w, h: _alpha_table(c, x, y, w, h),
        "alpha_chart": lambda c, x, y, w, h: dg.alpha_chart(c, x, y, w, h),
        "model_limits": d3.model_limits,
        "smoke_composition": d2.smoke_composition,
        "smoke_drivers": d3.smoke_drivers,
        "smoke_layer": d2.smoke_layer,
        "visibility_chart": d3.visibility_chart,
        "plume_zones": d2.plume_zones,
        "ceiling_jet": d2.ceiling_jet,
        "layer_build": d3.layer_build,
        "energy_balance": d2.energy_balance,
        "vent_flow": d2.vent_flow,
        "vent_transition": d3.vent_transition,
        "flashover_seq": d2.flashover_seq,
        "flashover_predict": d3.flashover_predict,
        "backdraft_seq": d2.backdraft_seq,
        "phenomena_table": d3.phenomena_table,
        "fuel_vs_vent_chart": d3.fuel_vs_vent_chart,
        "regime_diagnosis": d3.regime_diagnosis,
        "spread_paths": d2.spread_paths,
        "warehouse_spread": d3.warehouse_spread,
        "escalation_chain": d3.escalation_chain,
        "material_props": d3.material_props,
        "panel_section": d3.panel_section,
        "structure_response": d3.structure_response,
        "confined_space": d3.confined_space,
        "large_volume": d3.large_volume,
        "model_types": d3.model_types,
        "cfd_field": d3.cfd_field,
        "model_use": lambda c, x, y, w, h: d3.tools_grid(c, x, y, w, h),
        "worked_t2": d3.worked_t2,
        "worked_vent": d3.worked_vent,
        "worked_radiation": d3.worked_radiation,
        "worked_flashover": d3.worked_flashover,
        "worked_water": d3.worked_water,
        "case_cards": d3.case_cards,
        "case_west": lambda c, x, y, w, h: d3.case_visual(c, x, y, w, h, "case_west",
                                                          "West Pharmaceutical Services", "Kinston, North Carolina · 29 January 2003",
                                                          ["Six fatalities; plant destroyed.",
                                                           "Polyethylene dust on beams and above a suspended ceiling.",
                                                           "Primary deflagration, then secondary explosions through the building.",
                                                           "Mechanism: a distributed fuel layer becomes a dust cloud.",
                                                           "Lesson: dust is a fuel load, and a layer is a fuse."], RED),
        "case_buncefield": lambda c, x, y, w, h: d3.case_visual(c, x, y, w, h, "case_buncefield",
                                                                "Buncefield Oil Terminal", "Hemel Hempstead, UK · 11 December 2005",
                                                                ["Tank 912 overfilled; petrol cascaded and formed a vapour cloud.",
                                                                 "Vapour cloud explosion; 43 injuries, widespread blast damage.",
                                                                 "More than 20 tanks involved; fire burned for several days.",
                                                                 "Mechanism: flash point, dispersion, confinement, tank-to-tank radiation.",
                                                                 "Lesson: the most dangerous phase can precede any visible fire."], AMBER),
        "case_grenfell": lambda c, x, y, w, h: d3.case_visual(c, x, y, w, h, "case_grenfell",
                                                              "Grenfell Tower", "London, UK · 14 June 2017",
                                                              ["72 deaths in a 24-storey residential block.",
                                                               "ACM cladding with a polyethylene core plus PIR insulation.",
                                                               "External spread from the 4th floor to the roof in minutes.",
                                                               "Mechanism: melting core, cavity chimney, falling burning debris.",
                                                               "Industrial parallel: plastic-cored sandwich panels."], EMBER),
        "case_compare": d3.case_compare,
        "demo_setup": d3.demo_setup,
        "demo_anim": lambda c, x, y, w, h: d3.demo_frame(c, x, y, w, h, p.get("t1", 180), p.get("phase", "growth")),
        "demo_vent_compare": lambda c, x, y, w, h: d3.demo_frame(c, x, y, w, h, 420, "vent", two_panel=True),
        "decision_matrix": d3.decision_matrix,
        "tools_grid": d3.tools_grid,
        "sizeup_table": d3.sizeup_table,
        "assessment_list": lambda c, x, y, w, h: d3.assessment_list(c, x, y, w, h, p.get("items", [])),
    }
    return table[key]


# ---------------------------------------------------------------- extra visuals


def _ignition_curve(c, x, y, w, h):
    from charts import Chart
    ch = Chart(c, x, y, w, h, (5, 100), (1, 1000), "IMPOSED HEAT FLUX (kW/m²)", "TIME TO IGNITION (s)",
               xlog=True, ylog=True, xticks=[5, 10, 20, 50, 100], yticks=[1, 5, 10, 50, 100, 500])
    q = np.linspace(6, 100, 200)
    for k, col, lab in [(1.4, (146, 116, 78), "thick timber"), (0.55, AMBER, "polyurethane foam"),
                        (0.9, TEAL, "PMMA sheet")]:
        ch.line(q, 2200 / (q ** 1.7) * k + 2, col, 2.4, label=lab)
    ch.hline(20, RED, 1.2, 7, "20 kW/m²")
    ch.legend()
    c.text(x, y + h + 20, "Time to ignition falls steeply as heat flux rises — thin, low-density fuels ignite first.",
           size=14, color=MUTED, fname="Inter-Regular")


def _alpha_table(c, x, y, w, h):
    rows = [("SLOW", "0.00293", "600 s", "dense stacks, thick timber"),
            ("MEDIUM", "0.01172", "300 s", "mixed office and retail"),
            ("FAST", "0.0469", "150 s", "racked cartons, pallets, polymers"),
            ("ULTRA-FAST", "0.1876", "75 s", "foam, aerosols, thin films, liquids")]
    from diagrams import table
    table(c, x, y, w, rows, ["CLASS", "α (kW/s²)", "TIME TO 1 MW", "TYPICAL FUEL"],
          colw=[w * 0.20, w * 0.22, w * 0.20, w * 0.38], h=h, size=17)


def _stage_viz(c, x, y, w, h, stage):
    frac = [0.10, 0.34, 0.66, 0.80][stage]
    temp = [0.12, 0.40, 0.85, 0.45][stage]
    flames = [h * 0.10, h * 0.22, h * 0.34, h * 0.07][stage]
    c.panel(x, y, w, h, fill=(11, 16, 25), outline=(34, 46, 66), r=10)
    rh = h - 90
    g = d2.room(c, x + 14, y + 14, w - 28, rh, layer_frac=frac, layer_temp=temp,
                fire_x=0.34, flames=flames, seed=7 + stage)
    labels = [("50–150 °C in the layer", "tenable; detection and first aid"),
              ("300–600 °C in the layer", "rollover; flashover approaching"),
              ("800–1 200 °C gas temperature", "ventilation-controlled; unsurvivable"),
              ("falling temperature", "smouldering; backdraft risk")]
    c.text(x + 20, y + h - 56, labels[stage][0], size=17, color=AMBER, fname="Inter-SemiBold")
    c.text(x + 20, y + h - 30, labels[stage][1], size=14, color=MUTED, fname="Inter-Regular")
    if stage == 2:
        c.arrow(g["x"] + g["w"] - 30, g["floor"] - 10, g["x"] + g["w"] + 30, g["floor"] - 10, fill=EMBER, width=2, head=8)
        c.arrow(g["x"] + g["w"] + 30, g["ceil"] + 18, g["x"] + g["w"] - 30, g["ceil"] + 18, fill=EMBER, width=2, head=8)
    if stage == 1:
        for k in range(4):
            c.arrow(g["x"] + 40 + k * 46, g["ceil"] + 26, g["x"] + 62 + k * 46, g["ceil"] + 26,
                    fill=(255, 150, 60), width=1.6, head=7)


# ---------------------------------------------------------------- layouts


def _visual_area(c, s, kind="side"):
    hb = header(c, s["kicker"], s["title"], s.get("sub"), compact=(kind == "full"))
    if kind == "side":
        return (hb + 30, hb + 30, 0), 780, 1824
    else:
        return (hb + 26, hb + 26, 0), 96, 1824


def draw_visual(c, s, box):
    key, params = (None, None)
    v = s.get("visual")
    if v:
        key, params = v
    if not key:
        return
    fn = _v(key, params)
    if fn is None:
        return
    x, y, w, h = box
    fn(c, x, y, w, h)


def layout_side(c, s, text_w=640):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    ytop = hb + 34
    bx = 96 + text_w + 56
    bw = 1824 - bx
    bh = 1000 - ytop - 10
    # panel behind visual
    c.panel(bx - 18, ytop - 10, bw + 36, bh + 20, fill=(12, 17, 27), outline=(34, 46, 66), r=14)
    draw_visual(c, s, (bx, ytop + 10, bw, bh - 20))
    bullets = s["bullets"]
    # measure then centre vertically
    total = 0
    for b in bullets:
        if not b:
            total += 12
            continue
        _, hh = c.text(96, -4000, b, size=23, color=TEXT, fname="Inter-Regular", spacing=1.34, maxw=text_w - 24)
        total += hh + 18
    avail = (1000 - ytop) - 8
    start = ytop + max(0, (avail - total) / 2 - 10)
    bullet_list(c, 96, start, bullets, text_w, size=23, gap=18)
    return hb


def layout_full(c, s, pad=96):
    hb = header(c, s["kicker"], s["title"], s.get("sub"), compact=True)
    ytop = hb + 22
    bullets = s.get("bullets") or []
    bh = 1000 - ytop - (78 if bullets else 10)
    draw_visual(c, s, (pad, ytop, 1824 - pad, bh))
    if bullets:
        # caption strip
        c.rect(0, 1000 - 74, W, 74, fill=(9, 13, 21))
        c.line([(0, 1000 - 74), (W, 1000 - 74)], fill=(30, 42, 62), width=1)
        n = len(bullets)
        colw = 1728 / max(3, min(n, 4))
        for i, b in enumerate(bullets[:4]):
            bx = 96 + i * colw
            c.rect(bx, 1000 - 52, 5, 5, fill=EMBER, r=1)
            c.text(bx + 14, 1000 - 62, b, size=14, color=(206, 216, 232), fname="Inter-Regular",
                   maxw=colw - 24, spacing=1.25)
    return hb


def layout_outcomes(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    items = [b for b in s["bullets"] if b]
    colw = 800
    gap = (1000 - hb - 60) / 5
    for i, it in enumerate(items):
        col = i // 5
        row = i % 5
        x = 96 + col * 880
        y = hb + 46 + row * gap
        num = "".join(ch for ch in it.split(" ")[0] if ch.isdigit())
        body = it[len(num):].strip()
        c.text(x, y, num, size=30, color=EMBER, fname="Serif-Bold", anchor="la")
        c.text(x + 56, y + 2, body, size=21, color=TEXT, fname="Inter-Regular", maxw=colw - 70, spacing=1.34)
        c.line([(x, y + gap * 0.72), (x + colw, y + gap * 0.72)], fill=(28, 38, 56), width=1)


def layout_lessons(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    items = [b for b in s["bullets"] if b]
    colw = 800
    for i, it in enumerate(items):
        col = i // 5
        row = i % 5
        x = 96 + col * 880
        y = hb + 30 + row * 92
        num = "".join(ch for ch in it.split(" ")[0] if ch.isdigit())
        body = it[len(num):].strip()
        c.panel(x, y, colw, 78, fill=(15, 22, 35), outline=(38, 52, 76), r=8)
        c.text(x + 22, y + 26, num, size=20, color=EMBER, fname="Serif-Bold", anchor="la")
        c.text(x + 66, y + 18, body, size=19, color=TEXT, fname="Inter-Regular", maxw=colw - 90, spacing=1.26)


def layout_table_side(c, s):
    layout_side(c, s, text_w=600)


def layout_equation(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    ytop = hb + 30
    draw_visual(c, s, (700, ytop, 1124, 1000 - ytop - 10))
    bullet_list(c, 96, ytop + 10, s["bullets"], 560, size=23, gap=20)
    return hb


def layout_title(c, s, closing=False):
    im = hero_image(1920, 1080, seed=13 if not closing else 29, heat=0.85)
    # Keep the logical coordinate scale consistent with the supersampled canvas.
    # Replacing it with an unscaled hero cropped title/closing text at scale > 1.
    im = im.resize(c.img.size, Image.Resampling.LANCZOS)
    c.img = im
    c.d = ImageDraw.Draw(c.img)
    # left dark scrim
    arr = np.asarray(c.img).astype(np.float32)
    xx = np.linspace(0, 1, arr.shape[1])[None, :, None]
    arr = arr * (1 - 0.55 * np.clip((0.72 - xx) / 0.72, 0, 1) ** 1.2)
    c.img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    c.d = ImageDraw.Draw(c.img)
    c.text(96, 118, "TRIUNE BIBLICAL UNIVERSITY  ·  GLOBAL EXTENSION", size=15, color=(255, 190, 150),
           fname="Inter-SemiBold", track=2.2)
    c.text(96, 152, "MASTER IN INDUSTRIAL FIREFIGHTING  ·  IF 701", size=13, color=(200, 180, 170),
           fname="Inter-Medium", track=1.6)
    ty = 300
    if closing:
        c.text(96, ty, s["title"], size=86, color=WHITE, fname="Serif-Bold", maxw=1300, spacing=1.06)
    else:
        c.text(96, ty, "Understanding", size=78, color=WHITE, fname="Serif-Bold")
        c.text(96, ty + 92, "Fire Dynamics", size=78, color=(255, 214, 170), fname="Serif-Bold")
    sub = s.get("sub", "")
    if sub:
        _, hh = c.text(96, ty + (250 if not closing else 130), sub, size=25, color=(226, 220, 214),
                       fname="Inter-Regular", maxw=1150, spacing=1.4)
    c.rect(96, 900, 120, 4, fill=EMBER)
    c.text(96, 928, "Lecture 1  ·  68 minutes  ·  Narrated lecture with worked calculations and case studies",
           size=16, color=(210, 200, 196), fname="Inter-Regular")
    if closing:
        for i, b in enumerate(s.get("bullets") or []):
            c.text(96, 640 + i * 34, "— " + b, size=18, color=(228, 222, 216), fname="Inter-Regular")
    return 0


def layout_definitions(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    draw_visual(c, s, (96, hb + 60, 1728, 300))
    # explanatory paragraph
    c.text(96, hb + 400, "Combustion can occur without a visible flame — smouldering charcoal is combustion. "
                         "A flame requires gas-phase reaction. A fire is the whole system: chemistry, heat, "
                         "smoke and the response of the enclosure.",
           size=24, color=MUTED, fname="Inter-Regular", maxw=1400, spacing=1.55)


def layout_tool_grid(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    draw_visual(c, s, (96, hb + 26, 1728, 470))
    bullet_list(c, 96, hb + 520, s["bullets"], 820, size=20, gap=12)
    c.panel(1000, hb + 510, 824, 300, fill=(15, 22, 35), outline=(38, 52, 76), r=10)
    c.text(1024, hb + 530, "LIMITS OF THE TIC", size=12, color=AMBER, fname="Inter-SemiBold", track=1.2)
    for i, t in enumerate(["measures surface temperature, not gas temperature",
                           "cannot see through water spray, glass or metal skins",
                           "emissivity and reflections distort readings",
                           "a cold surface can hide a hot layer above it"]):
        c.text(1024, hb + 560 + i * 56, "—  " + t, size=16, color=MUTED, fname="Inter-Regular",
               maxw=780, spacing=1.3)


def layout_case_intro(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    draw_visual(c, s, (96, hb + 40, 1728, 300))
    bullet_list(c, 96, hb + 390, s["bullets"], 1000, size=22, gap=16)


def layout_assessment(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    items = [b[3:].strip() if b[:2].strip().isdigit() else b for b in s["bullets"]]
    d3.assessment_list(c, 96, hb + 30, 1728, 720, items)


def layout_flow(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"))
    draw_visual(c, s, (96, hb + 30, 1728, 420))
    bullet_list(c, 96, hb + 490, s["bullets"], 1728, size=20, gap=10)


def layout_compare_demo(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"), compact=True)
    draw_visual(c, s, (96, hb + 20, 1728, 420))
    bl = s["bullets"]
    for i, b in enumerate(bl):
        col, row = i % 2, i // 2
        x = 96 + col * 880
        y = hb + 470 + row * 46
        c.rect(x, y + 8, 6, 6, fill=EMBER, r=1)
        c.text(x + 18, y, b, size=18, color=TEXT, fname="Inter-Regular", maxw=840, spacing=1.25)


def layout_demo(c, s):
    hb = header(c, s["kicker"], s["title"], s.get("sub"), compact=True)
    draw_visual(c, s, (96, hb + 16, 1728, 470))
    bl = s["bullets"]
    for i, b in enumerate(bl):
        col, row = i % 2, i // 2
        x = 96 + col * 880
        y = hb + 510 + row * 46
        c.rect(x, y + 8, 6, 6, fill=EMBER, r=1)
        c.text(x + 18, y, b, size=18, color=TEXT, fname="Inter-Regular", maxw=840, spacing=1.25)


def render(s, idx, total, scale=2):
    c = Canvas(scale)
    background(c, ember=0.5)
    lay = s.get("layout", "bullets")
    if lay == "title":
        layout_title(c, s)
    elif lay == "closing":
        layout_title(c, s, closing=True)
    elif lay == "full":
        layout_full(c, s)
    elif lay in ("bullets", "split"):
        layout_side(c, s, text_w=620)
    elif lay == "table":
        layout_side(c, s, text_w=540)
    elif lay == "chart":
        layout_side(c, s, text_w=520)
    elif lay == "bar_chart":
        layout_side(c, s, text_w=500)
    elif lay == "equation":
        layout_equation(c, s)
    elif lay == "outcomes":
        layout_outcomes(c, s)
    elif lay == "lessons":
        layout_lessons(c, s)
    elif lay == "definitions":
        layout_definitions(c, s)
    elif lay == "tool_grid":
        layout_tool_grid(c, s)
    elif lay == "case_intro":
        layout_case_intro(c, s)
    elif lay == "assessment":
        layout_assessment(c, s)
    elif lay == "flow":
        layout_flow(c, s)
    elif lay == "compare_demo":
        layout_compare_demo(c, s)
    elif lay == "demo":
        layout_demo(c, s)
    elif lay == "case":
        hb = header(c, s["kicker"], s["title"], s.get("sub"), compact=True)
        draw_visual(c, s, (96, hb + 24, 1728, 640))
    elif lay == "worked":
        layout_full(c, s)
    else:
        layout_side(c, s)
    if lay not in ("title", "closing"):
        footer(c, idx, total, s.get("sec"))
    return c.finish()
