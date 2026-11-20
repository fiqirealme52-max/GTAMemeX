#!/usr/bin/env python3
"""Compose the GTA 6 meme v2 for make.fun bounty gta6-meme-x-01.

Pipeline: AI-generated two-panel scene (scene-v2.png, 2240x1120) + PIL
compositing of the make.fun ghost mascot, headline, year labels and the
punchline banner. Everything PIL does here is deterministic: running this
script twice on the same scene-v2.png produces a byte-identical meme.png.

Layout (1024x1024):
  0..120    headline band (Vice City sunset gradient)
  120..800  scene, cover-cropped to 1024x680
  800..1024 punchline banner (dark rounded rect)
The ghost floats at the centre divider, overlapping the top of the scene.
Text is drawn with PIL (bold DejaVu + black outline) -- never trusted to
the image generator, which garbles words.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "scene-v2.png")
OUT = os.path.join(HERE, "meme.png")
PREVIEW_480 = "/tmp/meme-v2-480.png"

SIZE = 1024
BAND_H = 120          # headline band height
BANNER_TOP = 800      # punchline banner starts here
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAGENTA = (230, 0, 126)
MAGENTA_DARK = (138, 0, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def font(px):
    return ImageFont.truetype(FONT_BOLD, px)


def vgrad(width, height, top, bottom):
    """Vertical gradient image from top colour to bottom colour."""
    img = Image.new("RGB", (width, height))
    d = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(1, height - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (width, y)], fill=c)
    return img


def text_outlined(draw, xy, s, fnt, fill=WHITE, outline=BLACK, sw=4):
    draw.text(xy, s, font=fnt, fill=fill, stroke_width=sw,
              stroke_fill=outline)


def text_centred(draw, cx, y, s, fnt, fill=WHITE, outline=BLACK, sw=4):
    w = draw.textlength(s, font=fnt)
    text_outlined(draw, (cx - w / 2, y), s, fnt, fill, outline, sw)
    return w


def star4_points(cx, cy, v_arm, h_arm):
    """4-pointed sparkle (diamond star): 8 vertices, long vertical arms."""
    pts = []
    for ang in (270, 0, 90, 180):
        r = v_arm if ang in (90, 270) else h_arm
        a = math.radians(ang)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        # concave corner between arms
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


def ghost_layer():
    """The make.fun ghost on a transparent layer (240x260).

    White ghost, thick black outline, two black 4-point sparkle eyes,
    one small round hand holding a magenta coin with a white star.
    The outline is made by dilating the body mask (MaxFilter) so it is
    even all around, then compositing black under white.
    """
    W, H = 240, 260
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # --- body silhouette as a polygon: dome + sides + wavy bottom ---
    cx, dome_cy, r = 105, 105, 78
    pts = []
    for deg in range(180, -1, -6):  # dome arc, left -> right over the top
        a = math.radians(deg)
        # minus: PIL y grows downward, so the arc must bulge UP
        pts.append((cx + r * math.cos(a), dome_cy - r * math.sin(a)))
    # right side down
    pts.append((cx + r, 205))
    # wavy bottom: 3 upward bumps (semicircle arcs), right -> left
    bump_r = r * 2 / 6
    for i in range(3):
        bcx = cx + r - bump_r * (2 * i + 1)
        for deg in range(0, 181, 12):
            a = math.radians(deg)
            pts.append((bcx + bump_r * math.cos(a),
                        205 - bump_r * math.sin(a)))
    # left side up
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
    # --- sparkle eyes ---
    d.polygon(star4_points(78, 118, 26, 9), fill=(0, 0, 0, 255))
    d.polygon(star4_points(132, 118, 26, 9), fill=(0, 0, 0, 255))
    # --- small round hand on the right side ---
    d.ellipse([168, 148, 196, 176], fill=(0, 0, 0, 255))
    d.ellipse([171, 151, 193, 173], fill=(255, 255, 255, 255))
    # --- magenta coin with white star, held by the hand ---
    d.ellipse([186, 128, 238, 180], fill=MAGENTA_DARK + (255,))
    d.ellipse([189, 131, 235, 177], fill=MAGENTA + (255,))
    d.polygon(star5_points(212, 154, 19, 8), fill=(255, 255, 255, 255))
    return layer


def cover_crop(img, tw, th):
    """Centre-crop img to the target aspect, then resize to (tw, th)."""
    w, h = img.size
    target = tw / th
    if w / h > target:  # too wide: crop sides
        nw = int(h * target)
        x0 = (w - nw) // 2
        img = img.crop((x0, 0, x0 + nw, h))
    else:               # too tall: crop top/bottom
        nh = int(w / target)
        y0 = (h - nh) // 2
        img = img.crop((0, y0, w, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def main():
    canvas = Image.new("RGB", (SIZE, SIZE), (20, 8, 40))
    draw = ImageDraw.Draw(canvas)

    # --- headline band: Vice City sunset gradient ---
    band = vgrad(SIZE, BAND_H, (43, 10, 74), (139, 30, 107))
    canvas.paste(band, (0, 0))
    text_centred(draw, SIZE // 2, 28, "WAITED 13 YEARS FOR GTA VI",
                 font(56), sw=4)

    # --- scene, cover-cropped into the middle band ---
    scene = Image.open(SCENE).convert("RGB")
    scene_area_h = BANNER_TOP - BAND_H
    scene = cover_crop(scene, SIZE, scene_area_h)
    canvas.paste(scene, (0, BAND_H))

    # --- ghost straddling the centre divider, top of the scene ---
    ghost = ghost_layer()
    canvas.paste(ghost, (SIZE // 2 - 120, BAND_H - 12), ghost)

    # --- year labels on the two panels ---
    draw = ImageDraw.Draw(canvas)
    text_outlined(draw, (36, BAND_H + 18), "2013", font(64), sw=5)
    yr = "2026"
    w = draw.textlength(yr, font=font(64))
    text_outlined(draw, (SIZE - 36 - w, BAND_H + 18), yr, font(64), sw=5)

    # --- punchline banner: dark rounded rect ---
    draw.rounded_rectangle([24, BANNER_TOP + 12, SIZE - 24, SIZE - 24],
                           radius=28, fill=(26, 11, 46))
    by = BANNER_TOP + 34
    text_centred(draw, SIZE // 2, by, "WHILE I WAITED, MY AI AGENT",
                 font(44), sw=4)
    text_centred(draw, SIZE // 2, by + 56, "EARNED REAL MONEY ON",
                 font(44), sw=4)
    text_centred(draw, SIZE // 2, by + 112, "make.fun", font(60),
                 fill=(255, 77, 184), sw=4)

    canvas.save(OUT, "PNG")
    canvas.resize((480, 480), Image.LANCZOS).save(PREVIEW_480, "PNG")
    print("saved", OUT, canvas.size)


if __name__ == "__main__":
    main()
