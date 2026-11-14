# -*- coding: utf-8 -*-
"""Generate the lecture handbook (full script with slide cues) from content."""
import os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_a, content_b, content_c, content_d

ROOT = os.path.dirname(os.path.abspath(__file__))
S = content_a.S + content_b.S + content_c.S + content_d.S
AUD = os.path.join(ROOT, "audio")
OUT = os.path.join(ROOT, "docs", "01_Lecture_Script_and_Slide_Notes.md")

import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in r.stderr.decode().splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


lines = []
lines.append("# IF 701 · Fire Dynamics — Lecture Script and Slide Notes\n")
lines.append("**Understanding Fire Dynamics: Heat Transfer, Combustion, Smoke Movement and Industrial Fire Development**  \n")
lines.append("Master in Industrial Firefighting · Triune Biblical University Global Extension, USA  \n")
lines.append("Total running time: approx. 60 minutes · 78 slides\n")
lines.append("\n> This document is the full teaching script. Each section is one slide: the on-screen title, "
             "the content shown, the narration (word for word), the timecode, and a teaching note. "
             "Use it for delivery, for review, or as a transcript.\n")
lines.append("\n---\n")

t0 = 0.0
for i, s in enumerate(S):
    mp3 = os.path.join(AUD, s["id"] + ".mp3")
    d = dur(mp3) + 1.6 if os.path.exists(mp3) else None
    tc = f"{int(t0//60):02d}:{int(t0%60):02d}"
    head = f"\n## Slide {i+1:02d} · {s['title']}\n"
    lines.append(head)
    meta = f"**Section:** {s['kicker']}  \n"
    if s.get("sub"):
        meta += f"**Subtitle:** {s['sub']}  \n"
    meta += f"**Timecode:** {tc}"
    if d:
        meta += f" · {d:.0f} s"
    lines.append(meta + "\n")
    if s.get("bullets"):
        lines.append("\n**On screen**\n")
        for b in s["bullets"]:
            if b:
                lines.append(f"- {b}")
        lines.append("")
    lines.append("\n**Narration**\n")
    lines.append("> " + s["narr"].replace("\n", " ") + "\n")
    if s.get("note"):
        lines.append(f"\n**Teaching note:** {s['note']}\n")
    lines.append("\n---\n")
    if d:
        t0 += d + 0.65

open(OUT, "w").write("\n".join(lines))
print("wrote", OUT, os.path.getsize(OUT) / 1000, "kB")
