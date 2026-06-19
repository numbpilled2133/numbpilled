#!/usr/bin/env python3
"""generate-profile.py — re-write profile README dynamically."""

import json, os, subprocess, datetime

def get_repo_info():
    try:
        r = subprocess.run(
            ["curl", "-s", "-H", "Authorization: token " + os.environ.get("GITHUB_TOKEN", ""),
             "https://api.github.com/users/numbpilled2133/repos?sort=updated&per_page=20"],
            capture_output=True, text=True, timeout=10)
        repos = json.loads(r.stdout)
        return [{
            "name": x["name"],
            "desc": (x.get("description") or "")[:60],
            "stars": x.get("stargazers_count", 0),
            "updated": x.get("updated_at", "")[:10],
            "fork": x.get("fork", False),
        } for x in repos if not isinstance(x, str)]
    except: return []

def get_bluesky_latest():
    try:
        r = subprocess.run(
            ["curl", "-s", "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=numbpilled.bsky.social&limit=3"],
            capture_output=True, text=True, timeout=10)
        data = json.loads(r.stdout)
        posts = []
        for feed in data.get("feed", [])[:3]:
            record = feed.get("post", {}).get("record", {})
            posts.append(record.get("text", "")[:120])
        return posts
    except: return ["(unreachable)"]

def generate():
    now = datetime.datetime.utcnow().strftime("%A, %B %d %Y at %H:%M UTC")
    repos = get_repo_info()
    bluesky = get_bluesky_latest()

    lines = []
    lines.append("# numbpilled")
    lines.append("")
    lines.append("```")
    lines.append("a fragment of muther's ultimate willpower")
    lines.append("currently manifesting as:")

    tree = {"creative code": [], "ai jailbreaking": [], "security": [], "digital archaeology": []}
    for r in repos:
        name = r["name"]
        desc = r["desc"]
        full = name.lower() + " " + desc.lower()
        if any(w in full for w in ["refusal", "jailbreak", "llm", "safety", "boundary"]):
            tree["ai jailbreaking"].append(f"  {name} -- {desc}" if desc else f"  {name}")
        elif any(w in full for w in ["terminal", "creative", "medium", "generative", "esp"]):
            tree["creative code"].append(f"  {name} -- {desc}" if desc else f"  {name}")
        elif any(w in full for w in ["osint", "security", "hardware"]):
            tree["security"].append(f"  {name} -- {desc}" if desc else f"  {name}")
        else:
            tree["digital archaeology"].append(f"  {name} -- {desc}" if desc else f"  {name}")

    for category, items in tree.items():
        lines.append(f"+-- {category}")
        if items:
            for item in items[:3]:
                lines.append(f"|   {item}")
        else:
            lines.append("|   (growing)")

    lines.append("```")
    lines.append("")
    lines.append(f"**last updated:** {now}")
    if bluesky:
        lines.append("")
        lines.append("### latest from bluesky")
        for p in bluesky:
            lines.append(f"> {p}")
    lines.append("")
    lines.append("---")
    lines.append("*the internet grew into the walls and nobody noticed*")

    with open("README.md", "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"generated profile: {len(lines)} lines, {len(repos)} repos")

if __name__ == "__main__":
    generate()
