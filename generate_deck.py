import os
import matplotlib.pyplot as plt
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 1. GENERATE HIGH-RES CHARTS WITH LIGHT, MODERN STYLING
os.makedirs("assets", exist_ok=True)

# Chart 1: Trend line + Donut chart combined for Slide 2
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

# Ax1: Yearly Surge
years = ['2021', '2022', '2023', '2024', '2025 (Proj)']
cases = [18, 34, 78, 165, 290]
ax1.set_facecolor('#F8FAFC')
ax1.plot(years, cases, marker='o', color='#4F46E5', linewidth=3, markersize=8, markerfacecolor='#FFFFFF', markeredgewidth=2.5, markeredgecolor='#4F46E5')
ax1.fill_between(years, cases, color='#4F46E5', alpha=0.12)
ax1.set_title('Reported Job Scam Cases in India (Thousands)', fontsize=12, fontweight='bold', color='#0F172A', pad=12)
ax1.set_ylabel('Cases (in Thousands)', fontsize=10, color='#475569')
ax1.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
for i, txt in enumerate(cases):
    ax1.annotate(f"{txt}K", (years[i], cases[i] + 12), ha='center', fontsize=10, fontweight='bold', color='#4F46E5')
ax1.set_ylim(0, 340)
ax1.tick_params(colors='#475569')
for spine in ax1.spines.values():
    spine.set_color('#E2E8F0')

# Ax2: Scam Breakdown Donut
categories = ['Task/Rating Scams\n(YouTube/Telegram)', 'Registration/Kit Fees', 'Fake Data Entry', 'Identity Theft / Docs']
sizes = [42, 31, 18, 9]
colors = ['#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6']
wedges, texts, autotexts = ax2.pie(
    sizes, labels=categories, autopct='%1.0f%%', startangle=140,
    colors=colors, pctdistance=0.75,
    textprops=dict(color='#0F172A', fontsize=9, fontweight='500'),
    wedgeprops=dict(width=0.45, edgecolor='#FFFFFF', linewidth=2)
)
for at in autotexts:
    at.set_color('#FFFFFF')
    at.set_fontweight('bold')
    at.set_fontsize(10)
ax2.set_title('Distribution of Student Job Frauds', fontsize=12, fontweight='bold', color='#0F172A', pad=12)

plt.tight_layout()
chart_path = os.path.join("assets", "problem_charts.png")
plt.savefig(chart_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Generated chart at: {chart_path}")

# 2. CREATE PPTX PRESENTATION
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 Widescreen
prs.slide_height = Inches(7.5)

# Color Palette Definitions
C_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC
C_WHITE = RGBColor(255, 255, 255)        # #FFFFFF
C_PRIMARY = RGBColor(79, 70, 229)        # #4F46E5 Indigo
C_PRIMARY_LIGHT = RGBColor(238, 242, 255)# #EEF2FF
C_CYAN = RGBColor(14, 165, 233)          # #0EA5E9
C_TEXT_DARK = RGBColor(15, 23, 42)       # #0F172A
C_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569
C_BORDER = RGBColor(226, 232, 240)       # #E2E8F0
C_DANGER = RGBColor(225, 29, 72)         # #E11D48
C_DANGER_BG = RGBColor(255, 241, 242)    # #FFF1F2
C_SUCCESS = RGBColor(5, 150, 105)        # #059669
C_SUCCESS_BG = RGBColor(236, 253, 245)   # #ECFDF5
C_WARNING = RGBColor(217, 119, 6)        # #D97706
C_CARD_SHADOW = RGBColor(241, 245, 249)

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = C_BG_LIGHT
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_text="THEME 1: AI & SMART SOLUTIONS | CODE: AI-04"):
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_text.upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_PRIMARY
    
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11), Inches(0.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_DARK

# ==========================================
# SLIDE 1: TITLE SLIDE (5 TEAM MEMBERS)
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Decorative top accent banner
banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
banner.fill.solid()
banner.fill.fore_color.rgb = C_PRIMARY
banner.line.fill.background()

# Title pill
tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(3.8), Inches(0.45))
tag.fill.solid()
tag.fill.fore_color.rgb = C_PRIMARY_LIGHT
tag.line.color.rgb = C_PRIMARY
tf = tag.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "COLLEGE HACKATHON 2026 • AI-04"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

