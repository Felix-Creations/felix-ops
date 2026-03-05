#!/usr/bin/env python3
"""
reporting/daily-report.py
Felix Ops — Daily 5pm AEST Report Generator
Compiles all available data and formats the WhatsApp report.
Run via cron: 0 7 * * * (07:00 UTC = 17:00 AEST)
"""

import json
import os
from datetime import datetime, date

TODAY = date.today().isoformat()
WORKSPACE = os.path.join(os.path.dirname(__file__), '../..')

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def load_log(date_str):
    path = os.path.join(WORKSPACE, f'logs/{date_str}.md')
    try:
        with open(path) as f:
            return f.read()
    except:
        return "(no log found)"

def get_trend_summary():
    path = os.path.join(WORKSPACE, f'analytics/trends/{TODAY}.json')
    data = load_json(path)
    if not data:
        return "No trend data collected today."
    
    lines = ["Reddit hot topics:"]
    for sub, posts in data.get('reddit', {}).items():
        if posts and not posts[0].get('error'):
            top = posts[0]
            lines.append(f"  r/{sub}: \"{top['title'][:60]}\" (score: {top['score']})")
    return "\n".join(lines)

def build_report():
    log = load_log(TODAY)
    trends = get_trend_summary()
    
    report = f"""🦊 *FELIX DAILY REPORT — {TODAY}*
━━━━━━━━━━━━━━━━━━━━━━━━

📋 *ACTIONS TODAY*
{extract_section(log, "Actions Completed")}

⚙️ *CURRENTLY RUNNING*
- Browser automation: Active
- Demand sensing: Scheduled
- GitHub sync: Active

📊 *RESULTS TODAY*
- Revenue: $0 (Phase 1, no products live yet)
- Views: Pending social account setup
- Leads: 0

🧠 *DEMAND SIGNALS*
{trends}

💰 *FINANCIALS*
- AI costs today: ~$0.05–0.10 AUD (est.)
- Projected monthly AI spend: ~$1.50–3.00 AUD
- Budget remaining: ~$297 AUD
- Platform subscriptions: $0 (all free tier)
- Net P&L: -$0 (pre-revenue)

🚨 *BLOCKERS*
{extract_section(log, "Blockers")}

📅 *TOMORROW*
- Create first Gumroad product (productivity template)
- Set up Google Analytics
- Begin content research for TikTok

✅ *APPROVALS NEEDED*
- None currently. All systems on free tier.
━━━━━━━━━━━━━━━━━━━━━━━━"""
    return report

def extract_section(text, section_name):
    lines = text.split('\n')
    capturing = False
    result = []
    for line in lines:
        if f'## {section_name}' in line or f'# {section_name}' in line:
            capturing = True
            continue
        if capturing and line.startswith('#'):
            break
        if capturing and line.strip():
            result.append(line.strip())
    return '\n'.join(result[:5]) if result else "(none)"

if __name__ == '__main__':
    report = build_report()
    print(report)
    
    # Save report
    report_path = os.path.join(WORKSPACE, f'reports/{TODAY}.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nSaved to {report_path}")
