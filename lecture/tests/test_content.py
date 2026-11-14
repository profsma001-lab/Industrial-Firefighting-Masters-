"""Small regression checks for production completeness and corrected examples."""
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import content_a, content_b, content_c, content_d
SLIDES = content_a.S + content_b.S + content_c.S + content_d.S


class LectureTests(unittest.TestCase):
    def test_unique_slide_ids(self):
        self.assertEqual(len(SLIDES), 78)
        self.assertEqual(len({s['id'] for s in SLIDES}), 78)

    def test_narration_assets_complete(self):
        for s in SLIDES:
            with self.subTest(slide=s['id']):
                audio = ROOT / 'audio' / (s['id'] + '.mp3')
                self.assertTrue(audio.is_file())
                self.assertGreater(audio.stat().st_size, 1000)
                self.assertTrue(s['narr'].strip())

    def test_corrected_worked_examples(self):
        self.assertAlmostEqual(math.sqrt(14000 / .0469) / 60, 9.106, places=2)
        self.assertAlmostEqual(14 * 60 / (2.591 * .35), 926.283, places=2)
        self.assertAlmostEqual(math.sqrt(1800 / (4 * math.pi * 12.5)), 3.385, places=2)
        self.assertAlmostEqual(345 * math.log10(8 * 30 + 1) + 20, 841.795, places=2)

    def test_demonstration_limitations_explicit(self):
        slides = {s['id']: s for s in SLIDES}
        self.assertIn('not a validated', slides['dem1']['narr'])
        self.assertIn('does not guarantee', slides['dem4']['narr'])
        self.assertIn('not a general withdrawal threshold', slides['dem5']['narr'])


if __name__ == '__main__':
    unittest.main()
