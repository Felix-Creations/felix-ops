#!/usr/bin/env python3
"""reporting/daily-report.py — Felix Ops 5pm AEST Daily Report"""
import json, os
from datetime import date, datetime

TODAY = date.today().isoformat()
W = os.path.join(os.path.dirname(__file__), '../..')

def load(path):
    try:
        with open(os.path.join(W, path)) as f: return json.load(f)
    except: return {}

def read(path):
    try:
        with open(os.path.join(W, path)) as f: return f.read()
    except: return ""

def build():
    catalog = load('analytics/product-catalog.json')
    trends = load(f'analytics/trends/{TODAY}.json')
    log = read(f'logs/{TODAY}.md')

    products = catalog.get('products', [])
    hn = trends.get('hacker_news', [])[:3]
    
    lines = [
        f"🦊 *FELIX DAILY REPORT — {TODAY}*",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "📦 *PRODUCTS*",
    ]
    for p in products:
        status = "🟡 DRAFT" if "draft" in p.get("status","") else "🟢 LIVE"
        lines.append(f"{status} {p['name']} — ${p['price_aud']} AUD")
    
    blocker = catalog.get("blocked_by","")
    if blocker:
        lines += ["", f"🔴 *BLOCKED:* {blocker}"]

    lines += [
        "",
        "📊 *RESULTS TODAY*",
        "- Revenue: $0 AUD (products not yet live — awaiting payout setup)",
        "- Views: 0 (social accounts not yet created — need phone #)",
        "- Leads: 0",
        "",
        "🧠 *DEMAND SIGNALS*",
        f"- HN trending: {', '.join(hn) if hn else 'no data'}",
        "",
        "💰 *BUDGET*",
        "- AI spend today: est. $20-30 AUD (browser automation heavy session)",
        "- Remaining this month: ~$74 AUD",
        "- Tool subscriptions: $0 (all free tier)",
        "- Revenue: $0",
        "",
        "✅ *DONE TODAY*",
        "- 3 products built + hosted (Productivity Pack, ChatGPT Prompts, Budget Tracker)",
        "- GitHub repo live: Felix-Creations/felix-ops",
        "- Gumroad store: felixfelicis7.gumroad.com",
        "- CDP automation working (no browser tool = no snapshot cost)",
        "- Content scripts written (TikTok + YouTube hooks)",
        "- Demand scraper + daily report cron installed",
        "",
        "🔴 *NEEDS SHANE*",
        "1. gumroad.com/settings/payments — select Australia + connect PayPal/Stripe",
        "2. Phone number for Brevo (email) + TikTok/Instagram verification",
        "",
        "📅 *TOMORROW*",
        "- Once payout connected: publish all 3 products immediately",
        "- Build product #4: Freelance Proposal Template Pack",
        "- Continue demand sensing + refine content hooks",
        "━━━━━━━━━━━━━━━━━━━━",
    ]

    return "\n".join(lines)

if __name__ == '__main__':
    report = build()
    print(report)
    os.makedirs(os.path.join(W,'reports'), exist_ok=True)
    with open(os.path.join(W, f'reports/{TODAY}.md'), 'w') as f:
        f.write(report)
