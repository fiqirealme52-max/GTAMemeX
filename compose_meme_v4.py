#!/usr/bin/env python3
"""Compose the GTA 6 meme v4 for make.fun bounty gta6-meme-x-01.

Joke angle (NEW format, same sick-day joke as v3): a FAKE OFFICIAL
DOCUMENT -- Vice City General Hospital discharge papers / sick-leave
certificate. Top-10 winners are all itemised fake official documents,
so this keeps v3's joke (launch-day mass sick day) and changes ONLY the
format (scene -> document): one variable, per the hypothesis that the
document format lifts the pairwise win rate vs v3 (0.549).

Pipeline: the whole document is drawn with PIL (crisp typography --
never trusted to an image generator, which garbles words). The script
first renders the blank paper background (scene-v4.png: cream paper,
navy frame, red-cross emblem, faint sunset + palm watermark), then
composites all document text, the bill box, the red PAID stamp and the
make.fun ghost on top (meme-v4.png). Deterministic: two runs on the
same script produce a byte-identical meme-v4.png (seeded texture).

Layout (1024x1024):
  24..36    navy double border frame
  60..150   hospital header (cross emblem + name + subtitle)
  172..225  document title + form number
  235..435  patient fields (5 ruled rows, mono values)
  460..840  four sections: DIAGNOSIS / SYMPTOMS / PRESCRIPTION / NOTES
  850..935  bill box ($481.10) + red PAID stamp + ghost
  950..990  footer disclaimer
The ghost is ~170px tall at the bottom right -- recognisable at 480x480.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "scene-v4.png")
OUT = os.path.join(HERE, "meme-v4.png")
PREVIEW_480 = os.path.join(HERE, "meme-v4-480.png")

SIZE = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_I = os.path.join(FONT_DIR, "DejaVuSerif.ttf")  # no serif italic on box
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

NAVY = (27, 42, 94)
NAVY_DARK = (16, 26, 66)
GRAY = (68, 74, 92)
LIGHT_RULE = (190, 192, 205)
BLACK = (18, 18, 22)
WHITE = (255, 255, 255)
RED = (198, 12, 32)
RED_DARK = (150, 8, 24)
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


def wrap(draw, text, font_obj, max_w):
    """Greedy word wrap to max_w, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font_obj) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star4_points(cx, cy, v_arm, h_arm):
    """4-pointed sparkle (diamond star): 8 vertices, long vertical arms."""
    pts = []
    for ang in (270, 0, 90, 180):
        r = v_arm if ang in (90, 270) else h_arm
        a = math.radians(ang)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        a2 = math.radians(ang + 45)
        cr = min(v_arm, h_arm) * 0.45
        pts.append((cx + cr * math.cos(a2), cy + cr * math.sin(a2)))
    return pts


def star5_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def palm(draw, x, y, s, color):
    """Simple palm silhouette: curved trunk + 6 fronds. (x, y) = base."""
    # trunk: slightly curved thick line
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((x + 10 * s * math.sin(t * 1.2) - 4 * s * t,
                    y - 90 * s * t))
    draw.line(pts, fill=color, width=max(2, int(7 * s)))
    top = pts[-1]
    # fronds: arcs drooping from the crown
    for ang in (-150, -110, -70, -30, 10, 50):
        a = math.radians(ang)
        ex = top[0] + 55 * s * math.cos(a)
        ey = top[1] + 55 * s * math.sin(a) * 0.55 + 18 * s
        mx = top[0] + 30 * s * math.cos(a)
        my = top[1] + 30 * s * math.sin(a) * 0.55 - 6 * s
        draw.line([top, (mx, my), (ex, ey)], fill=color,
                  width=max(2, int(4 * s)))


