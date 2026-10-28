# Project Instructions

## Overview
Static professional portfolio for Ais Hidayatul Uyun, Biology graduate. Stack: HTML5, CSS3, vanilla JavaScript, optimized WebP. Runtime: browser. Hosting: GitHub Pages. No package manager or build step.

## Commands

Preview:

```sh
python -m http.server 8099 --bind 127.0.0.1
```

Build generated project pages after editing `projects/meta-*.json` or `projects/body-*.html`:

```sh
python tools/build_projects.py
```

Run the optimized image conversion/selection tools only when updating images; they require Pillow and pillow-heif.

## Conventions
Use semantic HTML, English identifiers/comments, Indonesian user-facing copy, relative asset paths, and accessible image alt text. Use CSS tokens in `assets/css/site.css` and no external JS dependencies. Example: `<img src="assets/img/card-tape.webp" alt="Koloni BAL pada cawan Petri" loading="lazy">`.

## Boundaries
NEVER touch `.env`, secrets, session files, credentials, private keys, vendor folders, generated browser profiles, production config, or unrelated user data. Do not modify the original Downloads dataset. Do not publish unsupported personal claims.

## Dependencies
No runtime dependencies. Image tooling: Python 3, Pillow, pillow-heif; score tool optionally uses OpenCV. Local verification tools may use Node.js and `ws`.

## Configuration
No runtime configuration. Canonical URL in `index.html` must be updated to the final GitHub Pages URL before publication.

## Error Handling
Keep links relative for GitHub Pages project sites. Verify every local `src`/`href` target after edits. Avoid claiming success for GitHub deployment without checking repository, Pages settings, and published URL.

## Troubleshooting
GitHub Pages may take several minutes after enabling. A 404 on project pages usually means incorrect relative paths or Pages publishing source is not repository root.
