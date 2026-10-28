# Convert all source images (HEIC/HEIF/JPG/PNG) -> WebP staging for selection.
# Long edge 1600px, quality 80, keep EXIF-orientation. Output slug: category_index.
import os, sys, json
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

SRC = r"C:/Users/ramad/Downloads/AIS -20261024T154403Z-1-001/AIS"
OUT = r"C:/Users/ramad/projects/ais-portfolio/_staging"
os.makedirs(OUT, exist_ok=True)

CATS = {
    "profile": ["PROFIL"],
    "tape":    ["PENELITIAN TAPE", "WORK/TAPE KETAN RESERCH OKTOBER 2025- APRIL 2026"],
    "enkapsulasi": ["PROJECT ENKAPSULASI"],
    "airmawar": ["PROJECT AIR MAWAR NON ALCOHOL"],
    "pkl":     ["PROJECT PKL", "WORK/MAGANG BBVET JULI-AGUSTUS 2025"],
    "labassist": ["WORK/LABORATORY ASSISTANT FEBRUARI-MEI 2026"],
    "turun":   ["WORK/TURUN TANGAN MALANG NOVEMBER 2024-NOVEMBER 2025"],
    "sertifikat": ["SERTIFIKAT"],
}

def cat_of(rel):
    for cat, dirs in CATS.items():
        for d in dirs:
            if rel.startswith(d + "/") or rel.startswith(d.replace("/", "\\") + "\\"):
                return cat
    return None

img_exts = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".bmp", ".webp"}
manifest = []
counts = {}

for root, _, files in os.walk(SRC):
    for fn in sorted(files):
        ext = os.path.splitext(fn)[1].lower()
        if ext not in img_exts:
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, SRC)
        cat = cat_of(rel)
        if not cat:
            print("UNMAPPED:", rel); continue
        counts[cat] = counts.get(cat, 0) + 1
        idx = counts[cat]
        try:
            img = Image.open(full)
            img = ImageOps.exif_transpose(img).convert("RGB")
        except Exception as e:
            # HEIF fallback: reopen as plain image
            try:
                img = Image.open(full).convert("RGB")
            except Exception as e2:
                print("SKIP", rel, e2); continue
        w, h = img.size
        if max(w, h) > 1600:
            img.thumbnail((1600, 1600), Image.LANCZOS)
        out_name = f"{cat}_{idx:02d}.webp"
        img.save(os.path.join(OUT, out_name), "WEBP", quality=80, method=6)
        manifest.append({"src": rel, "cat": cat, "out": out_name, "w": img.size[0], "h": img.size[1]})
        print("OK", cat, idx, rel, "->", out_name)

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("TOTAL", len(manifest), json.dumps(counts))