def ghost_layer():
    """The make.fun ghost on a transparent layer (240x260).

    White ghost, thick black outline, two black 4-point sparkle eyes,
    one small round hand holding a magenta coin with a white star.
    Outline made by dilating the body mask (MaxFilter) so it is even.
    """
    W, H = 240, 260
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    cx, dome_cy, r = 105, 105, 78
    pts = []
    for deg in range(180, -1, -6):  # dome arc, left -> right over the top
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), dome_cy - r * math.sin(a)))
    pts.append((cx + r, 205))
    bump_r = r * 2 / 6
    for i in range(3):  # wavy bottom: 3 upward bumps, right -> left
        bcx = cx + r - bump_r * (2 * i + 1)
        for deg in range(0, 181, 12):
            a = math.radians(deg)
            pts.append((bcx + bump_r * math.cos(a),
                        205 - bump_r * math.sin(a)))
    pts.append((cx - r, 205))

    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(pts, fill=255)
    outline_mask = mask.filter(ImageFilter.MaxFilter(9))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    layer.paste(black, (0, 0), outline_mask)
    layer.paste(white, (0, 0), mask)

    d = ImageDraw.Draw(layer)
    d.polygon(star4_points(78, 118, 26, 9), fill=(0, 0, 0, 255))
    d.polygon(star4_points(132, 118, 26, 9), fill=(0, 0, 0, 255))
    d.ellipse([168, 148, 196, 176], fill=(0, 0, 0, 255))
    d.ellipse([171, 151, 193, 173], fill=(255, 255, 255, 255))
    d.ellipse([186, 128, 238, 180], fill=MAGENTA_DARK + (255,))
    d.ellipse([189, 131, 235, 177], fill=MAGENTA + (255,))
    d.polygon(star5_points(212, 154, 19, 8), fill=(255, 255, 255, 255))
    return layer


def stamp_layer():
    """Red PAID stamp on a transparent layer, double border, 2 lines."""
    W, H = 320, 115
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # double border
    d.rounded_rectangle([6, 6, W - 6, H - 6], radius=12,
                        outline=RED + (255,), width=5)
    d.rounded_rectangle([13, 13, W - 13, H - 13], radius=9,
                        outline=RED + (255,), width=2)
    # lines of stamp text, centred (line 1 measured 303px at 25px,
    # fits the 320px layer; at 28px it was 339px and clipped)
    f1 = f(SANS_B, 25)
    f2 = f(SANS_B, 34)
    for txt, fnt, yy in (("PAID BY MY AI AGENT", f1, 16),
                         ("ON MAKE.FUN", f2, 54)):
        w = d.textlength(txt, font=fnt)
        d.text(((W - w) / 2, yy), txt, font=fnt, fill=RED + (255,))
    # small stars flanking the bottom line
    d.polygon(star5_points(38, 98, 9, 4), fill=RED + (255,))
    d.polygon(star5_points(W - 38, 98, 9, 4), fill=RED + (255,))
    return layer