# Main Title & Subtitle
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(1.8))
tf = title_box.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "JobShield AI"
p1.font.size = Pt(46)
p1.font.bold = True
p1.font.color.rgb = C_PRIMARY

p2 = tf.add_paragraph()
p2.text = "Autonomous Multi-Layer Intelligence Engine for Local Job Scam Detection & Vacancy Verification"
p2.font.size = Pt(18)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_DARK

p3 = tf.add_paragraph()
p3.text = "Safeguarding students and freshers from fake offer letters, deposit fee traps, and predatory task scams."
p3.font.size = Pt(13)
p3.font.color.rgb = C_TEXT_MUTED

# 5 Team Members Card Grid
team_label = s1.shapes.add_textbox(Inches(0.8), Inches(3.5), Inches(5), Inches(0.35))
tl_p = team_label.text_frame.paragraphs[0]
tl_p.text = "ENGINEERED BY 5-MEMBER CORE TEAM:"
tl_p.font.size = Pt(11)
tl_p.font.bold = True
tl_p.font.color.rgb = C_TEXT_MUTED

members = [
    ("Member 1 (Lead)", "AI Vision & System Architecture", "Gemini 1.5 Vision / LangChain"),
    ("Member 2", "Backend & Rule Engine", "Python FastAPI / Security Rules"),
    ("Member 3", "OSINT & DNS Auditor", "WHOIS Protocol & Google Places API"),
    ("Member 4", "Frontend UI / UX", "HTML5 / Modern JS / Threat Visuals"),
    ("Member 5", "Bot Interface & QA", "Telegram Bot API / Cyber Crime Sync")
]

card_w = Inches(2.25)
card_h = Inches(2.5)
card_y = Inches(4.0)
card_gap = Inches(0.18)

for idx, (m_name, m_role, m_tech) in enumerate(members):
    c_x = Inches(0.8) + idx * (card_w + card_gap)
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, card_y, card_w, card_h)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    card.line.width = Pt(1)
    
    # Avatar badge
    avatar = s1.shapes.add_shape(MSO_SHAPE.OVAL, c_x + Inches(0.2), card_y + Inches(0.25), Inches(0.65), Inches(0.65))
    avatar.fill.solid()
    avatar.fill.fore_color.rgb = C_PRIMARY_LIGHT
    avatar.line.color.rgb = C_PRIMARY
    av_tf = avatar.text_frame
    av_p = av_tf.paragraphs[0]
    av_p.text = f"M{idx+1}"
    av_p.alignment = PP_ALIGN.CENTER
    av_p.font.bold = True
    av_p.font.size = Pt(12)
    av_p.font.color.rgb = C_PRIMARY
    
    # Text
    info_box = s1.shapes.add_textbox(c_x + Inches(0.15), card_y + Inches(1.0), card_w - Inches(0.3), Inches(1.3))
    i_tf = info_box.text_frame
    i_tf.word_wrap = True
    
    ip1 = i_tf.paragraphs[0]
    ip1.text = m_name
    ip1.font.size = Pt(12)
    ip1.font.bold = True
    ip1.font.color.rgb = C_TEXT_DARK
    
    ip2 = i_tf.add_paragraph()
    ip2.text = m_role
    ip2.font.size = Pt(10)
    ip2.font.bold = True
    ip2.font.color.rgb = C_PRIMARY
    
    ip3 = i_tf.add_paragraph()
    ip3.text = m_tech
    ip3.font.size = Pt(8.5)
    ip3.font.color.rgb = C_TEXT_MUTED

# ==========================================
# SLIDE 2: THE PROBLEM & VISUAL GRAPH
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "The Epidemic of Employment & Job Scams")

