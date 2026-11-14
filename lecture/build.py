# -*- coding: utf-8 -*-
"""Build stills, per-slide clips and an assembled episode for IF 701."""
import os, sys, subprocess, json, shutil, argparse, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

import content_a, content_b, content_c, content_d
from deck import render
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(ROOT, "media")
TMP = "/tmp/if701"
STILLS = os.path.join(TMP, "stills")
CLIPS = os.path.join(TMP, "clips")
AUDIO = os.path.join(ROOT, "audio")

SEGMENTS = content_a.S + content_b.S + content_c.S + content_d.S


def run(cmd, quiet=True):
    r = subprocess.run(cmd, stdout=subprocess.PIPE if quiet else None,
                       stderr=subprocess.PIPE if quiet else None)
    if r.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (" ".join(cmd)[:400],
                                                  (r.stderr or b"").decode()[-1500:]))
    return r


def duration(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path], stderr=subprocess.PIPE,
                       stdout=subprocess.PIPE)
    txt = r.stderr.decode()
    for line in txt.splitlines():
        if "Duration:" in line:
            t = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def make_still(seg, idx, scale=1.5):
    out = os.path.join(STILLS, f"{idx:02d}.png")
    if os.path.exists(out):
        return out
    im = render(seg, idx + 1, len(SEGMENTS), scale=scale)
    im.save(out)
    return out


def make_clip(idx, dur, still, fps=24, crf=26, preset="veryfast", out_w=1600, out_h=900):
    out = os.path.join(CLIPS, f"{idx:02d}.mp4")
    if os.path.exists(out):
        return out
    frames = max(2, int(round(dur * fps)))
    zexpr = "1+0.045*on/%d" % frames
    vf = (f"zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={out_w}x{out_h}:fps={fps},"
          f"format=yuv420p")
    cmd = [FF, "-y", "-loop", "1", "-framerate", str(fps), "-i", still, "-t", f"{dur:.3f}",
           "-vf", vf, "-an", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-r", str(fps), out]
    run(cmd)
    return out


def make_audio(idx, dur, mp3, mono=True):
    out = os.path.join(TMP, "audio", f"{idx:02d}.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        return out
    ad = duration(mp3)
    lead = 0.55
    tail = max(0.9, dur - ad - lead)
    cmd = [FF, "-y", "-i", mp3, "-af",
           f"adelay={int(lead*1000)}|{int(lead*1000)},apad=pad_dur={dur:.3f},atrim=0:{dur:.3f},"
           f"aresample=44100,pan=mono|c0=c0",
           "-c:a", "pcm_s16le", out]
    run(cmd)
    return out


def build(episode_name, indices, fps=24, crf=30, scale=1.5, tail_extra=0.65,
          out_w=1600, out_h=900, abr="48k"):
    os.makedirs(MEDIA, exist_ok=True)
    os.makedirs(STILLS, exist_ok=True)
    os.makedirs(CLIPS, exist_ok=True)
    clips, wavs, total = [], [], 0.0
    for idx in indices:
        seg = SEGMENTS[idx]
        mp3 = os.path.join(AUDIO, seg["id"] + ".mp3")
        ad = duration(mp3)
        dur = math.ceil((ad + 1.6 + tail_extra) * fps) / fps
        still = make_still(seg, idx, scale)
        clip = make_clip(idx, dur, still, fps=fps, crf=crf, out_w=out_w, out_h=out_h)
        wav = make_audio(idx, dur, mp3)
        clips.append(clip)
        wavs.append(wav)
        total += dur
        print(f"  [{idx:02d}] {seg['id']:<10} audio {ad:6.1f}s  slot {dur:6.1f}s  total {total/60:5.2f} min")

    # concat video
    listfile = os.path.join(MEDIA, f"{episode_name}_v.txt")
    with open(listfile, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    silent = os.path.join(MEDIA, f"{episode_name}_silent.mp4")
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", silent])

    # concat audio
    alist = os.path.join(MEDIA, f"{episode_name}_a.txt")
    with open(alist, "w") as f:
        for w in wavs:
            f.write(f"file '{w}'\n")
    full = os.path.join(MEDIA, f"{episode_name}_audio.wav")
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", alist, "-c", "copy", full])

    final = os.path.join(MEDIA, f"{episode_name}.mp4")
    run([FF, "-y", "-i", silent, "-i", full, "-c:v", "copy", "-c:a", "aac", "-b:a", abr,
         "-ac", "1", "-movflags", "+faststart", "-shortest", final])
    size = os.path.getsize(final) / 1e6
    print(f"FINAL {final}  {total/60:.2f} min  {size:.1f} MB")
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="part1")
    ap.add_argument("--from", dest="a", type=int, default=0)
    ap.add_argument("--to", dest="b", type=int, default=10)
    ap.add_argument("--crf", type=int, default=30)
    ap.add_argument("--w", type=int, default=1600)
    ap.add_argument("--h", type=int, default=900)
    args = ap.parse_args()
    idxs = [i for i in range(args.a, min(args.b, len(SEGMENTS)))
            if os.path.exists(os.path.join(AUDIO, SEGMENTS[i]["id"] + ".mp3"))]
    print("building", len(idxs), "segments:", idxs[0], "→", idxs[-1])
    build(args.episode, idxs, crf=args.crf, out_w=args.w, out_h=args.h)
