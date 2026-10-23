import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 Widescreen
prs.slide_height = Inches(7.5)

# Color Palette: Warm Off-White Theme
C_OFF_WHITE = RGBColor(246, 247, 249)    # #F6F7F9 Soft off-white background
C_WHITE = RGBColor(255, 255, 255)        # #FFFFFF Card background
C_PRIMARY = RGBColor(79, 70, 229)        # #4F46E5 Royal Indigo
C_PRIMARY_LIGHT = RGBColor(238, 242, 255)# #EEF2FF
C_CYAN = RGBColor(14, 165, 233)          # #0EA5E9
C_CYAN_LIGHT = RGBColor(224, 242, 254)   # #E0F2FE
C_TEXT_DARK = RGBColor(15, 23, 42)       # #0F172A
C_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569
C_BORDER = RGBColor(226, 232, 240)       # #E2E8F0
C_DANGER = RGBColor(225, 29, 72)         # #E11D48
C_DANGER_BG = RGBColor(255, 241, 242)    # #FFF1F2
C_SUCCESS = RGBColor(5, 150, 105)        # #059669
C_SUCCESS_BG = RGBColor(236, 253, 245)   # #ECFDF5
C_WARNING = RGBColor(217, 119, 6)        # #D97706
C_WARNING_BG = RGBColor(254, 243, 199)   # #FEF3C7

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = C_OFF_WHITE
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_text="THEME 1: AI & SMART SOLUTIONS | CODE: AI-04"):
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.35))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_text.upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_PRIMARY
    
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.75))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_DARK

# ==============================================================================
# SLIDE 1: TITLE SLIDE WITH TOPICS AGENDA (NO MEMBER ROLES AS REQUESTED)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Top primary banner
banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
banner.fill.solid()
banner.fill.fore_color.rgb = C_PRIMARY
banner.line.fill.background()

# Title pill
tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.65), Inches(4.2), Inches(0.4))
tag.fill.solid()
tag.fill.fore_color.rgb = C_PRIMARY_LIGHT
tag.line.color.rgb = C_PRIMARY
tf = tag.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "COLLEGE HACKATHON 2026 • THEME 1 (AI-04)"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

# Title & Subtitle
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(1.5))
tf = title_box.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "JobShield AI"
p1.font.size = Pt(44)
p1.font.bold = True
p1.font.color.rgb = C_PRIMARY

p2 = tf.add_paragraph()
p2.text = "Autonomous Multi-Layer Verification Engine for Local Job Scams & Vacancies"
p2.font.size = Pt(18)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_DARK

p3 = tf.add_paragraph()
p3.text = "Presented by Team Parakram (5 Members) • Protecting students and job seekers against fraudulent digital employment"
p3.font.size = Pt(12)
p3.font.color.rgb = C_TEXT_MUTED

# Topics Header
agenda_header = s1.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(8), Inches(0.35))
ah_p = agenda_header.text_frame.paragraphs[0]
ah_p.text = "PRESENTATION ROADMAP & TOPICS COVERED:"
ah_p.font.size = Pt(11)
ah_p.font.bold = True
ah_p.font.color.rgb = C_PRIMARY

# 6 Clean Topic Cards Grid (3 cols x 2 rows)
topics = [
    ("01", "The Epidemic: Campus Job Scams", "Rising student victimization, ₹1,850 Cr+ national loss, and deposit traps."),
    ("02", "Our Solution: 4 Pillars of Defense", "Omni-input vision, heuristic rule audits, live OSINT, and explainable trust index."),
    ("03", "System Pipeline & Flowchart", "Under-the-hood FastAPI architecture, Gemini Vision OCR, and verification layers."),
    ("04", "Beyond Generic Chatbots", "Why asking ChatGPT fails: Live WHOIS DNS checks and Google Places geo-auditing."),
    ("05", "Live Test Bench & Demonstrations", "Side-by-side comparison: 94% threat Telegram task vs. 96% authentic campus hiring."),
    ("06", "Civic Scalability & Roadmap", "Integration with National Cyber Crime Portal 1930 and college TPO portals.")
]

