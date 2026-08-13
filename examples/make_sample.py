#!/usr/bin/env python3
"""
Generate a fictional care schedule photo for demos and testing.

Everything in the output is invented: the agency, the staff names, the child.
No real person's data is used. Run:  python3 make_sample.py
"""
import calendar
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(20260901)

W, H = 1500, 1950
PAPER = (250, 247, 238)
PRINT = (40, 42, 48)
INK = (28, 48, 120)       # ballpoint blue
INK2 = (120, 30, 40)      # red pen
GRID = (150, 152, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
HAND = "/usr/share/texmf/fonts/opentype/public/lm/lmroman10-italic.otf"

try:
    ImageFont.truetype(HAND, 20)
except OSError:
    HAND = SANS


def f(path, size):
    return ImageFont.truetype(path, size)


def handwrite(img, xy, text, size=26, color=INK, jitter=1.6, slant=True):
    """Draw text with per-character jitter so it reads as handwriting."""
    font = f(HAND if slant else SANS, size)
    x, y = xy
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for ch in text:
        dx = random.uniform(-jitter, jitter)
        dy = random.uniform(-jitter, jitter)
        d.text((x + dx, y + dy), ch, font=font, fill=color + (255,))
        x += d.textlength(ch, font=font) * random.uniform(0.94, 1.02)
    layer = layer.rotate(random.uniform(-0.5, 0.5), resample=Image.BICUBIC, center=xy)
    img.alpha_composite(layer)
    return x


def ellipse_mark(d, box, color=INK2, width=3):
    """A hand-drawn-looking circle around something."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    for i in range(0, 400):
        a = math.radians(i)
        wob = 1 + 0.035 * math.sin(a * 3 + 1.2)
        pts.append((cx + rx * wob * math.cos(a), cy + ry * wob * math.sin(a)))
    d.line(pts + [pts[0]], fill=color, width=width, joint="curve")


def sticky(img, xy, wh, fill, lines, size=22):
    x, y = xy
    w, h = wh
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([x + 4, y + 5, x + w + 4, y + h + 5], fill=(0, 0, 0, 45))
    d.rectangle([x, y, x + w, y + h], fill=fill + (255,))
    img.alpha_composite(layer)
    ty = y + 10
    for ln in lines:
        handwrite(img, (x + 12, ty), ln, size=size, color=(35, 35, 45), jitter=1.2)
        ty += size + 6


img = Image.new("RGBA", (W, H), PAPER + (255,))
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- header
d.text((70, 60), "BRIGHTPATH HOME NURSING", font=f(SERIF, 40), fill=PRINT)
d.text((70, 112), "Monthly Visit Schedule", font=f(SANS, 26), fill=PRINT)
d.text((70, 150), "September 2026", font=f(SERIF, 34), fill=PRINT)
d.line([70, 200, W - 70, 200], fill=PRINT, width=2)

nf = f(SANS, 22)
d.text((70, 218), "Please review next month's plan and return your requests",
       font=nf, fill=PRINT)
lead, due = "for October by ", "Sep 20 (Fri), 5:00 PM."
d.text((70, 250), lead + due, font=nf, fill=PRINT)
d.text((70, 288), "Return by fax or hand to your visiting nurse.",
       font=f(SANS, 20), fill=PRINT)

# circle the deadline itself, measured so it lands on the right words
dx0 = 70 + d.textlength(lead, font=nf)
dx1 = dx0 + d.textlength(due, font=nf)
ellipse_mark(d, (dx0 - 14, 242, dx1 + 14, 282))

# ---------------------------------------------------------- transport note
sticky(img, (1010, 52), (420, 250), (255, 236, 140), [
    "TRANSPORT  (top=out, bot=back)",
    "  7    8    9   10   11",
    "self  bus  bus  self  bus",
    " H    bus  bus   H    bus",
    "",
    "  14  15   16   17   18",
    "bus  self  bus  bus  RC",
])

# ------------------------------------------------------------------ grid
cal = calendar.Calendar(firstweekday=6)  # Sunday first
weeks = cal.monthdayscalendar(2026, 9)
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

GX, GY = 70, 360
CW, CH = (W - 140) // 7, 275

for i, nm in enumerate(days):
    d.text((GX + i * CW + 12, GY - 34), nm, font=f(SANS, 24), fill=PRINT)

for r, week in enumerate(weeks):
    for c, day in enumerate(week):
        x0, y0 = GX + c * CW, GY + r * CH
        d.rectangle([x0, y0, x0 + CW, y0 + CH], outline=GRID, width=2)
        if day:
            d.text((x0 + 10, y0 + 8), str(day), font=f(SANS, 26), fill=PRINT)


def cell(day):
    for r, week in enumerate(weeks):
        for c, dd in enumerate(week):
            if dd == day:
                return GX + c * CW, GY + r * CH
    raise ValueError(day)


# ------------------------------------------------------- handwritten entries
routine = {2: "Kim", 4: "Alvarez", 7: "Kim", 9: "Novak", 11: "Alvarez",
           14: "Kim", 16: "Novak", 18: "Alvarez", 21: "Kim", 23: "Novak",
           25: "Alvarez", 28: "Kim", 30: "Novak"}
for day, who in routine.items():
    x, y = cell(day)
    handwrite(img, (x + 14, y + 46), "8:30-9:30", size=25)
    handwrite(img, (x + 14, y + 78), who, size=25)

# PT visits, circled
for day in (3, 17):
    x, y = cell(day)
    handwrite(img, (x + 22, y + 120), "PT", size=28)
    handwrite(img, (x + 70, y + 122), "10:00-11:00", size=22)
    ellipse_mark(d, (x + 12, y + 114, x + 66, y + 156), width=2)

# an all-day entry
x, y = cell(10)
handwrite(img, (x + 14, y + 120), "Dr. Ellery", size=24, color=INK)
handwrite(img, (x + 14, y + 150), "all day", size=24, color=INK)

# requested / not confirmed
x, y = cell(24)
handwrite(img, (x + 14, y + 120), "Rivers (app)", size=24, color=INK)
x, y = cell(26)
handwrite(img, (x + 14, y + 120), "PT cand", size=24, color=INK)

# cancelled entry with strikethrough
x, y = cell(8)
handwrite(img, (x + 14, y + 120), "OT 14:00", size=24, color=INK)
d.line([x + 12, y + 133, x + 175, y + 129], fill=INK, width=3)

# family annotations
for day in (5, 12, 19, 27):
    x, y = cell(day)
    handwrite(img, (x + CW - 70, y + 200), "PM", size=30, color=INK2)

# deliberately hard to read - exercises the "do not guess" rule
x, y = cell(22)
handwrite(img, (x + 14, y + 160), "M~ne c/o 15:3?", size=23, color=INK, jitter=3.4)

# deliberate weekday/date mismatch - exercises the mismatch rule
x, y = cell(29)
handwrite(img, (x + 14, y + 160), "Mon - swap w/ Kim", size=22, color=INK)

# deadline marked inside the grid
x, y = cell(20)
handwrite(img, (x + 12, y + 190), "REQUESTS DUE", size=24, color=INK2)
ellipse_mark(d, (x + 6, y + 182, x + CW - 8, y + 226), width=3)

# ---- sticky note straddling two cells: exercises the ambiguity rule
x, y = cell(15)
sticky(img, (x + CW - 60, y + CH - 120), (200, 110), (180, 235, 200),
       ["Saturday club", "meet 9am", "bring chair"], size=20)

# --------------------------------------------------------------- photo look
img = img.convert("RGB")
img = img.rotate(-0.7, resample=Image.BICUBIC, fillcolor=PAPER, expand=False)

# uneven lighting
grad = Image.new("L", (W, H))
gd = ImageDraw.Draw(grad)
for i in range(H):
    gd.line([(0, i), (W, i)], fill=int(238 + 17 * (i / H)))
grad = grad.filter(ImageFilter.GaussianBlur(160))
img = Image.composite(img, Image.new("RGB", (W, H), (255, 255, 255)), grad)

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save("sample-schedule.png", optimize=True)
print("wrote sample-schedule.png")
