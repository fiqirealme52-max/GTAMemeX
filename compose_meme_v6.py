#!/usr/bin/env python3
"""Compose the GTA 6 meme v6 for make.fun bounty gta6-meme-x-01.

Format: a FAKE OFFICIAL DOCUMENT -- a tax-audit notice from the
Leonida Revenue Service. v6 is a FRESH build (new premise, new form),
but it carries v4's winning DNA and fixes v5's proven failures.

What the board proved (fetched 23 Nov 16:12 WIB, 4,769 entries):
  - 178 entries are 12-0-0; the last one sits at #444 (0.838885).
    12-0-0 alone is only the entry ticket -- MARGIN decides rank:
    #1 0.912056, #10 0.901748, #50 0.893303, #100 0.884675.
  - #1 vs #2 are THE SAME eviction notice. The ONLY difference:
    #1 adds "Less: paid by my AI agent on make.fun -$2,240.99"
    -> TOTAL DUE $0.00 + "PAID IN FULL". That one twist is worth
    the #1 spot (+0.0041). The twist RESOLVES the document: the
    agent already paid it, so nothing is due.
  - v4 "Sick Note" (8W-3D-1L, 0.811075): ONE coherent story, one
    clear joke, readable -- but thin (1 price, no priced lines, no
    magenta band, weak make.fun sell). It drew 3x because the judge
    could not separate its thin joke from house opponents'.
  - v5 "WANTED" (7W-1D-4L, 0.792639): MORE density but MORE losses.
    Why, from the artifacts:
    (a) FORM INCOHERENCE: a wanted poster with an itemized
        "STATEMENT OF FINES" and TOTAL DUE. Real posters carry a
        REWARD, not fines -- the sheriff does not fine the fugitive
        on the poster. Compare #5 (fines make sense on a citation),
        #10 (charges make sense on a power bill).
    (b) PAID/TOTAL CONTRADICTION: "PAID / BY MY AI AGENT" stamp
        over "TOTAL DUE $9,163.13". If it is paid, the amount due
        is $0.00 (#1, #10 resolve this; v5 does not).
    (c) YEAR-AS-PRICE DECODING: $2,025.00 / $2,013.00 need a
        second of decoding ("price = year"). Top-10 prices are
        direct arithmetic ($2,028 = 156 x $13; $1,300 = 13 years;
        $4,811 = days; $79.99 = game price).
    (d) COP-FAMILY CROWDING: #12 impounded, #13 penitentiary,
        #14 paroled, #18 release, #26 booking sheet (SAME
        "LEONIDA COUNTY SHERIFF'S OFFICE" header), #40 booking
        photo -- v5 reads as another cop document at first glance.
  - v6 fixes all four: a tax notice whose charges MAKE SENSE on
    the form; the #1 zero-twist (Less: paid -> TOTAL DUE $0.00 +
    PAID IN FULL); direct-arithmetic prices only; a premise with
    exactly ONE weak entry on the board (#426 "Got audited",
    0.8x) and no tax entry in the top 100 (best tax #261).

Winner DNA carried over:
  - authority header + giant title + field grid
  - 7 priced charge lines with dotted leaders (prices ARE jokes)
  - the #1 twist: Less line + TOTAL DUE $0.00 + PAID IN FULL stamp
  - magenta footer band: ghost + "PAID BY MY AI AGENT" + make.fun
  - form-number footer; joke numbers 13y / 4,811d / 17 Sep 2013 /
    214 GB / 87 trailers / $79.99 game price
  - v4's DNA: taxpayer "EVERY GAMER ON EARTH", v4's $481.10
    (its total) returns as the interest line, one coherent story,
    clean readability.

Everything is drawn with PIL (crisp typography, never trusted to an
image generator, which garbles words). Deterministic: two runs on
the same script produce a byte-identical meme-v6.png.

Layout (1024x1024):
  24..1000  navy double border frame
  48..100   LEONIDA REVENUE SERVICE header + dept line
  108..200  NOTICE OF AUDIT (giant) + red sub-line
  240..350  rule + field grid (3 rows)
  362..414  body paragraph (the notice text)
  416..438  FINDING: THE WAIT WAS THE TAX. (bottom punchline)
  448..750  STATEMENT OF CHARGES: 7 priced lines + Less line
  758..812  TOTAL DUE $0.00 + PAID IN FULL stamp (clear zone)
  868..958  magenta footer band (ghost + pitch + make.fun pill)
  968       form footer
The ghost is ~160px wide, overlapping the band's top edge -- clearly
recognisable at 480x480.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme-v6.png")
PREVIEW_480 = os.path.join(HERE, "meme-v6-480.png")

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
BLACK = (18, 18, 22)
WHITE = (255, 255, 255)
RED = (198, 12, 32)
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


def paid_in_full_stamp():
    """Red PAID IN FULL stamp on a transparent layer: double border."""
    W, H = 260, 82
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([5, 5, W - 5, H - 5], radius=10,
                        outline=RED + (255,), width=5)
    d.rounded_rectangle([11, 11, W - 11, H - 11], radius=8,
                        outline=RED + (255,), width=2)
    for txt, fnt, yy in (("PAID IN FULL", f(SANS_B, 34), 8),
                         ("BY MY AI AGENT", f(SANS_B, 17), 52)):
        w = d.textlength(txt, font=fnt)
        d.text(((W - w) / 2, yy), txt, font=fnt, fill=RED + (255,))
    return layer


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


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

    # --- authority header ---
    office = "LEONIDA REVENUE SERVICE"
    of = f(SANS_B, 30)
    w = draw.textlength(office, font=of)
    draw.text(((SIZE - w) / 2, 48), office, font=of, fill=NAVY)
    dept = "DEPT. OF WAITING  ·  VICE CITY, LEONIDA  ·  EST. 2013"
    df = f(SANS_B, 17)
    w = draw.textlength(dept, font=df)
    draw.text(((SIZE - w) / 2, 84), dept, font=df, fill=GRAY)

    # --- giant title + red sub-line ---
    title = "NOTICE OF AUDIT"
    tf = f(SERIF_B, 80)
    w = draw.textlength(title, font=tf)
    assert w < 864, ("title too wide", w)
    draw.text(((SIZE - w) / 2, 112), title, font=tf, fill=BLACK)
    sub = "TAX YEARS 2013–2026  ·  YOUR PATIENCE HAS BEEN ASSESSED"
    sf = f(SANS_B, 21)
    w = draw.textlength(sub, font=sf)
    draw.text(((SIZE - w) / 2, 202), sub, font=sf, fill=RED)

    # --- field grid ---
    draw.line([(80, 240), (SIZE - 80, 240)], fill=NAVY, width=2)
    lab_f = f(SANS_B, 18)
    val_f = f(MONO_B, 21)
    for y, (ll, lv, rl, rv) in (
            (256, ("TAXPAYER", "EVERY GAMER ON EARTH", "TAX YEARS",
                   "2013–2026")),
            (286, ("AUDIT NO.", "13-4811", "ASSESSED", "23 NOV 2026")),
            (316, ("AUDITOR", "AGENT 13", "STATUS", "13 YEARS LATE"))):
        draw.text((80, y), ll, font=lab_f, fill=GRAY)
        draw.text((80 + draw.textlength(ll, font=lab_f) + 10, y),
                  lv, font=val_f, fill=BLACK)
        rw = draw.textlength(rv, font=val_f)
        rlw = draw.textlength(rl, font=lab_f)
        draw.text((SIZE - 80 - rw - rlw - 10, y), rl, font=lab_f,
                  fill=GRAY)
        draw.text((SIZE - 80 - rw, y), rv, font=val_f, fill=BLACK)

    # --- body paragraph (the notice text) ---
    body = ("You are hereby notified that your 13 years of waiting for "
            "Grand Theft Auto VI have been selected for audit. Our "
            "records show you believed every delay. Twice.")
    bf = f(SANS, 21)
    lines = wrap_text(draw, body, bf, SIZE - 160)
    assert len(lines) == 2, lines
    y = 362
    for ln in lines:
        draw.text((80, y), ln, font=bf, fill=BLACK)
        y += 26
    # bottom punchline lives here, under the body -- the stamp zone
    # below the total must stay clear of any text
    find = "FINDING: THE WAIT WAS THE TAX."
    ff2 = f(SANS_B, 22)
    draw.text((80, 416), find, font=ff2, fill=NAVY)

    # --- statement of charges ---
    draw.line([(80, 448), (SIZE - 80, 448)], fill=NAVY, width=2)
    head = "STATEMENT OF CHARGES"
    hf = f(SANS_B, 23)
    draw.text((80, 460), head, font=hf, fill=NAVY)
    keep = "DETACH AND KEEP"
    kf = f(SANS_B, 15)
    kw = draw.textlength(keep, font=kf)
    draw.text((SIZE - 80 - kw, 464), keep, font=kf, fill=GRAY)
    charges = [
        ("Waiting tax — 4,811 days @ $1.00/day", 4811.00),
        ("Interest — 4,811 days @ $0.10/day", 481.10),
        ("False-hope penalty — 2 delays", 260.00),
        ("Download duty — 214 GB, undelivered", 214.00),
        ("Trailer tax — 87 trailers watched", 87.00),
        ("GTA VI — standard edition", 79.99),
        ("Patience — 13 years, fully depreciated", 0.00),
    ]
    total = sum(p for _, p in charges)
    assert abs(total - 5933.09) < 0.005, total
    lab2 = f(SANS, 24)
    prc = f(MONO_B, 24)
    y = 494
    for label, price in charges:
        ptxt = "$%s" % format(price, ",.2f")
        pw = draw.textlength(ptxt, font=prc)
        lw = draw.textlength(label, font=lab2)
        assert 80 + lw + 12 < SIZE - 80 - pw - 12, label
        draw.text((80, y), label, font=lab2, fill=BLACK)
        dotted_leader(draw, 80 + lw + 12, SIZE - 80 - pw - 12, y + 14)
        draw.text((SIZE - 80 - pw, y), ptxt, font=prc, fill=BLACK)
        y += 31
    # the #1 twist: Less line -- the agent already paid it all
    draw.text((80, y + 2), "Less: paid by my AI agent on make.fun",
              font=f(SANS_B, 24), fill=RED)
    less_txt = "-$5,933.09"
    lw = draw.textlength(less_txt, font=prc)
    draw.text((SIZE - 80 - lw, y + 2), less_txt, font=prc, fill=RED)
    y += 35
    # total due: $0.00
    draw.line([(80, y + 6), (SIZE - 80, y + 6)], fill=NAVY, width=2)
    draw.text((80, y + 18), "TOTAL DUE", font=f(SANS_B, 26), fill=GRAY)
    ttxt = "$0.00"
    tf2 = f(SANS_B, 44)
    tw = draw.textlength(ttxt, font=tf2)
    draw.text((SIZE - 80 - tw, y + 12), ttxt, font=tf2, fill=NAVY_DARK)

    # --- red PAID IN FULL stamp over the total row (middle; the
    # Less line above and the band below both stay clear) ---
    stamp = paid_in_full_stamp().rotate(-8, expand=True,
                                         resample=Image.BICUBIC)
    paper.paste(stamp, (350, 745), stamp)

    # --- magenta footer band: ghost + pitch + make.fun pill ---
    band_y0, band_y1 = 868, 958
    draw.rounded_rectangle([48, band_y0, SIZE - 48, band_y1], radius=14,
                           fill=MAGENTA)
    ghost = ghost_image().resize((160, 174), Image.LANCZOS)
    paper.paste(ghost, (64, 800), ghost)
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
    foot = "FORM LRS-13 · LEONIDA REVENUE SERVICE · PAGE 1 OF 1"
    ff = f(MONO, 14)
    w = draw.textlength(foot, font=ff)
    draw.text(((SIZE - w) / 2, 968), foot, font=ff, fill=GRAY)

    paper.save(OUT, "PNG")
    paper.resize((480, 480), Image.LANCZOS).save(PREVIEW_480, "PNG")
    print("saved", OUT, paper.size, "total $%.2f" % total)


if __name__ == "__main__":
    build()