t_w = Inches(3.75)
t_h = Inches(1.6)
for idx, (num, t_title, t_desc) in enumerate(topics):
    col = idx % 3
    row = idx // 3
    tx = Inches(0.8) + col * (t_w + Inches(0.24))
    ty = Inches(3.35) + row * (t_h + Inches(0.25))
    
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, ty, t_w, t_h)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    card.line.width = Pt(1)
    
    # Left pill number badge
    nb = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx + Inches(0.18), ty + Inches(0.2), Inches(0.55), Inches(0.4))
    nb.fill.solid()
    nb.fill.fore_color.rgb = C_PRIMARY_LIGHT
    nb.line.color.rgb = C_PRIMARY
    np = nb.text_frame.paragraphs[0]
    np.alignment = PP_ALIGN.CENTER
    np.text = num
    np.font.size = Pt(11)
    np.font.bold = True
    np.font.color.rgb = C_PRIMARY
    
    tb = s1.shapes.add_textbox(tx + Inches(0.85), ty + Inches(0.15), t_w - Inches(0.95), t_h - Inches(0.25))
    ttf = tb.text_frame
    ttf.word_wrap = True
    tp1 = ttf.paragraphs[0]
    tp1.text = t_title
    tp1.font.size = Pt(11)
    tp1.font.bold = True
    tp1.font.color.rgb = C_TEXT_DARK
    
    tp2 = ttf.add_paragraph()
    tp2.text = t_desc
    tp2.font.size = Pt(8.8)
    tp2.font.color.rgb = C_TEXT_MUTED

# ==============================================================================
# SLIDE 2: THE PROBLEM WITH DUAL GRAPHS & STATS
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "The Epidemic: Job & Task Scams on Campus")

left_w = Inches(4.8)
pain_cards = [
    ("Upfront Deposit Extortion", "Students coerced into paying ₹500 - ₹5,000 for 'registration', 'laptop dispatch', or 'interview kits'. Money vanishes immediately.", C_DANGER),
    ("Telegram / WhatsApp Task Scams", "'Earn ₹3,000/day for liking YouTube videos'. Uses micro-payouts to build false trust before freezing lakhs in fraudulent portal accounts.", C_WARNING),
    ("The Local Vacancy Blindspot", "Street flyers on coaching walls and unverified local walk-ins lack registered corporate footprints, leaving victims with zero recourse.", C_PRIMARY)
]

py = Inches(1.6)
for title, desc, col in pain_cards:
    p_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), py, left_w, Inches(1.6))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = C_WHITE
    p_box.line.color.rgb = C_BORDER
    
    ibar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), py, Inches(0.12), Inches(1.6))
    ibar.fill.solid()
    ibar.fill.fore_color.rgb = col
    ibar.line.fill.background()
    
    tb = s2.shapes.add_textbox(Inches(1.05), py + Inches(0.15), left_w - Inches(0.35), Inches(1.3))
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
    
    py += Inches(1.75)

# Insert Generated Charts Image on the right
chart_img_path = os.path.join("assets", "problem_charts.png")
if os.path.exists(chart_img_path):
    c_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(1.6), Inches(6.7), Inches(5.2))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = C_WHITE
    c_card.line.color.rgb = C_BORDER
    s2.shapes.add_picture(chart_img_path, Inches(5.9), Inches(1.7), width=Inches(6.5))

# ==============================================================================
# SLIDE 3: OUR SOLUTION - 4 PILLARS OF DEFENSE
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "JobShield AI: 4 Pillars of Defense")

