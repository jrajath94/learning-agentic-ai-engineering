#!/usr/bin/env python3
"""Push one large file via the Git Data API (Contents API caps at 1 MB)."""
import base64, json, os, sys, time, urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

OWNER, REPO, BRANCH = "jrajath94", "learning-agentic-ai-engineering", "build/power-user-hub-v1"
API = "https://api.github.com"
LOCAL = os.path.expanduser("~/workspace/learning-agentic-site/site/assets/js/mermaid.min.js")
PATH = "site/assets/js/mermaid.min.js"

def req(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data: r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)

ref = req("GET", f"{API}/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
head_sha = ref["object"]["sha"]
head = req("GET", f"{API}/repos/{OWNER}/{REPO}/git/commits/{head_sha}")
base_tree = head["tree"]["sha"]
blob = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/blobs",
           {"content": base64.b64encode(open(LOCAL, "rb").read()).decode(), "encoding": "base64"})
tree = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/trees",
           {"base_tree": base_tree, "tree": [{"path": PATH, "mode": "100644", "type": "blob", "sha": blob["sha"]}]})
commit = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/commits",
             {"message": "Bundle Mermaid library locally for offline render", "tree": tree["sha"], "parents": [head_sha]})
req("PATCH", f"{API}/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}", {"sha": commit["sha"]})
print("big file pushed, blob", blob["sha"][:12], "size", os.path.getsize(LOCAL))
