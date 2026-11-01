"""Generate a printable 8.5x11 color-code chart (large text, readable from ~15-20 ft).

Usage:  pip install reportlab && python make_chart.py
Edit ROWS to match the colors and wording you use. Output: alert_chart.pdf
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import HexColor, black, white

TITLE = "LIGHT ALERTS"
OUTPUT = "alert_chart.pdf"

# (big word, what to do, light pattern, fill color, text color)
ROWS = [
    ("EVACUATE",     "LEAVE NOW",                  "FLASHING RED", "#cc2222", white),
    ("STORM",        "STAY INSIDE - TAKE SHELTER", "SOLID PURPLE", "#9966cc", black),
    ("HIGH WIND",    "SECURE OUTDOOR ITEMS",       "SOLID CYAN",   "#00ccee", black),
    ("EXTREME HEAT", "STAY COOL - DRINK WATER",    "SOLID ORANGE", "#ff9933", black),
    ("ALL CLEAR",    "SAFE - NO ALERT",            "SOLID GREEN",  "#33aa55", black),
]

W, H = letter
M, GAP, TITLE_H = 24, 8, 52

def fit(text, font, max_size, max_w):
    size = max_size
    while stringWidth(text, font, size) > max_w:
        size -= 1
    return size

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle(TITLE)
c.setFillColor(black)
ts = fit(TITLE, "Helvetica-Bold", 40, W - 2 * M)
c.setFont("Helvetica-Bold", ts)
c.drawCentredString(W / 2, H - M - ts + 4, TITLE)

top = H - M - TITLE_H
rh = (top - M - GAP * (len(ROWS) - 1)) / len(ROWS)
for i, (kw, meaning, light, fill, fg) in enumerate(ROWS):
    y_top = top - i * (rh + GAP)
    y_bot = y_top - rh
    c.setFillColor(HexColor(fill))
    c.roundRect(M, y_bot, W - 2 * M, rh, 22, stroke=0, fill=1)
    c.setFillColor(fg)
    inner = W - 2 * M - 40
    ls = fit(light, "Helvetica-Bold", 20, inner)
    c.setFont("Helvetica-Bold", ls)
    c.drawCentredString(W / 2, y_top - 10 - ls * 0.8, light)
    ks = fit(kw, "Helvetica-Bold", 72, inner)
    c.setFont("Helvetica-Bold", ks)
    c.drawCentredString(W / 2, y_bot + 46, kw)
    ms = fit(meaning, "Helvetica-Bold", 27, inner)
    c.setFont("Helvetica-Bold", ms)
    c.drawCentredString(W / 2, y_bot + 13, meaning)
c.showPage()
c.save()
print("wrote", OUTPUT)