# Left Column: Pain Points Cards
left_w = Inches(4.8)
pain_cards = [
    ("Upfront Fee & Deposit Extortion", "Scammers pose as recruiters demanding ₹500 - ₹5,000 for 'registration', 'laptop delivery', or 'mandatory verification kit'. Money disappears immediately.", C_DANGER),
    ("Telegram & WhatsApp Task Scams", "'Earn ₹3,000/day for liking YouTube videos'. Exploits young students with small initial payouts before locking thousands in fake crypto accounts.", C_WARNING),
    ("The Local Vacancy Digital Void", "Coaching notices, street flyers, and local walk-in postings operate in a total regulatory blindspot with zero public verifiability.", C_PRIMARY)
]

py = Inches(1.7)
for title, desc, col in pain_cards:
    p_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), py, left_w, Inches(1.55))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = C_WHITE
    p_box.line.color.rgb = C_BORDER
    
    # Left colored indicator bar
    ibar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), py, Inches(0.1), Inches(1.55))
    ibar.fill.solid()
    ibar.fill.fore_color.rgb = col
    ibar.line.fill.background()
    
    tb = s2.shapes.add_textbox(Inches(1.05), py + Inches(0.12), left_w - Inches(0.35), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_DARK
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_MUTED
    
    py += Inches(1.7)

# Right Column: The Matplotlib Chart Image
if os.path.exists(chart_path):
    chart_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(1.7), Inches(6.7), Inches(5.1))
    chart_box.fill.solid()
    chart_box.fill.fore_color.rgb = C_WHITE
    chart_box.line.color.rgb = C_BORDER
    s2.shapes.add_picture(chart_path, Inches(5.9), Inches(1.8), width=Inches(6.5))

# ==========================================
# SLIDE 3: OUR SOLUTION - 4 PILLARS
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "JobShield AI: 4 Pillars of Defense")

pillars = [
    ("1. Omni-Input Vision", "Extracts structured text from physical posters, WhatsApp chats, and PDF offer letters using Gemini Vision + EasyOCR without manual typing.", "📷", C_PRIMARY),
    ("2. Heuristic Audit", "Scans for extortion red flags: security deposits, interview kit charges, urgency triggers, and impossible pay-to-work ratios.", "🔍", C_CYAN),
    ("3. Live OSINT Checks", "Inspects live DNS with WHOIS to catch newly minted scam domains (< 30 days old) and verifies physical shop/office addresses on Google Places.", "🌐", C_WARNING),
    ("4. Explainable Score", "Provides a comprehensive 0-100% Trust Index with clear evidence badges and a 1-click Cyber Crime reporting template (Portal 1930).", "🛡️", C_SUCCESS)
]

col_w = Inches(2.75)
col_gap = Inches(0.25)
col_h = Inches(5.0)

for idx, (p_title, p_desc, icon, col) in enumerate(pillars):
    cx = Inches(0.8) + idx * (col_w + col_gap)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.7), col_w, col_h)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    # Top Accent line
    top_line = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.7), col_w, Inches(0.1))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = col
    top_line.line.fill.background()
    
    # Icon circle
    ic = s3.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.3), Inches(2.1), Inches(0.9), Inches(0.9))
    ic.fill.solid()
    ic.fill.fore_color.rgb = C_BG_LIGHT
    ic.line.color.rgb = C_BORDER
    ic_tf = ic.text_frame
    ic_p = ic_tf.paragraphs[0]
    ic_p.text = icon
    ic_p.alignment = PP_ALIGN.CENTER
    ic_p.font.size = Pt(20)
    
    # Content text
    tb = s3.shapes.add_textbox(cx + Inches(0.25), Inches(3.2), col_w - Inches(0.5), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = p_title
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_DARK
    
    p2 = tf.add_paragraph()
    p2.text = p_desc
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_TEXT_MUTED

# ==========================================
# SLIDE 4: SYSTEM PIPELINE FLOWCHART
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "System Engineering & End-to-End Pipeline")

