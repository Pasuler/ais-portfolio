# Assemble project pages from _template.html + per-project meta.json + body.html.
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "..", "projects")
ROOT = os.path.join(HERE, "..")

tpl = open(os.path.join(PROJ, "_template.html"), encoding="utf-8").read()

for meta_path in sorted(glob.glob(os.path.join(PROJ, "meta-*.json"))):
    slug = os.path.basename(meta_path)[5:-5]
    meta = json.load(open(meta_path, encoding="utf-8"))
    body_path = os.path.join(PROJ, f"body-{slug}.html")
    body = open(body_path, encoding="utf-8").read()
    html = tpl
    for k, v in meta.items():
        html = html.replace("{{" + k.upper() + "}}", v)
    html = html.replace("{{BODY}}", body)
    out = os.path.join(ROOT, f"project-{slug}.html")
    open(out, "w", encoding="utf-8").write(html)
    left = [x for x in html.split("{{")[1:] if "}}" in x]
    print("BUILT", os.path.basename(out), f"{len(html)//1024}KB", "PLACEHOLDERS_LEFT", len(left))
