#!/usr/bin/env python3
"""
demand/trend-scraper.py — Felix Ops Demand Sensing
Runs every 6-12h. Uses Google Trends + Gumroad public pages.
Results saved to analytics/trends/YYYY-MM-DD.json
"""
import json, os, urllib.request, urllib.parse, re
from datetime import datetime

TODAY = datetime.now().strftime('%Y-%m-%d')
OUT_DIR = os.path.join(os.path.dirname(__file__), '../../analytics/trends')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, f'{TODAY}.json')

NICHES = ["notion template", "productivity template", "ai prompt pack",
          "chatgpt prompts", "budget spreadsheet", "digital planner",
          "finance tracker", "canva templates", "passive income"]

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"ERROR:{e}"

def gumroad_demand(kw):
    url = f"https://gumroad.com/discover?query={urllib.parse.quote(kw)}&sort=top"
    html = fetch(url)
    if html.startswith("ERROR"):
        return {"kw": kw, "error": html}
    # Extract product names and prices
    prices = re.findall(r'"\$[\d.]+(?:\+)?"', html)
    titles = re.findall(r'"name":"([^"]{5,80})"', html)[:5]
    return {"kw": kw, "price_points": len(prices), "sample_titles": titles[:3]}

def google_trends_daily(geo="AU"):
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    xml = fetch(url)
    if xml.startswith("ERROR"):
        return []
    topics = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', xml)
    return topics[:15]

def hacker_news_top():
    html = fetch("https://news.ycombinator.com/")
    if html.startswith("ERROR"):
        return []
    titles = re.findall(r'class="titleline"[^>]*><a[^>]*>([^<]{10,100})</a>', html)
    return titles[:10]

def run():
    print(f"[{TODAY}] Demand sensing...")
    results = {
        "date": TODAY,
        "timestamp": datetime.now().isoformat(),
        "google_trends_au": google_trends_daily("AU"),
        "hacker_news": hacker_news_top(),
        "gumroad_niches": [gumroad_demand(kw) for kw in NICHES],
    }
    # Load existing if exists and merge
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE) as f:
            existing = json.load(f)
        existing.update(results)
        results = existing
    with open(OUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    # Print summary
    print(f"  Google AU trends: {len(results['google_trends_au'])} topics")
    print(f"  HN top: {results['hacker_news'][:3]}")
    for n in results['gumroad_niches'][:3]:
        print(f"  Gumroad '{n['kw']}': {n.get('price_points',0)} prices, titles: {n.get('sample_titles',[])}")
    print(f"  Saved: {OUT_FILE}")

if __name__ == '__main__':
    run()