pillars = [
    ("01", "Omni-Input Vision", "Extracts structured text from physical posters, WhatsApp chats, and PDF offer letters using Gemini Vision + EasyOCR without manual typing.", C_PRIMARY, C_PRIMARY_LIGHT),
    ("02", "Heuristic Audit", "Scans for extortion red flags: security deposits, interview kit charges, urgency triggers, and impossible pay-to-work ratios.", C_CYAN, C_CYAN_LIGHT),
    ("03", "Live OSINT Checks", "Inspects live DNS with WHOIS to catch newly minted scam domains (< 30 days old) and verifies physical shop/office addresses on Google Places.", C_WARNING, C_WARNING_BG),
    ("04", "Trust Score & Report", "Provides a comprehensive 0-100% Trust Index with clear evidence badges and a 1-click Cyber Crime reporting template (Portal 1930).", C_SUCCESS, C_SUCCESS_BG)
]

col_w = Inches(2.75)
col_gap = Inches(0.24)
col_h = Inches(5.1)

for idx, (num, p_title, p_desc, col_accent, col_bg) in enumerate(pillars):
    cx = Inches(0.8) + idx * (col_w + col_gap)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.6), col_w, col_h)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    # Top color strip
    top_bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.6), col_w, Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = col_accent
    top_bar.line.fill.background()
    
    # FILLED CIRCLE BADGE (Ensuring high contrast & no blank circle!)
    badge = s3.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.75), Inches(2.0), Inches(1.25), Inches(1.25))
    badge.fill.solid()
    badge.fill.fore_color.rgb = col_accent
    badge.line.color.rgb = col_accent
    btf = badge.text_frame
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = num
    bp.font.size = Pt(22)
    bp.font.bold = True
    bp.font.color.rgb = C_WHITE
    
    # Card text
    tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(3.45), col_w - Inches(0.4), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = p_title
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_DARK
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = p_desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_TEXT_MUTED

# ==============================================================================
# SLIDE 4: SYSTEM PIPELINE FLOWCHART (PROPERLY FILLED CIRCLES!)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "System Engineering & End-to-End Pipeline")

# 4 Pipeline Stages with FILLED CIRCLES
flow_steps = [
    ("01", "INGESTION", "User Upload", "WhatsApp Screenshot\nStreet Poster Photo\nPDF Offer Letter", C_PRIMARY),
    ("02", "VISION & OCR", "Gemini 1.5 API", "Multimodal Extraction\nCompany & VPA Handles\nSalary & Contact Info", C_CYAN),
    ("03", "FASTAPI ENGINE", "Tri-Tier Audit", "Heuristic Rule Regex\nWHOIS Domain Age\nGoogle Places Maps", C_WARNING),
    ("04", "TRUST REPORT", "Output Delivery", "0-100% Trust Meter\nRed Flag Breakdown\n1930 Complaint Draft", C_SUCCESS)
]

step_w = Inches(2.65)
step_gap = Inches(0.35)
step_y = Inches(1.6)

for idx, (step_num, step_name, step_sub, step_details, col_accent) in enumerate(flow_steps):
    sx = Inches(0.8) + idx * (step_w + step_gap)
    box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, step_y, step_w, Inches(2.8))
    box.fill.solid()
    box.fill.fore_color.rgb = C_WHITE
    box.line.color.rgb = C_BORDER
    box.line.width = Pt(1.5)
    
    # 100% FILLED CIRCLE AT TOP OF CARD WITH STEP NUMBER!
    c_badge = s4.shapes.add_shape(MSO_SHAPE.OVAL, sx + Inches(0.85), step_y + Inches(0.2), Inches(0.95), Inches(0.95))
    c_badge.fill.solid()
    c_badge.fill.fore_color.rgb = col_accent
    c_badge.line.color.rgb = col_accent
    c_tf = c_badge.text_frame
    c_p = c_tf.paragraphs[0]
    c_p.alignment = PP_ALIGN.CENTER
    c_p.text = step_num
    c_p.font.size = Pt(16)
    c_p.font.bold = True
    c_p.font.color.rgb = C_WHITE
    
    # Text below filled circle
    tb = s4.shapes.add_textbox(sx + Inches(0.15), step_y + Inches(1.2), step_w - Inches(0.3), Inches(1.5))
    tbf = tb.text_frame
    tbf.word_wrap = True
    
    tp1 = tbf.paragraphs[0]
    tp1.alignment = PP_ALIGN.CENTER
    tp1.text = step_name
    tp1.font.size = Pt(11)
    tp1.font.bold = True
    tp1.font.color.rgb = col_accent
    
    tp2 = tbf.add_paragraph()
    tp2.alignment = PP_ALIGN.CENTER
    tp2.text = step_sub
    tp2.font.size = Pt(9.5)
    tp2.font.bold = True
    tp2.font.color.rgb = C_TEXT_DARK
    
    tp3 = tbf.add_paragraph()
    tp3.alignment = PP_ALIGN.CENTER
    tp3.text = step_details
    tp3.font.size = Pt(8.5)
    tp3.font.color.rgb = C_TEXT_MUTED
    
    # Directional arrow between stages
    if idx < len(flow_steps) - 1:
        arr = s4.shapes.add_textbox(sx + step_w, step_y + Inches(1.0), step_gap, Inches(0.6))
        ap = arr.text_frame.paragraphs[0]
        ap.alignment = PP_ALIGN.CENTER
        ap.text = "➔"
        ap.font.size = Pt(22)
        ap.font.bold = True
        ap.font.color.rgb = C_PRIMARY