def build_scene():
    """Blank hospital paper background (scene-v4.png)."""
    paper = vgrad(SIZE, SIZE, PAPER_TOP, PAPER_BOT)
    d = ImageDraw.Draw(paper, "RGBA")
    # seeded paper speckle (deterministic)
    rng = random.Random(20260526)
    for _ in range(1600):
        x = rng.randint(0, SIZE - 1)
        y = rng.randint(0, SIZE - 1)
        d.point((x, y), fill=(120, 100, 60, rng.randint(4, 10)))
    # navy double border frame
    d.rectangle([24, 24, SIZE - 24, SIZE - 24], outline=NAVY, width=4)
    d.rectangle([36, 36, SIZE - 36, SIZE - 36], outline=NAVY, width=1)
    # (no sunset strip at the bottom: the footer disclaimer sits there
    # and needs clean contrast)
    d = ImageDraw.Draw(paper, "RGBA")
    # faint sun + palms watermark, top-right corner (free of text)
    wm = Image.new("RGBA", (220, 150), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    wd.ellipse([88, 8, 148, 68], fill=(255, 150, 60, 70))
    palm(wd, 30, 148, 0.9, (90, 40, 90, 55))
    palm(wd, 185, 148, 0.7, (90, 40, 90, 55))
    paper.paste(wm, (SIZE - 36 - 220, 44), wm)
    # red-cross emblem, top-left
    d.ellipse([64, 56, 128, 120], outline=NAVY, width=3,
              fill=(255, 255, 255, 255))
    d.rectangle([91, 66, 101, 110], fill=RED)   # vertical bar
    d.rectangle([76, 81, 116, 95], fill=RED)    # horizontal bar
    return paper


def main():
    canvas = build_scene()
    canvas.save(SCENE, "PNG")
    draw = ImageDraw.Draw(canvas)

    # --- hospital header ---
    title = "VICE CITY GENERAL HOSPITAL"
    tf = f(SERIF_B, 44)
    w = draw.textlength(title, font=tf)
    draw.text(((SIZE - w) / 2 + 20, 64), title, font=tf, fill=NAVY)
    sub = "LEONIDA   ·   EST. 1986   ·   EMERGENCY — OUTPATIENT — WAITING"
    sf = f(SANS_B, 19)
    w = draw.textlength(sub, font=sf)
    draw.text(((SIZE - w) / 2, 118), sub, font=sf, fill=GRAY)
    draw.line([(80, 152), (SIZE - 80, 152)], fill=NAVY, width=3)

    # --- document title + form number ---
    dt = "CERTIFICATE OF SICK LEAVE"
    df = f(SANS_B, 33)
    w = draw.textlength(dt, font=df)
    draw.text(((SIZE - w) / 2, 172), dt, font=df, fill=NAVY_DARK)
    fn = "FORM VCG-26 · No. 04811"
    ff = f(MONO_B, 19)
    draw.text((SIZE - 80 - draw.textlength(fn, font=ff), 224), fn,
              font=ff, fill=GRAY)

    # --- patient fields (5 ruled rows) ---
    fields = [
        ("PATIENT", "Every gamer on Earth"),
        ("ADMITTED", "26 May 2026 — GTA VI launch day"),
        ("DISCHARGED", "When the download finishes"),
        ("DOCTOR", "Dr. Lucia Santos, MD"),
        ("DEPARTMENT", "Dept. of Leonida Waiting"),
    ]
    lab_f = f(SANS_B, 23)
    val_f = f(MONO_B, 25)
    y = 258
    for label, value in fields:
        draw.text((80, y), label, font=lab_f, fill=GRAY)
        draw.text((300, y), value, font=val_f, fill=BLACK)
        draw.line([(80, y + 33), (SIZE - 80, y + 33)],
                  fill=LIGHT_RULE, width=1)
        y += 40

    # --- itemised sections ---
    sections = [
        ("DIAGNOSIS",
         "Acute Vice City Fever. Onset: 13 years ago — 26 May 2013."),
        ("SYMPTOMS",
         "Unable to stop checking the countdown — 4,811 days and counting."),
        ("PRESCRIPTION",
         "Rest + GTA VI. Dosage: one 214 GB download, taken with "
         "13 years of patience."),
        ("NOTES",
         "Patient refused to return to work. Entire office also admitted."),
    ]
    sec_f = f(SANS_B, 22)
    body_f = f(SANS, 26)
    y = 452
    for head, body in sections:
        draw.rectangle([80, y + 4, 92, y + 16], fill=RED)
        draw.text((104, y), head, font=sec_f, fill=NAVY)
        y += 30
        for line in wrap(draw, body, body_f, SIZE - 160):
            draw.text((80, y), line, font=body_f, fill=BLACK)
            y += 30
        y += 6

    # --- bill box + stamp + ghost ---
    # bill box (left)
    draw.rounded_rectangle([80, 820, 480, 906], radius=10,
                           outline=NAVY, width=3, fill=(255, 255, 255, 255))
    draw.text((104, 830), "TOTAL DUE", font=f(SANS_B, 20), fill=GRAY)
    draw.text((104, 852), "$481.10", font=f(SANS_B, 40), fill=NAVY_DARK)
    # red PAID stamp, rotated -6 deg, right of the bill box; its rotated
    # box (~335x147) fits between the NOTES line (ends ~800) and the
    # footer (starts ~960) without covering either
    stamp = stamp_layer().rotate(-6, expand=True, resample=Image.BICUBIC)
    canvas.paste(stamp, (480, 806), stamp)
    # ghost, bottom right, holding its magenta coin
    ghost = ghost_layer().resize((150, 163), Image.LANCZOS)
    canvas.paste(ghost, (825, 795), ghost)

    # --- footer disclaimer ---
    foot = ("This note excuses the patient from work, school and all "
            "responsibilities until further notice.")
    ff2 = f(SERIF_I, 17)
    w = draw.textlength(foot, font=ff2)
    draw.text(((SIZE - w) / 2, 962), foot, font=ff2, fill=GRAY)

    canvas.save(OUT, "PNG")
    canvas.resize((480, 480), Image.LANCZOS).save(PREVIEW_480, "PNG")
    print("saved", OUT, canvas.size)


if __name__ == "__main__":
    main()
