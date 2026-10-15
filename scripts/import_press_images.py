"""One-time import of public Bleach & Blood press artwork into GitHub Pages.

Sources are the owner's public Google Drive media files. Original files remain
in Drive; only optimized, crawlable WebP derivatives go into the website.
Run: python scripts/import_press_images.py
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import gdown
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "images" / "bleach-and-blood" / "press"
# Fixed, user-provided media IDs. No search, secrets, or private resources.
SOURCES = [
    ("1g5KnQp6nVqcE6k_SVYkQ4OQW3tNGBMBx", "bleach-and-blood-laundromat-night-art.webp"),
    ("10ottcuVUsgJXESgTQTlGVoaz4thfKMhP", "bleach-and-blood-killer-character.webp"),
    ("1ZT4nEvL4RDACJWKjdi8rdkPQCI-glenL", "bleach-and-blood-laundromat-wide-art.webp"),
    ("1eFYuAkhbRRQvDwZ5bpdeH1zzrxkDzwL5", "bleach-and-blood-title-art.webp"),
    ("1xlsFG9Fzcha33XePlmXEVUTziP_cgEZ6", "bleach-and-blood-screenshot-01.webp"),
    ("1TKJMzjRLZe5bAdMoWovI8zYPpNBTpoIa", "bleach-and-blood-screenshot-02.webp"),
    ("1n-_oPL5EaHnwm7mybKiOJZkUjF7Krm6L", "bleach-and-blood-screenshot-03.webp"),
    ("1jJ2Bgu_P-EmlyAgGR5wS2glESFRzVyzE", "bleach-and-blood-screenshot-04.webp"),
    ("1ojgiPTwTH647Aw6ZMIK0srio2du7wRwA", "bleach-and-blood-screenshot-05.webp"),
    ("1ekCgmiX2hCwEBsba6EiB_gNbaAKarPUL", "bleach-and-blood-screenshot-06.webp"),
    ("1eq_4EDE_FWQfIPfH_F0dQBhFc4wqPMKj", "bleach-and-blood-trailer-thumbnail.webp"),
]

def run() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    report = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, (file_id, name) in enumerate(SOURCES, start=1):
            raw = Path(tmp) / f"source-{n}"
            print(f"[{n}/{len(SOURCES)}] Downloading {name}", flush=True)
            result = gdown.download(id=file_id, output=str(raw), quiet=True)
            if not result or not raw.is_file() or raw.stat().st_size < 10000:
                raise RuntimeError(f"Google Drive download failed: {name} ({file_id})")
            with Image.open(raw) as source:
                im = ImageOps.exif_transpose(source)
                im.thumbnail((2560, 1920), Image.Resampling.LANCZOS)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
                target = DEST / name
                im.save(target, format="WEBP", quality=88, method=6)
                size = target.stat().st_size
                if size < 3000:
                    raise RuntimeError(f"Unexpectedly small output: {target}")
                report.append({"name": name, "width": im.width, "height": im.height, "size_bytes": size, "drive_id": file_id})
                print(f"  saved {im.width}x{im.height}, {size:,} bytes", flush=True)
    (DEST / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(report)} optimized images.", flush=True)

if __name__ == "__main__":
    run()