# Bottom Technology Stack Container
tech_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.73), Inches(2.1))
tech_card.fill.solid()
tech_card.fill.fore_color.rgb = C_WHITE
tech_card.line.color.rgb = C_BORDER

t_head = s4.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(6.0), Inches(0.35))
tp = t_head.text_frame.paragraphs[0]
tp.text = "CORE ARCHITECTURAL STACK & COMPONENT INTEGRATION:"
tp.font.size = Pt(11)
tp.font.bold = True
tp.font.color.rgb = C_PRIMARY

sub_stacks = [
    ("Frontend (Lightweight & Instant)", "Vanilla HTML5 / Modern CSS Grid / ES6 JS. Zero build compilation, loaded in <200ms on any mobile or desktop browser."),
    ("Backend & Intelligence Engine", "Python FastAPI (Asynchronous), Google Gemini 1.5 Flash Vision for OCR, and Python-WHOIS DNS inspection library."),
    ("Outreach & Civic Integration", "python-telegram-bot for instant message forwarding, plus pre-formatted reporting templates for National Cyber Portal 1930.")
]

for idx, (h, b) in enumerate(sub_stacks):
    bx = Inches(1.0) + idx * Inches(3.85)
    b_box = s4.shapes.add_textbox(bx, Inches(5.2), Inches(3.6), Inches(1.4))
    btf = b_box.text_frame
    btf.word_wrap = True
    bp1 = btf.paragraphs[0]
    bp1.text = h
    bp1.font.size = Pt(10.5)
    bp1.font.bold = True
    bp1.font.color.rgb = C_TEXT_DARK
    
    bp2 = btf.add_paragraph()
    bp2.text = b
    bp2.font.size = Pt(8.8)
    bp2.font.color.rgb = C_TEXT_MUTED

# ==============================================================================
# SLIDE 5: JOB SHIELD AI VS GENERIC CHATBOTS
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "Why Asking ChatGPT or a Generic Chatbot Fails")

table_shape = s5.shapes.add_table(6, 3, Inches(0.8), Inches(1.7), Inches(11.73), Inches(4.9))
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
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

rows = [
    ("Live Domain Age (WHOIS)", "❌ Blind - Cannot query live DNS records. Completely misses domains registered 2 days ago.", "✅ Live Query - Flags domains registered < 30 days instantly with 50% trust penalty."),
    ("Physical Address Verification", "❌ Hallucinates fake validation for non-existent shops and coaching centers.", "✅ Google Places API - Cross-verifies physical shop / office coordinates on map."),
    ("Free Email Spoofing", "⚠️ Weak - Overlooks @gmail.com or @yahoo.com claiming to be corporate HR.", "✅ Strict Enforcement - Demotes trust score by 50% for free mail providers."),
    ("Street Flyer / Image OCR", "❌ Tedious - Requires user to transcribe entire flyer manually into prompt.", "✅ Native Vision - Upload raw camera photo of posters without manual typing."),
    ("Mobile Chatbot Forwarding", "❌ None - Requires user to log into website interface.", "✅ 1-Click - Forward messages straight to Telegram bot for instant verdict.")
]

