# IF 701 · Fire Dynamics — Video Lecture Series

**Understanding Fire Dynamics: Heat Transfer, Combustion, Smoke Movement and Industrial Fire Development**

Master in Industrial Firefighting · Triune Biblical University Global Extension, USA

---

## What this package is

A complete, narrated postgraduate lecture in 78 slides, produced as a video lecture series with a
matching slide deck PDF, a full teaching script, a calculation workbook, three industrial case studies,
an assessment pack and a printable reference card.

Everything here is generated from source: the slide deck is drawn programmatically
(`lecture/render/`), the narration is written in `lecture/content_*.py`, and the video is assembled
by `lecture/build.py`. That means the deck and the film can be revised, re-timed and re-rendered.

## Contents

| File | What it is |
|---|---|
| `lecture/media/IF701_Fire_Dynamics_Full_Lecture.mp4` | **Complete lecture — 68:18, 76.6 MB, 78 slide chapters, H.264 1600×900** |
| `lecture/media/part1.mp4` | Part 1 (7:20) — opening, definitions, fire tetrahedron |
| `lecture/media/part2.mp4` | Part 2 (9:13) — heat transfer, ignition parameters, fire development to growth |
| `lecture/media/part3.mp4` | Part 3 (7:24) — growth, fully developed, decay, heat release rate, the t² model |
| `lecture/media/part4.mp4` | Part 4 (4:13) — smoke: composition, movement, layers, visibility |
| `lecture/media/part5.mp4` | Part 5 (8:47) — plumes, ceiling jets, the compartment, flashover, backdraft, regimes |
| `lecture/media/part6.mp4` | Part 6 (9:07) — slides 46–55: regime diagnosis, spread, materials, structure, special spaces and modelling |
| `lecture/media/part7.mp4` | Part 7 (9:28) — modelling, five worked calculations, case introduction and West Pharmaceutical |
| `lecture/media/part8.mp4` | Part 8 (9:37) — Buncefield, Grenfell, illustrative warehouse scenario and assessment tools |
| `lecture/media/part9.mp4` | Part 9 (3:08) — assessment and closing lessons |
| `lecture/media/IF701_Fire_Dynamics_Slides.pdf` | The complete 78-slide deck, print-ready |
| `lecture/docs/01_Lecture_Script_and_Slide_Notes.md` | Full narration, slide by slide, with timecodes and teaching notes |
| `lecture/docs/02_Worked_Examples_and_Calculations.md` | Seven worked examples, a practice set and marking guidance |
| `lecture/docs/03_Case_Studies.md` | West Pharmaceutical (2003), Buncefield (2005), Grenfell (2017) plus vignettes |
| `lecture/docs/04_Assessment_Pack.md` | Essay and calculation questions, practical exercise, rubric, short-answer bank |
| `lecture/docs/05_Reference_Card.md` | Equations, constants, thresholds and decision cues on two pages |

## Lecture architecture (78 slides, ≈ 68 minutes)

| Block | Slides | Content |
|---|---|---|
| 00 Opening | 1–2 | Title; why fire dynamics is a physics problem with a deadline |
| 01 Introduction | 3–5 | What fire dynamics studies; industrial vs domestic regimes; learning outcomes |
| 02 Definitions | 6–8 | Fire, combustion, flame; heat, temperature, flux; heat release rate |
| 03 Fire tetrahedron | 9–11 | Triangle to tetrahedron; what actually burns; oxygen, oxidisers, radical inhibition |
| 04 Heat transfer | 12–16 | Three modes; conduction, convection, radiation; reading a fire through its heat paths |
| 05 Ignition parameters | 17–19 | Ignition temperature; autoignition and self-heating; flash point and flammable range |
| 06 Fire development | 20–24 | Four stages; incipient, growth, fully developed, decay |
| 07 Heat release rate | 25–27 | Typical values; measurement; why one number explains so much |
| 08 Fire growth | 28–30 | The t² model; reading the curve; where the model fails |
| 09 Smoke | 31–34 | Composition; buoyancy and drivers; layers and neutral plane; visibility |
| 10 Plumes | 35–37 | Plume zones; ceiling jets; building the hot layer |
| 11 Compartments | 38–40 | Energy balance; ventilation factor; openings change the fire |
| 12 Flashover & backdraft | 41–44 | Flashover; prediction; backdraft; other phenomena |
| 13 Regimes | 45–46 | Fuel- vs ventilation-controlled; diagnosing the regime |
| 14 Fire spread | 47–49 | Five mechanisms; vertical and horizontal spread; storage and escalation |
| 15 Materials & structure | 50–52 | Reaction to fire vs fire resistance; composite panels; structural response |
| 16 Confined vs large | 53–54 | Confined spaces; large-volume and travelling fires |
| 17 Modelling | 55–57 | Why we model; inside a CFD model; using models without being fooled |
| 18 Calculations | 58–62 | Five worked examples with charts |
| 19 Case studies | 63–67 | Three industrial cases and a synthesis |
| 20 Demonstration | 68–72 | Simulated warehouse fire: growth, spread, ventilation change, decisions |
| 21 Tools | 73–74 | Thermal imaging, smoke reading, modelling, monitoring; size-up |
| 22 Assessment | 75–78 | Questions; ten professional lessons; close |

## How to use it

- **As a roughly 68-minute lecture:** play the parts in sequence. Each part ends at a natural section boundary.
- **As shorter teaching blocks:** use the section dividers (slides 1, 25, 45, 63) as episode breaks.
- **As a flipped classroom:** issue the script and the workbook before the session, then use the
  demonstration (slides 68–72) and the case studies as the live discussion.
- **For assessment:** `04_Assessment_Pack.md` contains the written paper, the practical brief and the rubric.

## Rebuilding

```bash
pip install --break-system-packages pillow numpy fonttools brotli imageio-ffmpeg
cd lecture
python3 make_pdf.py                     # rebuild the slide deck PDF
python3 build.py --episode part1 --from 0 --to 10
```

Narration audio lives in `lecture/audio/` (one MP3 per slide). The build script takes the slide list
from `lecture/content_*.py`, renders each still, adds a slow push-in, and muxes the narration.

## Notes on sources and images

The scientific content follows standard fire engineering practice: the SFPE Handbook of Fire Protection
Engineering, ISO 834, Heskestad plume and flame-height correlations, Alpert ceiling-jet correlations,
Thomas and McCaffrey flashover correlations, and the standard t² growth classes. Case-study facts follow
the published investigations by the U.S. Chemical Safety Board, the UK Health and Safety Executive, the
Buncefield Major Incident Investigation Board and the Grenfell Tower Inquiry. Illustrative images in the
deck are AI-generated reconstructions and are captioned as such; they are not photographs of the
incidents and should not be presented as evidence.

## Final production validation

The complete film is rendered with 78 embedded slide chapters. Duration and expected streams were checked, the full audio stream decoded without reported errors, and representative video frames decoded and visually inspected. The supersampling crop on the opening/closing slides is fixed. Four content regression tests pass. See `lecture/render_validation.json` and `lecture/chapters.json`.

This is teaching material, not a validated operational simulator or safety certification. Qualified instructional and technical review remains necessary before operational use. Rendered videos and PDF are workspace deliverables, intentionally excluded from Git; source and narration support rebuilding.
