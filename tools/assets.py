# Copy + crop selected staged images into final assets/img with per-use sizes.
import os, json
from PIL import Image

STAGE = r"C:/Users/ramad/projects/ais-portfolio/_staging"
OUT = r"C:/Users/ramad/projects/ais-portfolio/assets/img"

# slug -> (source, kind)  kind: 'wide' 16:10 crop, 'tall' 4:5 crop, 'full' keep aspect max 1400
SEL = {
    # hero / profile
    "profile-hero":      ("profile_06.webp", "tall"),
    # home project card thumbs (16:10)
    "card-tape":         ("tape_03.webp", "wide"),
    "card-enkapsulasi":  ("enkapsulasi_08.webp", "wide"),
    "card-pkl":          ("pkl_02.webp", "wide"),
    "card-airmawar":     ("airmawar_02.webp", "wide"),
    "card-labassist":    ("labassist_01.webp", "wide"),
    "card-turun":        ("turun_03.webp", "wide"),
    # tape project gallery
    "tape-a": ("tape_02.webp", "wide"),
    "tape-b": ("tape_03.webp", "wide"),
    "tape-c": ("tape_04.webp", "wide"),
    "tape-d": ("tape_07.webp", "wide"),
    "tape-e": ("tape_08.webp", "wide"),
    "tape-f": ("tape_12.webp", "wide"),
    "tape-g": ("tape_19.webp", "wide"),
    "tape-h": ("tape_21.webp", "wide"),
    # enkapsulasi
    "enk-a": ("enkapsulasi_02.webp", "wide"),
    "enk-b": ("enkapsulasi_03.webp", "wide"),
    "enk-c": ("enkapsulasi_04.webp", "wide"),
    "enk-d": ("enkapsulasi_06.webp", "wide"),
    "enk-e": ("enkapsulasi_07.webp", "wide"),
    "enk-f": ("enkapsulasi_08.webp", "wide"),
    # pkl
    "pkl-a": ("pkl_02.webp", "wide"),
    "pkl-b": ("pkl_03.webp", "wide"),
    "pkl-c": ("pkl_06.webp", "wide"),
    "pkl-d": ("pkl_08.webp", "wide"),
    "pkl-e": ("pkl_09.webp", "wide"),
    "pkl-f": ("pkl_01.webp", "wide"),
    "pkl-g": ("pkl_13.webp", "wide"),
    "pkl-h": ("pkl_16.webp", "wide"),
    # air mawar
    "rose-a": ("airmawar_02.webp", "wide"),
    "rose-b": ("airmawar_03.webp", "wide"),
    "rose-c": ("airmawar_04.webp", "wide"),
    "rose-d": ("airmawar_01.webp", "tall"),
    # work / organisation
    "turun-a": ("turun_03.webp", "wide"),
    "turun-b": ("turun_07.webp", "wide"),
    "turun-c": ("turun_09.webp", "wide"),
    "lab-a":   ("labassist_01.webp", "wide"),
    "lab-b":   ("labassist_03.webp", "wide"),
    # certificates
    "cert-ttm":  ("sertifikat_01.webp", "full"),
    "cert-pohon":("sertifikat_02.webp", "full"),
}

def crop(img, ratio):
    w, h = img.size
    target = ratio
    cur = w / h
    if cur > target:            # too wide -> crop sides
        nw = int(h * target)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    else:                       # too tall -> crop top-biased
        nh = int(w / target)
        y = max(0, int((h - nh) * 0.30))
        return img.crop((0, y, w, y + nh))

written = []
for slug, (src, kind) in SEL.items():
    p = os.path.join(STAGE, src)
    if not os.path.exists(p):
        print("MISSING", src); continue
    im = Image.open(p).convert("RGB")
    if kind == "wide":
        im = crop(im, 16 / 10)
        im.thumbnail((1400, 875), Image.LANCZOS)
    elif kind == "tall":
        im = crop(im, 4 / 5)
        im.thumbnail((900, 1125), Image.LANCZOS)
    else:
        im.thumbnail((1400, 1400), Image.LANCZOS)
    out = os.path.join(OUT, slug + ".webp")
    im.save(out, "WEBP", quality=82, method=6)
    written.append((slug, im.size, os.path.getsize(out)))

total = 0
for s, size, byt in written:
    total += byt
    print(f"{s:18s} {size[0]:4d}x{size[1]:4d} {byt/1024:7.1f} KB")
print("FILES", len(written), "TOTAL", round(total / 1024 / 1024, 2), "MB")
