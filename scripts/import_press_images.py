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
    # Publish gallery and sitemap only after every image has downloaded successfully.
    press_page = ROOT / "bleach-and-blood" / "press" / "index.html"
    page = press_page.read_text(encoding="utf-8")
    start_marker = "<!-- PRESS_GALLERY_START -->"
    end_marker = "<!-- PRESS_GALLERY_END -->"
    base_url = "https://the-windy-project.github.io/windy-site/"
    names = {
        "bleach-and-blood-laundromat-night-art.webp": "Laundromat promotional background art",
        "bleach-and-blood-killer-character.webp": "Masked killer full-body promotional art",
        "bleach-and-blood-laundromat-wide-art.webp": "Wide official background artwork",
        "bleach-and-blood-title-art.webp": "Bleach & Blood title art",
        **{f"bleach-and-blood-screenshot-{i:02d}.webp": f"Bleach & Blood gameplay screenshot {i}" for i in range(1, 7)},
        "bleach-and-blood-trailer-thumbnail.webp": "Bleach & Blood teaser trailer thumbnail",
    }
    cards = []
    for item in report:
        name = item["name"]
        url = "/windy-site/images/bleach-and-blood/press/" + name
        title = names[name]
        cards.append(
            '<figure class="asset">'
            f'<a href="{url}" target="_blank" rel="noopener">'
            f'<img src="{url}" alt="{title} — official imagery from The Windy Project" '
            f'width="{item["width"]}" height="{item["height"]}" loading="lazy" '
            'style="width:100%;aspect-ratio:16/9;object-fit:contain;background:#151518" /></a>'
            f'<figcaption class="asset-body"><h3>{title}</h3>'
            f'<p>Official website-hosted image · WebP · {item["width"]} × {item["height"]}</p>'
            f'<a href="{url}" download>Open / download image ↗</a></figcaption></figure>'
        )
    gallery = (
        '<section class="content" aria-labelledby="press-gallery-heading"><div class="shell">'
        '<div class="label">Official image gallery</div><h2 id="press-gallery-heading">Screenshots &amp; promotional art</h2>'
        '<p class="copy">Original-resolution files are in the press archive above; these website-hosted images '
        'are optimized for fast browsing and search indexing.</p>'
        '<div class="assets">' + "".join(cards) + '</div></div></section>'
    )
    if start_marker in page and end_marker in page:
        a, tail = page.split(start_marker, 1)
        _, b = tail.split(end_marker, 1)
        page = a + start_marker + gallery + end_marker + b
    else:
        page = page.replace('</main>', start_marker + gallery + end_marker + '</main>')
    press_page.write_text(page, encoding="utf-8")

    from xml.etree import ElementTree as ET
    sitemap_path = ROOT / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ims = "http://www.google.com/schemas/sitemap-image/1.1"
    ET.register_namespace("", ns)
    ET.register_namespace("image", ims)
    tree = ET.parse(sitemap_path)
    urlset = tree.getroot()
    press_url = base_url + "bleach-and-blood/press/"
    press_entry = next((u for u in urlset if u.find(f"{{{ns}}}loc") is not None
                        and u.find(f"{{{ns}}}loc").text == press_url), None)
    if press_entry is None:
        press_entry = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(press_entry, f"{{{ns}}}loc").text = press_url
    for old in list(press_entry):
        if old.tag == f"{{{ims}}}image":
            press_entry.remove(old)
    for name in ["cover-background.jpg", "title-logo.png"]:
        el = ET.SubElement(press_entry, f"{{{ims}}}image")
        ET.SubElement(el, f"{{{ims}}}loc").text = base_url + "images/bleach-and-blood/" + name
    for item in report:
        el = ET.SubElement(press_entry, f"{{{ims}}}image")
        ET.SubElement(el, f"{{{ims}}}loc").text = base_url + "images/bleach-and-blood/press/" + item["name"]
    ET.indent(tree, space="  ")
    tree.write(sitemap_path, encoding="unicode", xml_declaration=True)
    print(f"Imported {len(report)} optimized images and updated gallery/sitemap.", flush=True)

if __name__ == "__main__":
    run()
