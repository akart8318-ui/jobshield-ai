import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.environ['MPLCONFIGDIR'] = os.path.join(os.getcwd(), 'assets', 'mpl_cache')
os.makedirs("assets", exist_ok=True)
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

# 1. GENERATE STATISTICAL CHARTS (OFF-WHITE THEME COMPATIBLE)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=250)
fig.patch.set_facecolor('#FFFFFF')

years = ['2021', '2022', '2023', '2024', '2025 (Proj)']
cases = [18, 34, 78, 165, 290]
ax1.set_facecolor('#FFFFFF')
ax1.plot(years, cases, marker='o', color='#4F46E5', linewidth=3.5, markersize=8, markerfacecolor='#FFFFFF', markeredgewidth=2.5, markeredgecolor='#4F46E5')
ax1.fill_between(years, cases, color='#4F46E5', alpha=0.10)
ax1.set_title('Reported Job Scam Cases in India', fontsize=12, fontweight='bold', color='#1E293B', pad=12)
ax1.set_ylabel('Annual Cases (Thousands)', fontsize=10, color='#64748B')
ax1.grid(True, linestyle='--', alpha=0.6, color='#E2E8F0')
for i, txt in enumerate(cases):
    ax1.annotate(f"{txt}K", (years[i], cases[i] + 12), ha='center', fontsize=10, fontweight='bold', color='#4F46E5')
ax1.set_ylim(0, 340)
ax1.tick_params(colors='#64748B')
for spine in ax1.spines.values():
    spine.set_color('#E2E8F0')

categories = ['Telegram / Tasks\n(42%)', 'Registration Fee\n(31%)', 'Data Entry Trap\n(18%)', 'Identity Theft\n(9%)']
sizes = [42, 31, 18, 9]
colors = ['#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6']
wedges, texts = ax2.pie(
    sizes, labels=categories, startangle=140,
    colors=colors, pctdistance=0.75,
    textprops=dict(color='#1E293B', fontsize=9.5, fontweight='600'),
    wedgeprops=dict(width=0.45, edgecolor='#FFFFFF', linewidth=2.5)
)
ax2.set_title('Scam Modality Distribution', fontsize=12, fontweight='bold', color='#1E293B', pad=12)

plt.tight_layout()
chart_path = os.path.join("assets", "problem_charts.png")
plt.savefig(chart_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved charts to", chart_path)

# 2. GENERATE 4 FILLED PILLAR ICONS / GRAPHICS (Slide 3 & 4)
pillar_configs = [
    ("icon_vision.png", "#4F46E5", "01", "SCAN & OCR", "Extracts Text from Posters & PDFs"),
    ("icon_audit.png", "#0EA5E9", "02", "HEURISTICS", "Detects Deposit & Fee Extortion"),
    ("icon_osint.png", "#D97706", "03", "LIVE OSINT", "Checks DNS Age & Google Maps"),
    ("icon_trust.png", "#059669", "04", "TRUST SCORE", "Generates 0-100% Risk Report")
]

for filename, color_hex, num, label, desc in pillar_configs:
    img = Image.new("RGBA", (320, 320), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle
    draw.ellipse([10, 10, 310, 310], fill="#FFFFFF", outline=color_hex, width=6)
    # Inner filled circle
    draw.ellipse([26, 26, 294, 294], fill=color_hex)
    
    # Number badge
    # Draw simple sharp text or shapes
    draw.ellipse([100, 50, 220, 170], fill="#FFFFFF")
    
    # We can write text with default font or bitmap
    draw.text((140, 85), num, fill=color_hex)
    draw.text((75, 195), label, fill="#FFFFFF")
    draw.text((50, 230), desc, fill="#E2E8F0")
    
    out_p = os.path.join("assets", filename)
    img.save(out_p)

# 3. GENERATE A FRIENDLY CHAT SCAM MOCKUP IMAGE
scam_img = Image.new("RGB", (600, 380), "#F1F5F9")
s_draw = ImageDraw.Draw(scam_img)

# Message Bubble
s_draw.rounded_rectangle([30, 30, 570, 280], radius=16, fill="#FFFFFF", outline="#CBD5E1", width=2)
# Sender header
s_draw.text((50, 50), "HR Priya - Global Career Hub (Telegram)", fill="#4F46E5")
s_draw.text((50, 75), "Online • Unverified Sender", fill="#94A3B8")
s_draw.line([50, 100, 550, 100], fill="#E2E8F0", width=1)

# Message Content
msg_lines = [
    "URGENT: Part-Time Job Opportunity for College Students!",
    "Earn Rs. 2,500 - 5,000 per day by rating videos.",
    "No interview needed. Immediate Joining.",
    "Requirement: Pay Rs. 499 security deposit (100% Refundable).",
    "Pay to UPI: quickwork@upi to claim your spot!"
]
y_text = 120
for line in msg_lines:
    s_draw.text((50, y_text), line, fill="#1E293B")
    y_text += 26

# Warning Overlay Stamp
s_draw.rounded_rectangle([120, 295, 480, 355], radius=12, fill="#E11D48")
s_draw.text((150, 312), "FLAGGED: 94% FRAUD THREAT", fill="#FFFFFF")

scam_mockup_path = os.path.join("assets", "scam_mockup.png")
scam_img.save(scam_mockup_path)
print("Saved scam mockup to", scam_mockup_path)

# 4. GENERATE A FRIENDLY VERIFIED MOCKUP IMAGE
legit_img = Image.new("RGB", (600, 380), "#F0FDF4")
l_draw = ImageDraw.Draw(legit_img)

# Message Bubble
l_draw.rounded_rectangle([30, 30, 570, 280], radius=16, fill="#FFFFFF", outline="#A7F3D0", width=2)
l_draw.text((50, 50), "TCS Campus Placement Office (Verified Gateway)", fill="#059669")
l_draw.text((50, 75), "Official Domain: tcs.com • NextStep Portal", fill="#65A30D")
l_draw.line([50, 100, 550, 100], fill="#E2E8F0", width=1)

l_lines = [
    "Invitation for Batch 2026 Engineering Students.",
    "Role: Assistant System Engineer (Ninja & Digital).",
    "Official Registration: https://nextstep.tcs.com",
    "NOTE: TCS does NOT ask for any monetary deposit or fee.",
    "Any such request is strictly fraudulent."
]
y_text = 120
for line in l_lines:
    l_draw.text((50, y_text), line, fill="#1E293B")
    y_text += 26

# Success Overlay Stamp
l_draw.rounded_rectangle([130, 295, 470, 355], radius=12, fill="#059669")
l_draw.text((160, 312), "VERIFIED: 96% AUTHENTIC", fill="#FFFFFF")

legit_mockup_path = os.path.join("assets", "legit_mockup.png")
legit_img.save(legit_mockup_path)
print("Saved legit mockup to", legit_mockup_path)

print("All visual assets successfully generated!")
