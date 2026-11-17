"""subpost: share good things with a subreddit, with a person checking every post.

  draft   - write a post into the queue (nothing goes to Reddit)
  list    - show the queue and who approved what
  approve - a named person reads a draft and approves it
  post    - send approved posts, one at a time, slowly
  replies - list replies to our posts so a person can answer each one

Never: votes, direct messages, comments on other people's posts, the same
post in two subreddits, or keeping Reddit data.

Keys come from the environment:
  REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD
"""

import argparse
import base64
import datetime
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUEUE = ROOT / "queue"
API = "https://oauth.reddit.com"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
USER_AGENT = "script:subpost:1.0 (by /u/{user})"
GAP_SECONDS = 600  # at least ten minutes between posts


# ---- the queue (plain JSON files a person can read) ----

def fingerprint(title, body):
    return hashlib.sha256(f"{title}\n{body}".strip().lower().encode()).hexdigest()[:16]


def drafts():
    return sorted(QUEUE.glob("*.json"))


def load(path):
    return json.loads(path.read_text())


def save(path, item):
    path.write_text(json.dumps(item, indent=2) + "\n")


def draft(subreddit, title, url=None, text=None, why=""):
    if not (url or text):
        sys.exit("Give --url or --text.")
    key = fingerprint(title, url or text)
    for p in drafts():
        old = load(p)
        if old["fingerprint"] == key and old["subreddit"].lower() != subreddit.lower():
            sys.exit(f"This post is already queued for r/{old['subreddit']}. Write a new one for r/{subreddit}.")
    QUEUE.mkdir(exist_ok=True)
    path = QUEUE / f"{datetime.date.today()}-{subreddit.lower()}-{key[:6]}.json"
    save(path, {"subreddit": subreddit, "title": title, "url": url, "text": text,
                "why": why, "fingerprint": key, "approved_by": None, "posted": None})
    print(f"Queued {path.name}. A person approves it with: subpost approve {path.stem} --by NAME")


def show():
    for p in drafts():
        i = load(p)
        state = "posted" if i["posted"] else f"approved by {i['approved_by']}" if i["approved_by"] else "waiting"
        print(f"{p.stem:40} r/{i['subreddit']:20} {state:24} {i['title']}")


def approve(name, by):
    path = QUEUE / f"{name}.json"
    if not path.exists():
        sys.exit(f"No draft called {name}.")
    item = load(path)
    item["approved_by"] = by
    save(path, item)
    print(f"Approved by {by}.")


# ---- Reddit ----

def env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing {name}. Set it in the environment first.")
    return value


def call(url, headers, data=None, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=30) as r:
            if float(r.headers.get("x-ratelimit-remaining") or 100) < 5:
                time.sleep(float(r.headers.get("x-ratelimit-reset") or 60))
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Reddit answered {e.code}: {e.read()[:300].decode(errors='replace')}")


def session():
    user = env("REDDIT_USERNAME")
    agent = USER_AGENT.format(user=user)
    basic = base64.b64encode(f"{env('REDDIT_CLIENT_ID')}:{env('REDDIT_SECRET')}".encode()).decode()
    reply = call(TOKEN_URL, {"Authorization": f"Basic {basic}", "User-Agent": agent},
                 data={"grant_type": "password", "username": user, "password": env("REDDIT_PASSWORD")})
    if not reply.get("access_token"):
        sys.exit(f"Reddit refused the login: {reply}")
    return {"Authorization": f"bearer {reply['access_token']}", "User-Agent": agent}


def post():
    ready = [p for p in drafts() if load(p)["approved_by"] and not load(p)["posted"]]
    if not ready:
        print("Nothing approved and waiting.")
        return
    headers = session()
    for n, path in enumerate(ready):
        if n:
            time.sleep(GAP_SECONDS)
        item = load(path)
        data = {"sr": item["subreddit"], "title": item["title"], "api_type": "json"}
        data.update({"kind": "link", "url": item["url"]} if item["url"] else {"kind": "self", "text": item["text"]})
        result = call(f"{API}/api/submit", headers, data=data).get("json", {})
        if result.get("errors"):
            sys.exit(f"Reddit said no to {path.stem}: {result['errors']}")
        item["posted"] = result.get("data", {}).get("url") or str(datetime.datetime.now())
        save(path, item)
        print(f"Posted {path.stem}: {item['posted']}")


def replies():
    headers = session()
    for child in call(f"{API}/message/inbox", headers, params={"limit": 50}).get("data", {}).get("children", []):
        c = child["data"]
        if c.get("was_comment"):
            print(f"r/{c['subreddit']}  u/{c['author']}: {c['body'][:200]}\n  https://www.reddit.com{c['context']}\n")


def main():
    p = argparse.ArgumentParser(prog="subpost", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft")
    d.add_argument("subreddit")
    d.add_argument("title")
    d.add_argument("--url")
    d.add_argument("--text")
    d.add_argument("--why", default="", help="why this helps that community")
    sub.add_parser("list")
    a = sub.add_parser("approve")
    a.add_argument("name")
    a.add_argument("--by", required=True, help="the person who read it")
    sub.add_parser("post")
    sub.add_parser("replies")
    args = p.parse_args()
    if args.cmd == "draft":
        draft(args.subreddit, args.title, args.url, args.text, args.why)
    elif args.cmd == "list":
        show()
    elif args.cmd == "approve":
        approve(args.name, args.by)
    elif args.cmd == "post":
        post()
    else:
        replies()


if __name__ == "__main__":
    main()