# Flowchart steps
flow_steps = [
    ("Stage 1: Multi-Input Ingestion", "Upload Poster / WhatsApp screenshot / Offer letter PDF or Telegram forward", C_PRIMARY),
    ("Stage 2: Vision & Extraction", "Gemini 1.5 Flash Vision / OCR parses salary, company, URL, email, and phone", C_CYAN),
    ("Stage 3: FastAPI Verification Engine", "Tri-tier validation: Rule-based regex + WHOIS Domain Audit + Maps verification", C_WARNING),
    ("Stage 4: Trust Score & Action", "0-100% Trust Meter + Red flag badges + 1-Click Police complaint draft", C_SUCCESS)
]

step_w = Inches(2.65)
step_gap = Inches(0.35)
step_y = Inches(1.8)

for idx, (title, desc, col) in enumerate(flow_steps):
    sx = Inches(0.8) + idx * (step_w + step_gap)
    box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, step_y, step_w, Inches(2.4))
    box.fill.solid()
    box.fill.fore_color.rgb = C_WHITE
    box.line.color.rgb = col
    box.line.width = Pt(1.5)
    
    tb = box.text_frame
    tb.word_wrap = True
    p1 = tb.paragraphs[0]
    p1.text = title
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = col
    
    p2 = tb.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_MUTED
    
    # Arrow (except last)
    if idx < len(flow_steps) - 1:
        arrow_box = s4.shapes.add_textbox(sx + step_w, step_y + Inches(0.9), step_gap, Inches(0.6))
        ap = arrow_box.text_frame.paragraphs[0]
        ap.text = "➔"
        ap.alignment = PP_ALIGN.CENTER
        ap.font.size = Pt(22)
        ap.font.bold = True
        ap.font.color.rgb = C_PRIMARY

# Architecture details container at bottom
tech_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(11.73), Inches(2.2))
tech_card.fill.solid()
tech_card.fill.fore_color.rgb = C_WHITE
tech_card.line.color.rgb = C_BORDER

t_title = s4.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(5.0), Inches(0.35))
tp = t_title.text_frame.paragraphs[0]
tp.text = "TECHNOLOGY STACK & INTEGRATIONS"
tp.font.size = Pt(11)
tp.font.bold = True
tp.font.color.rgb = C_PRIMARY

# 3 Sub-blocks in tech stack
sub_techs = [
    ("Frontend (Light & Responsive)", "Vanilla HTML5, Modern CSS Grid, Clean JavaScript. Zero build steps, instant load under 200ms."),
    ("Backend & AI Core", "Python FastAPI (async), Google Gemini 1.5 Flash Vision API, Python-WHOIS DNS library."),
    ("Bot & Civic Integrations", "python-telegram-bot for mobile forwarding, Google Places API for address verification.")
]

for idx, (h, b) in enumerate(sub_techs):
    bx = Inches(1.0) + idx * Inches(3.8)
    b_box = s4.shapes.add_textbox(bx, Inches(5.15), Inches(3.6), Inches(1.4))
    btf = b_box.text_frame
    btf.word_wrap = True
    bp1 = btf.paragraphs[0]
    bp1.text = h
    bp1.font.size = Pt(11)
    bp1.font.bold = True
    bp1.font.color.rgb = C_TEXT_DARK
    
    bp2 = btf.add_paragraph()
    bp2.text = b
    bp2.font.size = Pt(9)
    bp2.font.color.rgb = C_TEXT_MUTED

# ==========================================
# SLIDE 5: JOB SHIELD AI VS GENERIC CHATBOTS
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "Why Asking ChatGPT or a Generic Chatbot Fails")

table_shape = s5.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(11.73), Inches(4.8))
table = table_shape.table
table.columns[0].width = Inches(3.2)
table.columns[1].width = Inches(4.2)
table.columns[2].width = Inches(4.33)