for row_idx, r_data in enumerate(rows):
    for col_idx, val in enumerate(r_data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else C_OFF_WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9.8)
        p.font.color.rgb = C_TEXT_DARK
        if col_idx == 0:
            p.font.bold = True

# ==============================================================================
# SLIDE 6: LIVE TEST CASES WITH FRIENDLY IMAGES
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Live Demonstration & Test Bench (Real-World Audits)")

# Case A: Scam Mockup Image + Details
c_a = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
c_a.fill.solid()
c_a.fill.fore_color.rgb = C_WHITE
c_a.line.color.rgb = C_DANGER
c_a.line.width = Pt(1.5)

scam_img_path = os.path.join("assets", "scam_mockup.png")
if os.path.exists(scam_img_path):
    s6.shapes.add_picture(scam_img_path, Inches(1.0), Inches(1.8), width=Inches(5.3))

a_tb = s6.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.3), Inches(2.2))
atf = a_tb.text_frame
atf.word_wrap = True
ap1 = atf.paragraphs[0]
ap1.text = "JobShield AI Detected Threat Indicators:"
ap1.font.size = Pt(11)
ap1.font.bold = True
ap1.font.color.rgb = C_DANGER

flags = [
    "🚩 Upfront Extortion: Demands Rs. 499 deposit before work begins.",
    "🚩 Impossible Wage Ratio: Rs. 5,000/day for casual video clicks.",
    "🚩 Anonymous Routing: Directs students to Telegram instead of domain."
]
for f in flags:
    fp = atf.add_paragraph()
    fp.text = f
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = C_TEXT_DARK

# Case B: Legit Mockup Image + Details
c_b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
c_b.fill.solid()
c_b.fill.fore_color.rgb = C_WHITE
c_b.line.color.rgb = C_SUCCESS
c_b.line.width = Pt(1.5)

legit_img_path = os.path.join("assets", "legit_mockup.png")
if os.path.exists(legit_img_path):
    s6.shapes.add_picture(legit_img_path, Inches(7.0), Inches(1.8), width=Inches(5.3))

b_tb = s6.shapes.add_textbox(Inches(7.0), Inches(4.5), Inches(5.3), Inches(2.2))
btf = b_tb.text_frame
btf.word_wrap = True
bp1 = btf.paragraphs[0]
bp1.text = "JobShield AI Verified Safety Metrics:"
bp1.font.size = Pt(11)
bp1.font.bold = True
bp1.font.color.rgb = C_SUCCESS

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

# ==============================================================================
# SLIDE 7: ROADMAP, CIVIC IMPACT & CONCLUSION
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Future Roadmap & Civic Scalability")

road_cards = [
    ("🏛️ Cyber Cell 1930 Sync", "Auto-generate pre-filled police complaint reports formatted according to National Cyber Crime Reporting Portal guidelines, containing extracted transaction handles and timestamps."),
    ("👥 Crowdsourced Fraud Blacklist", "A peer-vetted community registry allowing students across universities to report recurring scammer UPI IDs, phone numbers, and WhatsApp recruiter handles."),
    ("🎓 College TPO Bulletin Widget", "A lightweight browser extension that automatically verifies off-campus hiring drives and internship alerts posted on college WhatsApp groups.")
]

for idx, (title, desc) in enumerate(road_cards):
    rx = Inches(0.8) + idx * Inches(4.0)
    box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.7), Inches(3.73), Inches(3.3))
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

output_pptx = "JobShield_AI_Hackathon_Pitch.pptx"
prs.save(output_pptx)
print(f"Successfully generated updated PowerPoint: {output_pptx}")
