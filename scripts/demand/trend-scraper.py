#!/usr/bin/env python3
"""
demand/trend-scraper.py
Felix Ops — Demand Sensing Module
Runs every 6-12 hours. Pulls trending data from free sources.
Stores results in analytics/trends/YYYY-MM-DD.json
"""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../../analytics/trends')
os.makedirs(OUTPUT_DIR, exist_ok=True)

TODAY = datetime.now().strftime('%Y-%m-%d')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'{TODAY}.json')

NICHES = [
    "notion template",
    "productivity template",
    "ai prompt pack",
    "chatgpt prompts",
    "budget spreadsheet",
    "digital planner",
    "finance tracker",
    "passive income",
    "digital products",
    "canva templates",
]

def fetch_google_trends_rss(keyword):
    """Fetch Google Trends RSS for a keyword (free, no auth)."""
    encoded = urllib.parse.quote(keyword)
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo=AU"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"ERROR: {e}"

def fetch_gumroad_discover(keyword):
    """Check Gumroad discover for a keyword — free public endpoint."""
    encoded = urllib.parse.quote(keyword)
    url = f"https://gumroad.com/discover?query={encoded}&sort=top"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Count product listings as a proxy for demand
            product_count = content.count('"productCard"') + content.count('class="product"')
            return {"query": keyword, "gumroad_results_proxy": product_count}
    except Exception as e:
        return {"query": keyword, "error": str(e)}

def fetch_reddit_hot(subreddit):
    """Fetch hot posts from a subreddit — free JSON endpoint."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'felix-demand-bot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            posts = data.get('data', {}).get('children', [])
            return [
                {
                    "title": p['data']['title'],
                    "score": p['data']['score'],
                    "comments": p['data']['num_comments'],
                    "url": f"https://reddit.com{p['data']['permalink']}"
                }
                for p in posts[:10]
            ]
    except Exception as e:
        return [{"error": str(e)}]

SUBREDDITS = [
    "passive_income",
    "EntrepreneurRideAlong",
    "SideProject",
    "digitalmarketing",
    "productivity",
]

def run():
    print(f"[{TODAY}] Felix Demand Sensing — starting...")
    results = {
        "date": TODAY,
        "timestamp": datetime.now().isoformat(),
        "reddit": {},
        "gumroad_demand": [],
    }

    # Reddit hot posts
    for sub in SUBREDDITS:
        print(f"  Fetching r/{sub}...")
        results["reddit"][sub] = fetch_reddit_hot(sub)

    # Gumroad demand proxy
    for kw in NICHES:
        print(f"  Gumroad check: {kw}...")
        results["gumroad_demand"].append(fetch_gumroad_discover(kw))

    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  Saved to {OUTPUT_FILE}")
    return results

if __name__ == '__main__':
    run()
