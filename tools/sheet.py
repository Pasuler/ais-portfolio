# Build labeled contact sheets per category so the best images can be picked visually.
import os, json, math
from PIL import Image, ImageDraw, ImageFont

STAGE = r"C:/Users/ramad/projects/ais-portfolio/_staging"
manifest = json.load(open(os.path.join(STAGE, "manifest.json"), encoding="utf-8"))

by_cat = {}
for m in manifest:
    by_cat.setdefault(m["cat"], []).append(m)

CELL, COLS, PAD, LBL = 320, 5, 8, 22
try:
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
except Exception:
    font = ImageFont.load_default()

for cat, items in by_cat.items():
    items.sort(key=lambda x: x["out"])
    rows = math.ceil(len(items) / COLS)
    W = COLS * (CELL + PAD) + PAD
    H = rows * (CELL + LBL + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (250, 250, 247))
    d = ImageDraw.Draw(sheet)
    for i, m in enumerate(items):
        r, c = divmod(i, COLS)
        x = PAD + c * (CELL + PAD)
        y = PAD + r * (CELL + LBL + PAD)
        im = Image.open(os.path.join(STAGE, m["out"]))
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        # center on white tile
        tile = Image.new("RGB", (CELL, CELL), (235, 235, 232))
        tile.paste(im, ((CELL - im.size[0]) // 2, (CELL - im.size[1]) // 2))
        sheet.paste(tile, (x, y))
        d.text((x + 2, y + CELL + 3), m["out"].replace(".webp", ""), fill=(20, 24, 15), font=font)
    out = os.path.join(STAGE, f"_sheet_{cat}.jpg")
    sheet.save(out, "JPEG", quality=85)
    print(out, sheet.size, len(items))
