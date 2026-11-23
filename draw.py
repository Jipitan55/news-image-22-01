#!/usr/bin/env python3
"""Render entry.png: a one-page infographic summing up world news of
Sunday 22 November 2026. Drawn entirely with PIL shapes and DejaVu text.
Writes entry.png next to this script (1024x1024, under 1 MiB)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
BG = (247, 243, 234)          # paper
INK = (16, 27, 46)            # dark navy
NAVY = (16, 27, 46)
WHITE = (255, 255, 255)
MUTED = (90, 100, 115)
PANEL = (255, 255, 255)
ACCENT = (198, 47, 47)        # red accent


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- pictograms, drawn in a box (x, y, w, h) with a colour --------------
def pic_globe(d, x, y, w, h, c):
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=6)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=c, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=c, width=4)
    d.line([cx - r, cy - r // 2, cx + r, cy - r // 2], fill=c, width=3)
    d.line([cx - r, cy + r // 2, cx + r, cy + r // 2], fill=c, width=3)
    # crack: talks broke down
    d.line([cx + r // 3, cy - r, cx + r // 6, cy - r // 3,
            cx + r // 2, cy, cx + r // 4, cy + r // 2], fill=(198, 47, 47), width=5)


def pic_ship_drone(d, x, y, w, h, c):
    # sea
    d.line([x + 6, y + h - 22, x + w - 6, y + h - 22], fill=c, width=5)
    d.line([x + 16, y + h - 12, x + w - 16, y + h - 12], fill=c, width=4)
    # ship hull
    d.polygon([(x + 10, y + h - 42), (x + w - 26, y + h - 42),
               (x + w - 38, y + h - 24), (x + 22, y + h - 24)], fill=c)
    d.rectangle([x + 34, y + h - 66, x + 52, y + h - 42], fill=c)
    d.line([x + 43, y + h - 82, x + 43, y + h - 66], fill=c, width=4)
    # drone above
    dx, dy = x + w - 44, y + 22
    d.ellipse([dx - 12, dy - 8, dx + 12, dy + 8], outline=c, width=4)
    d.line([dx - 22, dy - 12, dx + 22, dy - 12], fill=c, width=4)
    d.line([dx - 22, dy + 12, dx + 22, dy + 12], fill=c, width=4)
    # explosion star
    ex, ey = x + w - 52, y + h - 62
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([ex, ey, ex + int(16 * math.cos(a)), ey + int(16 * math.sin(a))],
               fill=(198, 47, 47), width=4)


def pic_tanker(d, x, y, w, h, c):
    d.line([x + 6, y + h - 20, x + w - 6, y + h - 20], fill=c, width=5)
    d.rectangle([x + 8, y + h - 46, x + w - 30, y + h - 22], fill=c)
    d.rectangle([x + w - 44, y + h - 66, x + w - 26, y + h - 46], fill=c)
    d.line([x + w - 35, y + h - 80, x + w - 35, y + h - 66], fill=c, width=4)
    # flame
    fx, fy = x + 34, y + h - 62
    d.polygon([(fx, fy), (fx + 12, fy - 18), (fx + 20, fy - 4),
               (fx + 30, fy - 22), (fx + 34, fy), (fx + 17, fy + 8)],
              fill=(230, 120, 30))


def pic_handshake(d, x, y, w, h, c):
    # circle of stars (EU) + simple Union Jack block (UK)
    cx, cy, r = x + 34, y + h // 2, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 140))
    import math
    for i in range(12):
        a = math.radians(i * 30)
        sx, sy = cx + int(22 * math.cos(a)), cy + int(22 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 210, 60))
    bx, by = x + w - 62, cy - 26
    d.rectangle([bx, by, bx + 52, by + 52], fill=(180, 30, 40))
    d.rectangle([bx + 21, by, bx + 31, by + 52], fill=WHITE)
    d.rectangle([bx, by + 21, bx + 52, by + 31], fill=WHITE)
    d.line([bx, by, bx + 52, by + 52], fill=WHITE, width=5)
    d.line([bx + 52, by, bx, by + 52], fill=WHITE, width=5)
    # link arrow between them
    d.line([cx + r + 4, cy, bx - 6, cy], fill=c, width=5)
    d.polygon([(bx - 6, cy - 8), (bx - 6, cy + 8), (bx + 6, cy)], fill=c)


def pic_bars(d, x, y, w, h, c):
    # prison bars + badge star
    for i in range(5):
        bx = x + 16 + i * 18
        d.line([bx, y + 14, bx, y + h - 14], fill=c, width=7)
    d.line([x + 8, y + 14, x + w - 8, y + 14], fill=c, width=6)
    d.line([x + 8, y + h - 14, x + w - 8, y + h - 14], fill=c, width=6)
    # star badge
    import math
    sx, sy, r = x + w // 2, y + h // 2, 26
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
    d.polygon(pts, fill=(198, 47, 47), outline=(140, 20, 20))


def pic_boat(d, x, y, w, h, c):
    # waves
    for wy in (y + h - 26, y + h - 14):
        d.arc([x + 6, wy - 8, x + 34, wy + 8], 0, 180, fill=c, width=4)
        d.arc([x + 38, wy - 8, x + 66, wy + 8], 0, 180, fill=c, width=4)
        d.arc([x + 70, wy - 8, x + 98, wy + 8], 0, 180, fill=c, width=4)
    # capsized hull (tilted)
    d.polygon([(x + 18, y + 34), (x + 92, y + 52), (x + 84, y + 74),
               (x + 26, y + 58)], fill=c)
    d.line([x + 52, y + 44, x + 62, y + 22], fill=c, width=5)
    d.polygon([(x + 62, y + 22), (x + 84, y + 30), (x + 62, y + 38)],
              fill=(198, 47, 47))


STORIES = [
    dict(tag="CLIMATE", colour=(34, 120, 80), pic=pic_globe,
         head="COP31 climate talks end with no deal",
         body="Nearly 200 nations leave Antalya, Turkey, after a record 48 hours of overtime, split over phasing out fossil fuels."),
    dict(tag="WAR IN UKRAINE", colour=(40, 70, 130), pic=pic_ship_drone,
         head="Drones strike Russian warship in Libya",
         body="Suspected Ukrainian sea drones hit a Russian vessel docked at Benghazi naval base, officials say."),
    dict(tag="MIDDLE EAST", colour=(150, 70, 20), pic=pic_tanker,
         head="Iran hits Bahrain site; tankers struck",
         body="Bahrain says Iran struck a civilian industrial site in Sitra; two tankers are hit in the Strait of Hormuz."),
    dict(tag="EUROPE", colour=(30, 60, 140), pic=pic_handshake,
         head="UK and EU strike new post-Brexit deals",
         body="London and Brussels agree new pacts on trade and travel, pledging to rebuild ties after Brexit."),
    dict(tag="AMERICAS", colour=(120, 40, 90), pic=pic_bars,
         head="Mexico captures \u201cEl Chapo Isidro\u201d",
         body="FBI most-wanted cartel boss Fausto Isidro Meza Flores is seized in Sinaloa; 11 people die in the operation."),
    dict(tag="AFRICA", colour=(20, 110, 130), pic=pic_boat,
         head="Boat capsizes in Nigeria; at least 24 dead",
         body="A boat carrying mourners to a funeral overturns; at least 24 people are killed."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 138], fill=NAVY)
    d.rectangle([0, 138, W, 144], fill=ACCENT)
    f_kicker = font(FONT_B, 22)
    f_title = font(FONT_B, 58)
    f_sub = font(FONT, 24)
    d.text((28, 14), "THE WORLD IN ONE DAY  \u2022  WORLD NEWS",
           font=f_kicker, fill=(255, 210, 60))
    d.text((26, 42), "SUNDAY 22 NOVEMBER 2026", font=f_title, fill=WHITE)
    d.text((28, 106), "Six stories that shaped the day, around the globe.",
           font=f_sub, fill=(200, 210, 225))

    # ---- grid: 2 cols x 3 rows ----
    mx, my = 24, 158
    gap = 16
    pw = (W - 2 * mx - gap) // 2          # 480
    ph = (H - my - 34 - 2 * gap) // 3      # ~272
    f_tag = font(FONT_B, 17)
    f_head = font(FONT_B, 27)
    f_body = font(FONT, 20)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = mx + col * (pw + gap)
        y0 = my + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PANEL,
                            outline=(210, 205, 195), width=2)
        # icon strip
        strip = (118, ph)
        d.rounded_rectangle([x0, y0, x0 + 118, y1], radius=10, fill=s["colour"])
        d.rectangle([x0 + 60, y0, x0 + 118, y1], fill=s["colour"])
        s["pic"](d, x0 + 4, y0 + (ph - 110) // 2, 110, 110, WHITE)

        tx = x0 + 134
        tw = pw - 134 - 16
        ty = y0 + 16
        d.text((tx, ty), s["tag"], font=f_tag, fill=s["colour"])
        ty += 28
        for line in wrap(d, s["head"], f_head, tw)[:3]:
            d.text((tx, ty), line, font=f_head, fill=INK)
            ty += 33
        ty += 4
        for line in wrap(d, s["body"], f_body, tw)[:4]:
            d.text((tx, ty), line, font=f_body, fill=(50, 58, 70))
            ty += 26

    # ---- footer ----
    f_foot = font(FONT, 17)
    d.text((W // 2, H - 26), "Reported 22 November 2026  \u2022  Sources: AP, Al Jazeera, AFP, The Hindu",
           font=f_foot, fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
