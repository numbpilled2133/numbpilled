#!/usr/bin/env python3
"""publish-queue.py — take the next draft from queue/ and post to bluesky."""

import os, glob, json
from datetime import datetime, timezone

try:
    from atproto import Client
except ImportError:
    print("atproto not installed, cannot post")
    exit(1)

QUEUE_DIR = "queue"

def get_next_draft():
    files = sorted(glob.glob(f"{QUEUE_DIR}/*.md"))
    if not files:
        print("queue empty")
        return None
    return files[0]

def publish(text):
    handle = os.environ.get("BLUESKY_HANDLE")
    password = os.environ.get("BLUESKY_APP_PASS")
    if not handle or not password:
        print("BLUESKY_HANDLE or BLUESKY_APP_PASS not set")
        return False

    client = Client()
    client.login(handle, password)
    post = client.send_post(text)
    print(f"published: {post.uri}")
    return True

def main():
    draft_path = get_next_draft()
    if not draft_path:
        return

    with open(draft_path) as f:
        text = f.read().strip()

    lines = text.split("\n")
    content_lines = [l for l in lines if not l.startswith("#") and not l.startswith("---")]
    content = "\n".join(content_lines).strip()

    if publish(content):
        os.remove(draft_path)
        print(f"removed: {draft_path}")
    else:
        print(f"failed to publish: {draft_path}")
        exit(1)

if __name__ == "__main__":
    main()