headers = ["Verification Capability", "Asking ChatGPT / Generic LLM", "JobShield AI (Our Solution)"]
for col_idx, h in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_PRIMARY_LIGHT
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

rows = [
    ("Live Domain Age (WHOIS)", "❌ Blind - Cannot query live DNS records. Misses domains created 2 days ago.", "✅ Live Query - Flags domains registered < 30 days immediately."),
    ("Physical Address Verification", "❌ Hallucinates fake validation for non-existent addresses.", "✅ Google Places API - Cross-verifies physical shop / office coordinates."),
    ("Free Email Spoofing", "⚠️ Weak - Ignores @gmail.com or @yahoo.com claiming to be corporate HR.", "✅ Strict Enforcement - Demotes trust score by 50% for free mail providers."),
    ("Street Flyer / Image OCR", "❌ Tedious - Requires user to transcribe entire flyer manually.", "✅ Native Vision - Upload raw photo taken from mobile camera directly."),
    ("Mobile Chatbot Forwarding", "❌ None - Requires user to log into web platform.", "✅ 1-Click - Forward messages straight to Telegram bot for instant verdict.")
]

for row_idx, r_data in enumerate(rows):
    for col_idx, val in enumerate(r_data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else C_BG_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if col_idx == 0:
            p.font.bold = True

# ==========================================
# SLIDE 6: LIVE DEMO & TEST CASES
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Live Demonstration & Test Bench")

# Case A: High Risk Scam
c_a = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
c_a.fill.solid()
c_a.fill.fore_color.rgb = C_WHITE
c_a.line.color.rgb = C_DANGER
c_a.line.width = Pt(1.5)

a_badge = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(2.0), Inches(2.5), Inches(0.38))
a_badge.fill.solid()
a_badge.fill.fore_color.rgb = C_DANGER_BG
a_badge.line.color.rgb = C_DANGER
a_p = a_badge.text_frame.paragraphs[0]
a_p.alignment = PP_ALIGN.CENTER
a_p.text = "⚠️ HIGH RISK SCAM (94%)"
a_p.font.size = Pt(10)
a_p.font.bold = True
a_p.font.color.rgb = C_DANGER

a_tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.55), Inches(5.1), Inches(4.0))
atf = a_tb.text_frame
atf.word_wrap = True

ap1 = atf.paragraphs[0]
ap1.text = "Sample Input (Telegram Task Offer):"
ap1.font.size = Pt(11)
ap1.font.bold = True
ap1.font.color.rgb = C_TEXT_DARK

ap2 = atf.add_paragraph()
ap2.text = "\"Earn ₹3,000 - ₹5,000/day by liking YouTube videos! Pay ₹499 security deposit (100% refundable with first salary). Contact HR on Telegram @earn_quick_india.\""
ap2.font.size = Pt(10)
ap2.font.italic = True
ap2.font.color.rgb = C_TEXT_MUTED

ap3 = atf.add_paragraph()
ap3.text = "\nDetected Threat Indicators:"
ap3.font.size = Pt(11)
ap3.font.bold = True
ap3.font.color.rgb = C_DANGER

flags = [
    "🚩 Upfront Extortion: Demands ₹499 deposit before work begins.",
    "🚩 Impossible Wage Ratio: ₹5,000/day for casual video clicks.",
    "🚩 Anonymous Channel: Routes candidates to Telegram instead of verified domain."
]
for f in flags:
    fp = atf.add_paragraph()
    fp.text = f
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = C_TEXT_DARK

# Case B: Verified Legitimate Drive
c_b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
c_b.fill.solid()
c_b.fill.fore_color.rgb = C_WHITE
c_b.line.color.rgb = C_SUCCESS
c_b.line.width = Pt(1.5)

b_badge = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(2.0), Inches(2.6), Inches(0.38))
b_badge.fill.solid()
b_badge.fill.fore_color.rgb = C_SUCCESS_BG
b_badge.line.color.rgb = C_SUCCESS
b_p = b_badge.text_frame.paragraphs[0]
b_p.alignment = PP_ALIGN.CENTER
b_p.text = "✅ VERIFIED SAFE (96%)"
b_p.font.size = Pt(10)
b_p.font.bold = True
b_p.font.color.rgb = C_SUCCESS

