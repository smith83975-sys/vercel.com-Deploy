#!/usr/bin/env python3
"""Build the VaultPulse Daily Brief and send it via MailerLite.
Usage: python3 scripts/send_brief.py [--dry-run]   (--dry-run = create draft campaign only, never send)
Token: env MAILERLITE_API_KEY or /home/box/.mailerlite_token (never printed)."""
import os, sys, json, subprocess, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://connect.mailerlite.com/api"
GROUP_ID = os.environ.get("MAILERLITE_GROUP_ID", "201346253191120872")
FROM, FROM_NAME = "mark@vaultpulsehq.com", "VaultPulse"

def token():
    t = os.environ.get("MAILERLITE_API_KEY")
    if not t:
        with open(os.path.expanduser("/home/box/.mailerlite_token")) as f: t = f.read().strip()
    return t

def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read(); return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"MailerLite {method} {path} -> {e.code}: {e.read().decode()[:500]}")

def main():
    dry = "--dry-run" in sys.argv
    out = "/tmp/vp_brief.html"
    line = subprocess.run([sys.executable, os.path.join(HERE, "daily_brief_html.py"), out, "/tmp/vp_brief.md"],
                          check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    subject = line.split(" | ", 1)[1].strip()
    html = open(out).read()
    c = call("POST", "/campaigns", {"name": subject + (" [dry run]" if dry else ""), "type": "regular",
        "emails": [{"subject": subject, "from_name": FROM_NAME, "from": FROM, "content": html}], "groups": [GROUP_ID]})["data"]
    print("campaign", c["id"], c.get("status"), "|", subject)
    if dry:
        print("dry run: draft only, not scheduled"); return c["id"]
    s = call("POST", f"/campaigns/{c['id']}/schedule", {"delivery": "instant"})["data"]
    print("scheduled:", s.get("status"))
    return c["id"]

if __name__ == "__main__":
    main()
