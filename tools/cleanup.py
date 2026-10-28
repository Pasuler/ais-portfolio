import os
import shutil

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets = ["_staging", "_shots", "tools/node_modules", "tools/package-lock.json", "tools/verify.cjs", "tools/verify_render.py"]
for item in targets:
    path = os.path.join(root, item)
    if os.path.isdir(path):
        shutil.rmtree(path)
        print("removed", item)
    elif os.path.exists(path):
        os.remove(path)
        print("removed", item)
