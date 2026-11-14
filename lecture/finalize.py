"""Add slide chapters and validate a completed full-lecture render.

Run after build.py --episode IF701_Fire_Dynamics_Full_Lecture --from 0 --to 78.
Does not delete the original if remuxing or validation fails.
"""
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

import build

MEDIA = Path(build.MEDIA)
FILM = MEDIA / 'IF701_Fire_Dynamics_Full_Lecture.mp4'


def main():
    if not FILM.is_file():
        raise SystemExit('Full film not found; finish the build first.')
    slots = []
    for s in build.SEGMENTS:
        audio = Path(build.AUDIO) / (s['id'] + '.mp3')
        length = build.duration(str(audio))
        if length <= 0:
            raise SystemExit(f'Invalid narration: {audio}')
        slots.append(math.ceil((length + 2.25) * 24) / 24)
    expected = sum(slots)
    actual = build.duration(str(FILM))
    if abs(actual - expected) > 2:
        raise SystemExit(f'Duration mismatch: expected {expected:.3f}, got {actual:.3f}')
    info = subprocess.run([build.FF, '-hide_banner', '-i', str(FILM)], capture_output=True).stderr.decode()
    if 'Video: h264' not in info or 'Audio: aac' not in info or '1600x900' not in info:
        raise SystemExit('Unexpected video/audio format: ' + info)

    def escape(text):
        return re.sub(r'([\\=;#])', r'\\\1', text).replace('\n', ' ')

    meta = [';FFMETADATA1', 'title=IF 701 — Fire Dynamics', 'comment=Teaching material; not an operational safety guide.']
    chapters = []
    elapsed = 0.0
    for i, (slide, slot) in enumerate(zip(build.SEGMENTS, slots)):
        start, end = round(elapsed * 1000), round((elapsed + slot) * 1000)
        title = f'{i+1:02d}. {slide["title"]}'
        meta.extend(['[CHAPTER]', 'TIMEBASE=1/1000', f'START={start}', f'END={end}', f'title={escape(title)}'])
        chapters.append({'slide': i + 1, 'id': slide['id'], 'title': slide['title'], 'start_seconds': round(elapsed, 3), 'duration_seconds': round(slot, 3)})
        elapsed += slot
    metadata = Path('/tmp/if701-chapters.ffmetadata')
    metadata.write_text('\n'.join(meta) + '\n')
    remuxed = MEDIA / 'IF701_chaptered.tmp.mp4'
    build.run([build.FF, '-y', '-i', str(FILM), '-f', 'ffmetadata', '-i', str(metadata), '-map', '0', '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-movflags', '+faststart', str(remuxed)])
    if abs(build.duration(str(remuxed)) - actual) > 0.1:
        raise SystemExit('Chaptered remux duration mismatch; original retained.')
    os.replace(remuxed, FILM)
    # Decode representative frames including the corrected water example and ending.
    frames = Path('/tmp/if701-qa')
    frames.mkdir(exist_ok=True)
    for index in (0, 41, 62, 71, 77):
        t = chapters[index]['start_seconds'] + 3
        build.run([build.FF, '-y', '-ss', str(t), '-i', str(FILM), '-frames:v', '1', str(frames / f'{index+1:02d}.png')])
    # Decode the complete audio stream to catch corrupt packets without storing PCM.
    build.run([build.FF, '-v', 'error', '-xerror', '-i', str(FILM), '-vn', '-f', 'null', '-'])
    report = {'duration_seconds': actual, 'expected_seconds': round(expected, 3), 'bytes': FILM.stat().st_size, 'slides': 78, 'chapters': len(chapters), 'video': 'h264, 1600x900, 24 fps', 'audio': 'AAC mono', 'checks': ['duration within 2 seconds', 'expected video/audio streams', 'five representative frames decoded', 'complete audio stream decoded without reported error'], 'manual_review': 'Representative frame images in /tmp/if701-qa still require visual inspection. Not a full scientific/operational content certification.'}
    (Path(build.ROOT) / 'chapters.json').write_text(json.dumps(chapters, indent=2, ensure_ascii=False) + '\n')
    (Path(build.ROOT) / 'render_validation.json').write_text(json.dumps(report, indent=2) + '\n')
    for suffix in ('_silent.mp4', '_audio.wav', '_a.txt', '_v.txt'):
        (MEDIA / ('IF701_Fire_Dynamics_Full_Lecture' + suffix)).unlink(missing_ok=True)
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
