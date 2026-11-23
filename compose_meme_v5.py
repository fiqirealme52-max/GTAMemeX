#!/usr/bin/env python3
"""Compose the GTA 6 meme v5 for make.fun bounty gta6-meme-x-01.

Format: a FAKE OFFICIAL DOCUMENT -- a WANTED poster from the Leonida
County Sheriff's Office. The top-10 winners are all dense fake official
documents, so v5 keeps the winner family's DNA and changes the premise
to one that is still unused on the board (0 hits for "wanted" in the
current top 100): GTA VI as the most wanted fugitive in Leonida.

Winner DNA carried over, item by item:
  - authority header + giant title + field grid
  - 7 priced charge lines with dotted leaders (the prices ARE jokes)
  - one big TOTAL DUE + red PAID stamp, rotated, over the total row
  - magenta footer band: ghost + "PAID BY MY AI AGENT" + make.fun pill
  - form-number footer; joke numbers 13y / 4,811d / 17 Sep 2013 /
    214 GB / perjury $2,025 / trespassing $2,013 / "Fall 2025" /
    26 May 2026 / 87 rewatches

Everything is drawn with PIL (crisp typography, never trusted to an
image generator, which garbles words). Deterministic: two runs on the
same script produce a byte-identical meme-v5.png.

Layout (1024x1024):
  24..1000  navy double border frame
  48..300   sheriff header + WANTED + sub-line + 5 gold stars
  308..448  fugitive name, alias/last seen, field rows
  462..745  CHARGES: 7 priced lines + TOTAL DUE $9,163.13
  726..859  red PAID stamp over the total row (middle, price stays clear)
  868..958  magenta footer band (ghost + pitch + make.fun pill)
  968       form footer
The ghost is ~170px tall, overlapping the band's top edge -- clearly
recognisable at 480x480.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme-v5.png")
PREVIEW_480 = os.path.join(HERE, "meme-v5-480.png")

SIZE = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")

NAVY = (27, 42, 94)
NAVY_DARK = (16, 26, 66)
GRAY = (68, 74, 92)
LIGHT_RULE = (190, 192, 205)
BLACK = (18, 18, 22)
WHITE = (255, 255, 255)
RED = (198, 12, 32)
GOLD = (212, 175, 55)
GOLD_DARK = (150, 110, 15)
MAGENTA = (230, 0, 126)
MAGENTA_DARK = (138, 0, 80)
PAPER_TOP = (253, 248, 238)
PAPER_BOT = (247, 239, 221)


def f(path, px):
    return ImageFont.truetype(path, px)


def vgrad(w, h, top, bottom):
    """Vertical gradient image."""
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def sparkle(cx, cy, v_arm, h_arm):
    """4-pointed sparkle polygon (diamond star), 8 vertices."""
    pts = []
    for ang in (270, 0, 90, 180):
        r = v_arm if ang in (90, 270) else h_arm
        a = math.radians(ang)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        a2 = math.radians(ang + 45)
        cr = min(v_arm, h_arm) * 0.45
        pts.append((cx + cr * math.cos(a2), cy + cr * math.sin(a2)))
    return pts


def star5(cx, cy, r_out, r_in):
    """Regular 5-pointed star polygon, 10 vertices."""
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def dotted_leader(d, x1, x2, y, color=GRAY):
    """Row of dots filling the gap between a label and its price."""
    x = x1
    while x < x2 - 3:
        d.ellipse([x, y - 2, x + 3, y + 1], fill=color)
        x += 9


def ghost_image():
    """The make.fun ghost on a transparent layer (240x260).

    White ghost, thick black outline, two black 4-point sparkle eyes,
    one small round hand holding a magenta coin with a white star.
    The body is built from an ellipse dome + rectangle + three notches
    cut from the hem; the outline comes from dilating that mask.
    """
    W, H = 240, 260
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    cx, top, r, bottom = 110, 18, 82, 218
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, top, cx + r, top + 2 * r], fill=255)
    md.rectangle([cx - r, top + r, cx + r, bottom], fill=255)
    for i in range(3):  # wavy hem: three semicircular notches
        bx = cx - r + (2 * r / 3) * (i + 0.5)
        md.ellipse([bx - 28, bottom - 28, bx + 28, bottom + 28], fill=0)

    outline = mask.filter(ImageFilter.MaxFilter(9))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    layer.paste(black, (0, 0), outline)
    layer.paste(white, (0, 0), mask)

    d = ImageDraw.Draw(layer)
    d.polygon(sparkle(82, 120, 28, 10), fill=(0, 0, 0, 255))
    d.polygon(sparkle(138, 120, 28, 10), fill=(0, 0, 0, 255))
    # magenta coin with white star, held out to the side by a round hand
    # (coin kept fully inside the layer: right edge 234 < layer width 240)
    d.ellipse([182, 124, 234, 176], fill=MAGENTA_DARK + (255,))
    d.ellipse([185, 127, 231, 173], fill=MAGENTA + (255,))
    d.polygon(star5(208, 150, 17, 7), fill=(255, 255, 255, 255))
    d.ellipse([164, 146, 192, 174], fill=(0, 0, 0, 255))
    d.ellipse([167, 149, 189, 171], fill=(255, 255, 255, 255))
    return layer


def paid_stamp():
    """Red PAID stamp on a transparent layer: double border, 2 lines."""
    W, H = 280, 95
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([5, 5, W - 5, H - 5], radius=10,
                        outline=RED + (255,), width=5)
    d.rounded_rectangle([11, 11, W - 11, H - 11], radius=8,
                        outline=RED + (255,), width=2)
    for txt, fnt, yy in (("PAID", f(SANS_B, 46), 8),
                         ("BY MY AI AGENT", f(SANS_B, 19), 60)):
        w = d.textlength(txt, font=fnt)
        d.text(((W - w) / 2, yy), txt, font=fnt, fill=RED + (255,))
    return layer


def build():
    paper = vgrad(SIZE, SIZE, PAPER_TOP, PAPER_BOT)
    d = ImageDraw.Draw(paper, "RGBA")
    # seeded paper speckle (deterministic)
    rng = random.Random(20261123)
    for _ in range(1400):
        x = rng.randint(0, SIZE - 1)
        y = rng.randint(0, SIZE - 1)
        d.point((x, y), fill=(120, 100, 60, rng.randint(4, 10)))
    # navy double border frame
    d.rectangle([24, 24, SIZE - 24, SIZE - 24], outline=NAVY, width=4)
    d.rectangle([36, 36, SIZE - 36, SIZE - 36], outline=NAVY, width=1)
    draw = ImageDraw.Draw(paper)

    # --- sheriff header ---
    office = "LEONIDA COUNTY SHERIFF'S OFFICE"
    of = f(SANS_B, 25)
    w = draw.textlength(office, font=of)
    draw.text(((SIZE - w) / 2, 48), office, font=of, fill=NAVY)
    wanted = "WANTED"
    wf = f(SERIF_B, 132)
    w = draw.textlength(wanted, font=wf)
    draw.text(((SIZE - w) / 2, 76), wanted, font=wf, fill=BLACK)
    sub = "DEAD OR ALIVE — PREFERABLY OUT NOW"
    sf = f(SANS_B, 25)
    w = draw.textlength(sub, font=sf)
    draw.text(((SIZE - w) / 2, 212), sub, font=sf, fill=RED)
    # 5 gold stars: the wanted level
    for i in range(5):
        sx = SIZE // 2 + (i - 2) * 88
        draw.polygon(star5(sx, 254, 30, 12), fill=GOLD,
                     outline=GOLD_DARK, width=3)

    # --- fugitive block ---
    draw.line([(80, 296), (SIZE - 80, 296)], fill=NAVY, width=2)
    name = "GRAND THEFT AUTO VI"
    nf = f(SANS_B, 46)
    w = draw.textlength(name, font=nf)
    draw.text(((SIZE - w) / 2, 308), name, font=nf, fill=NAVY_DARK)
    alias = "ALIAS GTA VI  ·  LAST SEEN LOS SANTOS, 17 SEP 2013  ·  AT LARGE"
    af = f(MONO_B, 21)
    w = draw.textlength(alias, font=af)
    draw.text(((SIZE - w) / 2, 362), alias, font=af, fill=BLACK)
    # field rows: label small gray, value mono bold
    lab_f = f(SANS_B, 18)
    val_f = f(MONO_B, 21)
    for y, (ll, lv, rl, rv) in (
            (394, ("CASE NO.", "W-13-4811", "ISSUED", "23 NOV 2026")),
            (420, ("REWARD", "$500", "PAID TO", "MY AI AGENT"))):
        draw.text((80, y), ll, font=lab_f, fill=GRAY)
        draw.text((80 + draw.textlength(ll, font=lab_f) + 10, y),
                  lv, font=val_f, fill=BLACK)
        rw = draw.textlength(rv, font=val_f)
        rlw = draw.textlength(rl, font=lab_f)
        draw.text((SIZE - 80 - rw - rlw - 10, y), rl, font=lab_f,
                  fill=GRAY)
        draw.text((SIZE - 80 - rw, y), rv, font=val_f, fill=BLACK)
    # --- charges: statement of fines ---
    draw.line([(80, 448), (SIZE - 80, 448)], fill=NAVY, width=2)
    head = "CHARGES — STATEMENT OF FINES"
    hf = f(SANS_B, 23)
    draw.text((80, 462), head, font=hf, fill=NAVY)
    charges = [
        ("Grand theft auto — 13 years on the run", 4811.00),
        ('Perjury — swore "Fall 2025" under oath', 2025.00),
        ("Evading a 214 GB download", 214.00),
        ("Trespassing — squatting in Vice City since 2013", 2013.00),
        ("87 trailer rewatches", 87.00),
        ("Impersonating a launch date — 26 May 2026", 13.13),
        ("Mugshot — none on file, still at large since 2013", 0.00),
    ]
    total = sum(p for _, p in charges)
    assert abs(total - 9163.13) < 0.005, total
    lab2 = f(SANS, 24)
    prc = f(MONO_B, 24)
    y = 496
    for label, price in charges:
        ptxt = "$%s" % format(price, ",.2f")
        pw = draw.textlength(ptxt, font=prc)
        lw = draw.textlength(label, font=lab2)
        draw.text((80, y), label, font=lab2, fill=BLACK)
        dotted_leader(draw, 80 + lw + 12, SIZE - 80 - pw - 12, y + 14)
        draw.text((SIZE - 80 - pw, y), ptxt, font=prc, fill=BLACK)
        y += 33
    # total due
    draw.line([(80, y + 6), (SIZE - 80, y + 6)], fill=NAVY, width=2)
    draw.text((80, y + 18), "TOTAL DUE", font=f(SANS_B, 26), fill=GRAY)
    ttxt = "$9,163.13"
    tf = f(SANS_B, 44)
    tw = draw.textlength(ttxt, font=tf)
    draw.text((SIZE - 80 - tw, y + 12), ttxt, font=tf, fill=NAVY_DARK)

    # --- red PAID stamp over the total row (middle; price stays clear) ---
    stamp = paid_stamp().rotate(-8, expand=True, resample=Image.BICUBIC)
    paper.paste(stamp, (330, 726), stamp)

    # --- magenta footer band: ghost + pitch + make.fun pill ---
    band_y0, band_y1 = 868, 958
    draw.rounded_rectangle([48, band_y0, SIZE - 48, band_y1], radius=14,
                           fill=MAGENTA)
    ghost = ghost_image().resize((170, 184), Image.LANCZOS)
    paper.paste(ghost, (62, 798), ghost)
    draw.text((240, 884), "PAID BY MY AI AGENT", font=f(SANS_B, 38),
              fill=WHITE)
    draw.text((240, 926), "with real money it won in make.fun bounties.",
              font=f(SANS, 22), fill=WHITE)
    # make.fun pill: width sized from the text so nothing overflows it
    pill = "make.fun"
    pf = f(SANS_B, 28)
    pw = draw.textlength(pill, font=pf)
    px1, py0, py1 = 950, 888, 938
    px0 = px1 - int(pw) - 40
    draw.rounded_rectangle([px0, py0, px1, py1], radius=25,
                           fill=WHITE)
    draw.text(((px0 + px1 - pw) / 2, py0 + 9), pill, font=pf,
              fill=MAGENTA)

    # --- form footer ---
    foot = "FORM W-13 · LEONIDA COUNTY SHERIFF'S OFFICE · PAGE 1 OF 1"
    ff = f(MONO, 14)
    w = draw.textlength(foot, font=ff)
    draw.text(((SIZE - w) / 2, 968), foot, font=ff, fill=GRAY)

    paper.save(OUT, "PNG")
    paper.resize((480, 480), Image.LANCZOS).save(PREVIEW_480, "PNG")
    print("saved", OUT, paper.size, "total $%.2f" % total)


if __name__ == "__main__":
    build()
