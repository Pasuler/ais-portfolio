# Create public GitHub repo using Git Credential Manager's saved credential.
# Token is kept in memory and never printed or written to disk.
import json
import subprocess
import urllib.error
import urllib.request


def credential():
    proc = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        text=True, capture_output=True, check=True,
    )
    fields = dict(line.split("=", 1) for line in proc.stdout.splitlines() if "=" in line)
    return fields.get("username", ""), fields.get("password", "")


def request(url, token, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            body = json.loads(body)
        except Exception:
            pass
        return exc.code, body


user, token = credential()
if not token:
    raise SystemExit("No saved GitHub token found in Git Credential Manager.")
status, identity = request("https://api.github.com/user", token)
if status != 200:
    raise SystemExit(f"GitHub auth failed: HTTP {status}; {identity}")
print("Authenticated GitHub account:", identity.get("login"))
repo_url = "https://api.github.com/repos/" + identity["login"] + "/ais-portfolio"
status, repo = request(repo_url, token)
if status == 200:
    print("Repository already exists:", repo.get("html_url"))
elif status == 404:
    status, repo = request(
        "https://api.github.com/user/repos", token, "POST",
        {"name": "ais-portfolio", "description": "Professional portfolio of Ais Hidayatul Uyun, S.Si.",
         "private": False, "has_issues": False, "auto_init": False},
    )
    if status not in (200, 201):
        raise SystemExit(f"Repository creation failed: HTTP {status}; {repo}")
    print("Created public repository:", repo.get("html_url"))
else:
    raise SystemExit(f"Repository lookup failed: HTTP {status}; {repo}")