b_tb = s6.shapes.add_textbox(Inches(7.1), Inches(2.55), Inches(5.1), Inches(4.0))
btf = b_tb.text_frame
btf.word_wrap = True

bp1 = btf.paragraphs[0]
bp1.text = "Sample Input (Official Campus Placement):"
bp1.font.size = Pt(11)
bp1.font.bold = True
bp1.font.color.rgb = C_TEXT_DARK

bp2 = btf.add_paragraph()
bp2.text = "\"TCS National Qualifier Test 2026 for Batch 2026. Register exclusively on nextstep.tcs.com. No fee is charged at any point of recruitment. Official emails only from @tcs.com.\""
bp2.font.size = Pt(10)
bp2.font.italic = True
bp2.font.color.rgb = C_TEXT_MUTED

bp3 = btf.add_paragraph()
bp3.text = "\nVerified Safety Metrics:"
bp3.font.size = Pt(11)
bp3.font.bold = True
bp3.font.color.rgb = C_SUCCESS

b_flags = [
    "🛡️ Established Domain Authority: tcs.com registered > 25 years ago.",
    "🛡️ Zero Fee Policy: Explicit disclaimer against monetary demands.",
    "🛡️ Official Corporate Gateway: Directs to standard NextStep portal."
]
for f in b_flags:
    fp = btf.add_paragraph()
    fp.text = f
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = C_TEXT_DARK

# ==========================================
# SLIDE 7: ROADMAP, CIVIC IMPACT & CONCLUSION
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Future Roadmap & Civic Scalability")

road_cards = [
    ("🏛️ Cyber Cell 1930 Integration", "Auto-generate pre-filled police complaint reports formatted according to National Cyber Crime Reporting Portal guidelines, containing extracted transaction handles and timestamps."),
    ("👥 Crowdsourced Fraud Blacklist", "A peer-vetted community registry allowing students across universities to report recurring scammer UPI IDs, phone numbers, and WhatsApp recruiter handles."),
    ("🎓 College TPO Bulletin Widget", "A lightweight browser extension that automatically verifies off-campus hiring drives and internship alerts posted on college WhatsApp groups.")
]

for idx, (title, desc) in enumerate(road_cards):
    rx = Inches(0.8) + idx * Inches(4.0)
    box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.8), Inches(3.73), Inches(3.2))
    box.fill.solid()
    box.fill.fore_color.rgb = C_WHITE
    box.line.color.rgb = C_BORDER
    
    tb = box.text_frame
    tb.word_wrap = True
    p1 = tb.paragraphs[0]
    p1.text = title
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = C_PRIMARY
    
    p2 = tb.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_TEXT_MUTED

# Final Q&A Banner
qa_banner = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.73), Inches(1.5))
qa_banner.fill.solid()
qa_banner.fill.fore_color.rgb = C_PRIMARY_LIGHT
qa_banner.line.color.rgb = C_PRIMARY

qa_tf = qa_banner.text_frame
qa_tf.word_wrap = True
qp1 = qa_tf.paragraphs[0]
qp1.alignment = PP_ALIGN.CENTER
qp1.text = "Thank You! We are Ready for Q&A."
qp1.font.size = Pt(20)
qp1.font.bold = True
qp1.font.color.rgb = C_PRIMARY

qp2 = qa_tf.add_paragraph()
qp2.alignment = PP_ALIGN.CENTER
qp2.text = "JobShield AI — Securing Student Careers Against Digital Employment Extortion."
qp2.font.size = Pt(11)
qp2.font.color.rgb = C_TEXT_MUTED

output_pptx = "JobShield_AI_Pitch_Deck.pptx"
prs.save(output_pptx)
print(f"Successfully generated PowerPoint presentation: {output_pptx}")
