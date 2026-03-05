#!/usr/bin/env python3
"""Generate the Productivity Template Pack PDF"""
from fpdf import FPDF
import os

OUT = os.path.join(os.path.dirname(__file__), 'Ultimate-Productivity-Template-Pack.pdf')

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 107, 53)
        self.cell(0, 8, 'FELIX CREATIONS - Ultimate Productivity Template Pack', align='L')
        self.ln(2)
        self.set_draw_color(255, 107, 53)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, f'Page {self.page_no()} | felixfelicis7.gumroad.com', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(50, 50, 50)
        self.set_fill_color(255, 245, 240)
        self.cell(0, 10, title, fill=True, ln=True)
        self.ln(2)

    def body(self, txt):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, txt)
        self.ln(3)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# --- Cover Page ---
pdf.add_page()
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(255, 107, 53)
pdf.ln(20)
pdf.cell(0, 12, 'ULTIMATE PRODUCTIVITY', align='C', ln=True)
pdf.cell(0, 12, 'TEMPLATE PACK', align='C', ln=True)
pdf.ln(6)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, 'Stop winging your week. Start owning it.', align='C', ln=True)
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, 'Includes: Weekly Planner | Priority Matrix | 90-Day Goal Tracker', align='C', ln=True)
pdf.cell(0, 6, 'Meeting Notes Template | Sprint Board Guide', align='C', ln=True)
pdf.ln(20)
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(200, 200, 200)
pdf.cell(0, 6, 'felixfelicis7.gumroad.com', align='C', ln=True)

# --- Template 1: Weekly Planner ---
pdf.add_page()
pdf.section_title('TEMPLATE 1: WEEKLY PLANNER')
pdf.body('Use this template at the start of each week to map out your priorities, tasks, and goals. Review on Friday.')
pdf.ln(2)

pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(255, 107, 53)
pdf.cell(0, 8, f'Week of: _______________________', ln=True)
pdf.ln(2)

days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
for day in days:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 7, f'  {day}', fill=True, ln=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    for i in range(3):
        pdf.cell(8, 6, '', border=1)
        pdf.cell(0, 6, '  _______________________________________________', ln=True)
    pdf.ln(1)

# --- Template 2: Priority Matrix ---
pdf.add_page()
pdf.section_title('TEMPLATE 2: EISENHOWER PRIORITY MATRIX')
pdf.body('Categorise your tasks into 4 quadrants. Focus on Q1 and Q2. Delegate Q3. Eliminate Q4.')
pdf.ln(4)

matrix = [
    ('Q1: DO FIRST', 'Urgent + Important', '255,107,53'),
    ('Q2: SCHEDULE', 'Not Urgent + Important', '70,130,180'),
    ('Q3: DELEGATE', 'Urgent + Not Important', '100,160,100'),
    ('Q4: ELIMINATE', 'Not Urgent + Not Important', '160,160,160'),
]
for label, sub, color in matrix:
    r,g,b = map(int, color.split(','))
    pdf.set_fill_color(r,g,b)
    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(95, 8, f'  {label}', fill=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 8, f'  ({sub})', fill=True, ln=True)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Helvetica', '', 9)
    for i in range(5):
        pdf.cell(8, 6, str(i+1)+'.')
        pdf.cell(0, 6, '  _________________________________________', ln=True)
    pdf.ln(3)

# --- Template 3: 90-Day Goal Tracker ---
pdf.add_page()
pdf.section_title('TEMPLATE 3: 90-DAY GOAL TRACKER')
pdf.body('Set 3 goals for the next 90 days. Break each into monthly milestones and weekly actions.')
pdf.ln(2)

for g in range(1, 4):
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255,107,53)
    pdf.cell(0, 8, f'GOAL {g}:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60,60,60)
    pdf.cell(0, 7, 'Goal statement: ________________________________________', ln=True)
    pdf.cell(0, 7, 'Why it matters: _________________________________________', ln=True)
    pdf.cell(0, 7, 'Month 1 milestone: ______________________________________', ln=True)
    pdf.cell(0, 7, 'Month 2 milestone: ______________________________________', ln=True)
    pdf.cell(0, 7, 'Month 3 milestone: ______________________________________', ln=True)
    pdf.cell(0, 7, 'Weekly action: __________________________________________', ln=True)
    pdf.cell(0, 7, 'Success metric: _________________________________________', ln=True)
    pdf.ln(4)

# --- Template 4: Meeting Notes ---
pdf.add_page()
pdf.section_title('TEMPLATE 4: MEETING NOTES')
pdf.body('Fill this in before, during, and after every meeting to maximise output and accountability.')
pdf.ln(2)
fields = [
    'Meeting title:', 'Date/Time:', 'Attendees:', 'Objective:',
    '', 'KEY DISCUSSION POINTS', '1.', '2.', '3.', '4.',
    '', 'DECISIONS MADE', '1.', '2.', '3.',
    '', 'ACTION ITEMS', 'Who | What | By When',
    '_____ | __________________________ | _______',
    '_____ | __________________________ | _______',
    '_____ | __________________________ | _______',
    '', 'NEXT MEETING: _________________________',
]
for f in fields:
    if f in ('KEY DISCUSSION POINTS', 'DECISIONS MADE', 'ACTION ITEMS'):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(255,107,53)
    else:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(60,60,60)
    pdf.cell(0, 7, f, ln=True)

# --- Template 5: Sprint Board Guide ---
pdf.add_page()
pdf.section_title('TEMPLATE 5: PROJECT SPRINT BOARD')
pdf.body('Use this Kanban-style sprint board to track a 1-2 week project sprint.')
pdf.ln(2)

pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(50,50,50)
cols = ['BACKLOG', 'THIS WEEK', 'IN PROGRESS', 'DONE']
col_w = 45
for col in cols:
    pdf.set_fill_color(240,240,240)
    pdf.cell(col_w, 8, col, fill=True, border=1, align='C')
pdf.ln()

for row in range(8):
    for col in cols:
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(150,150,150)
        pdf.cell(col_w, 8, '  ...', border=1)
    pdf.ln()

pdf.ln(6)
pdf.set_font('Helvetica', 'I', 9)
pdf.set_text_color(120,120,120)
pdf.multi_cell(0, 6, 'Tip: Duplicate this board in Notion for a digital version. Limit "In Progress" to 3 tasks maximum to stay focused.')

# --- Notion Links Page ---
pdf.add_page()
pdf.section_title('BONUS: NOTION TEMPLATE LINKS')
pdf.body('Duplicate these free Notion templates to your workspace:')
pdf.ln(4)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(50,50,50)

links = [
    ('Weekly Planner', 'Coming soon - check felixfelicis7.gumroad.com for updates'),
    ('Priority Matrix', 'Coming soon - check felixfelicis7.gumroad.com for updates'),
    ('90-Day Goal Tracker', 'Coming soon - check felixfelicis7.gumroad.com for updates'),
    ('Sprint Board', 'Coming soon - check felixfelicis7.gumroad.com for updates'),
]
for name, url in links:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255,107,53)
    pdf.cell(0, 7, f'* {name}:', ln=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(80,80,200)
    pdf.cell(0, 6, f'  {url}', ln=True)
    pdf.ln(1)

pdf.ln(8)
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(80,80,80)
pdf.cell(0, 7, 'Questions? Email: felixfelicis01@proton.me', ln=True)
pdf.cell(0, 7, 'More templates: felixfelicis7.gumroad.com', ln=True)

pdf.output(OUT)
print(f'Generated: {OUT}')
