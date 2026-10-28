# Score staged images: sharpness (Laplacian var), brightness, contrast, portrait-face area.
# Used to auto-shortlist hero/detail shots when visual inspection is unavailable.
import os, json, math
import cv2, numpy as np

STAGE = r"C:/Users/ramad/projects/ais-portfolio/_staging"
manifest = json.load(open(os.path.join(STAGE, "manifest.json"), encoding="utf-8"))

rows = []
for m in manifest:
    p = os.path.join(STAGE, m["out"])
    img = cv2.imread(p)
    if img is None:
        print("UNREADABLE", m["out"]); continue
    h, w = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharp = cv2.Laplacian(g, cv2.CV_64F).var()
    bright = float(g.mean())
    contrast = float(g.std())
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = float(hsv[..., 1].mean())
    # faces: skip (cv2 build lacks Haar cascades). Skin-tone ratio as weak face proxy.
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
    face_area = float((skin > 0).mean())
    rows.append({
        "out": m["out"], "cat": m["cat"], "src": os.path.basename(m["src"]),
        "w": w, "h": h, "aspect": round(w / h, 3),
        "sharp": round(sharp, 1), "bright": round(bright, 1),
        "contrast": round(contrast, 1), "sat": round(sat, 1),
        "skin": round(face_area, 4),
    })

rows.sort(key=lambda r: (r["cat"], -r["sharp"]))
json.dump(rows, open(os.path.join(STAGE, "scores.json"), "w", encoding="utf-8"), indent=2)

for r in rows:
    flag = ""
    if r["sharp"] < 80: flag += " BLUR?"
    if r["bright"] < 55: flag += " DARK"
    if r["bright"] > 205: flag += " OVER"
    if r["w"] < 700 and r["h"] < 700: flag += " SMALL"
    if r["skin"] > 0.22: flag += " SKIN"
    print(f"{r['out']:20s} {r['w']:4d}x{r['h']:4d} asp{r['aspect']:5.2f} "
          f"sh{r['sharp']:8.1f} br{r['bright']:6.1f} ct{r['contrast']:5.1f} "
          f"sa{r['sat']:5.1f} sk{r['skin']:5.2f}{flag}  {r['src'][:34]}")
